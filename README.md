# Camera-volume add-on for Home Assistant
CeC
July 2024

Monitor volume levels from microphones on remote cameras using ffmpeg
to parse rtsp feeds.  This add-on has only been tested on Amcrest
cameras so it's far from proven.

The addon uses ffmpeg to sample sound from the mic(s) every 5 seconds,
then to report max and mean volume via MQTT every 60s (by default).

# To install as a local addon:

1. Customize *cameravolume.yaml* with specifics regarding your MQTT broker address,
MQTT username and password, and RTSP feeds. These will be the same feeds you use
in Frigate (if you use Frigate), which may have embedded credentils
(so treat this as a secrets file). If you want to report less frequently than
every 60s you can change the *stats_interval* value in this file.

2. Move *cameravolume.yaml* to the */config* directory in Home Assistant

3. If you don't already have */addons/local* in Home Assistant, create it. Then
create a directory for this particular local addon, named *cameravolume*.
Thus you now have */addons/local/cameravolume* in Home Assistant.

4. Move all of the files in the *src* directory into the */addons/local/caameravolume*
folder in Home Assistant..

5. Make sure the permissions are correct - in your */addons/local/cameravolume*
directory in Home Assistant set them:
```
chmod 755 ./*
```

You should now be able to go to the Add-on store and see this add-on in the local
section.  If not, select "Check for Updates" from the 3-dot icon at upper right, 
then reload the page.  If it still does not show up, review the instructions above.

# To use the addon measurements

For each camera, the addon creates two MQTT topics of the form

  *HA/sensor/<camera_name>_audio_volume_mean* and

  *HA/sensor/<camera_name>_audio_volume_max*

(the HA/sensor prefix can be configured in /config/cameravolume.yamlif you prefer a different prefix)
In your /config/configuration.yaml file you will associate the topics with variables as in the
code block below, for instance if your cameras are named "drivewaycam" and "poolcam." (you may
have other conventions you use for the names)

```
mqtt:
  sensor:
    - name: "drivewaycam_volume_mean"
      state_topic: "HA/sensor/drivewaycam_audio_volume_mean"
      unit_of_measurement: 'dB'
    - name: "drivewaycam_volume_max"
      state_topic: "HA/sensor/drivewaycam_audio_volume_max"
      unit_of_measurement: 'dB'
    - name: "poolcam_volume_mean"
      state_topic: "HA/sensor/poolcam_audio_volume_mean"
      unit_of_measurement: 'dB'
    - name: "poolcam_volume_max"
      state_topic: "HA/sensor/poolcam_audio_volume_max"
      unit_of_measurement: 'dB'
```

