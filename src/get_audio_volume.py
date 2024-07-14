import subprocess
import paho.mqtt.client as mqtt
import logging
import time
import yaml
import os

# Set up logging to standard output with timestamps
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Load user configuration from cameravolume.yaml (from the /config folder)
config_path = '/config/cameravolume.yaml'  
if not os.path.exists(config_path):
    logger.error(f"Configuration file {config_path} does not exist.")
    raise FileNotFoundError(f"Configuration file {config_path} does not exist.")

with open(config_path) as f:
    config = yaml.safe_load(f)

# Extracting MQTT settings
mqtt_settings = config.get('mqtt', {})
mqtt_host = mqtt_settings.get('host')
mqtt_port = mqtt_settings.get('port')
mqtt_topic_prefix = mqtt_settings.get('topic_prefix')
mqtt_client_id = mqtt_settings.get('client_id')
mqtt_username = mqtt_settings.get('user')
mqtt_password = mqtt_settings.get('password')
mqtt_stats_interval = mqtt_settings.get('stats_interval', 60)

# Extracting camera settings
camera_settings = config.get('cameras', {})
camera_ffmpeg_path = camera_settings.get('cam1', {}).get('ffmpeg', {}).get('path')

def get_audio_volume(rtsp_url, duration=10):
    command = [
        'ffmpeg',
        '-use_wallclock_as_timestamps', '1',
        '-i', rtsp_url,
        '-vn',
        '-af', 'volumedetect',
        '-t', str(duration),
        '-f', 'null',
        '/dev/null'
    ]

    logger.debug(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stderr_output = result.stderr
    logger.debug("Command executed.")
    logger.debug("stderr output:\n%s", stderr_output)

    mean_volume = None
    for line in stderr_output.split('\n'):
        if 'mean_volume' in line:
            logger.debug("Found mean_volume line: %s", line)
            try:
                mean_volume = float(line.split()[-2])
                logger.debug("Extracted mean_volume: %f", mean_volume)
            except ValueError as e:
                logger.error("Error parsing mean_volume: %s", e)
            break

    if mean_volume is None:
        logger.debug("mean_volume not found.")

    return mean_volume

# MQTT connection setup
mqtt_client = mqtt.Client(client_id=mqtt_client_id)
mqtt_client.username_pw_set(mqtt_username, mqtt_password)

def on_connect(client, userdata, flags, rc):
    logger.debug(f"Connected to MQTT broker with result code {rc}")
    if rc == 0:
        logger.debug("Publishing debug message to {}/debug".format(mqtt_topic_prefix))
        client.publish("{}/debug".format(mqtt_topic_prefix), "MQTT connection successful")

def on_publish(client, userdata, mid):
    logger.debug(f"MQTT message published with mid {mid}")

mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish

logger.debug("Attempting to connect to MQTT broker...")
try:
    mqtt_client.connect(mqtt_host, mqtt_port, 60)
    mqtt_client.loop_start()
except Exception as e:
    logger.error(f"Failed to connect to MQTT broker: {e}")

while True:
    volume = get_audio_volume(camera_ffmpeg_path, duration=10)
    logger.debug(f"Volume: {volume}")

    if volume is not None:
        if mqtt_client.is_connected():
            try:
                result = mqtt_client.publish("{}/FrontDoorCam_audio_volume".format(mqtt_topic_prefix), volume)
                result.wait_for_publish()
                logger.debug(f"MQTT message publish result: {result.rc}")
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    logger.debug("MQTT message successfully published.")
                else:
                    logger.error(f"Failed to publish MQTT message, return code: {result.rc}")
            except Exception as e:
                logger.error(f"Failed to publish MQTT message: {e}")
        else:
            logger.error("MQTT client is not connected. Skipping publish.")
    else:
        logger.debug("Volume is None. MQTT message not sent.")

    # Sleep for a while before checking again
    time.sleep(mqtt_stats_interval)

# Disconnect from MQTT broker on exit
mqtt_client.loop_stop()
mqtt_client.disconnect()
logger.debug("Disconnected from MQTT broker.")

