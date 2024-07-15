# Camera-volume add-on for Home Assistant
CeC
July 2024

Monitor volume levels from microphones on remote cameras using ffmpeg
to parse rtsp feeds.  This add-on has only been tested on Amcrest
cameras so it's far from proven.

The addon uses ffmpeg to sample sound from the mic(s) every 5 seconds,
then to report max and mean volume via MQTT every 60s (by default,
but can be changed in /config/cameravolume.yamlif (stats_interval). 
If you want to sample less frequently, this can be adjusted in the
python code (src/get_audio_volume.py  - sample_interval) just
above the main loop).

# To install as a local addon:

1. Customize *cameravolume.yaml* with specifics regarding your MQTT broker address, MQTT username and password, and RTSP feeds (the same feeds you use in Frigate, which will have embedded credentils (so treat this as a secrets file)).

2. Move cameravolume.yaml to /config in Home Assistant

3. If you don't already have /addons/local in Home Assistant, create it. Then create a directory for this particular local addon, named cameravolume.  Thus you now have /addons/local/cameravolume in Home Assistant.

4. Move all of the files in the src directory into a /addons/local/caameravolume

Now the add-on should appear in your add-on store categorized as a local addon.

# To use the addon measurements

For each camera, the addon creates two MQTT topics of the form
"HA/sensor/<camera_name>_audio_volume_mean" and "HA/sensor/<camera_name>_audio_volume_max"
(the HA/sensor prefix can be configured in /config/cameravolume.yamlif you prefer a different prefix)
In your /config/configuration.yaml file you will associate the topics with variables:

'''
mqtt:
  sensor:
    - name: "frontyardcam_volume"
      state_topic: "HA/sensor/frontyardcam_audio_volume_mean"
      unit_of_measurement: 'dB'
'''


