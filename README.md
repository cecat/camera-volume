# Camera-volume add-on for Home Assistant
CeC
July 2024

### NOTE: This is a local add-on
Installing it from here will mean having the static files on your
machine.  I recommend instead that you add the repository below to
our Add-on store page, and install the add-on from its repository
so that you are able to get updates/fixes:
```
https://github.com/cecat/CeC-HA-Addons.git
```

[![Open your Home Assistant instance and show the add-on store.](https://my.home-assistant.io/badges/supervisor_store.svg)](https://my.home-assistant.io/redirect/supervisor_store/)

## Description

Monitor volume levels from microphones on remote cameras using ffmpeg
to parse rtsp feeds.  This add-on has only been tested on Amcrest
cameras so it's far from proven.

The add-on uses ffmpeg to sample 5s of sound from the mic(s) every 10s,
then to report max and mean volume via MQTT every 60s.

## To install as a local add-on:

1. Customize *cameravolume.yaml* with specifics regarding your MQTT broker address,
MQTT username and password, and RTSP feeds. These will be the same feeds you use
in Frigate (if you use Frigate), which may have embedded credentils
(so treat this as a secrets file). If you want to report less frequently than
every 60s you can change the *stats_interval* value in this file.

2. Move *cameravolume.yaml* to the */config* directory in Home Assistant

3. If you don't already have */addons/local* in Home Assistant, create it. Then
create a directory for this particular local add-on, named *cameravolume*.
Thus you now have */addons/local/cameravolume* in Home Assistant.

4. Move all of the files in the *src* directory here into the */addons/local/caameravolume*
directory in Home Assistant..

5. Make sure the permissions are correct - in your */addons/local/cameravolume*
directory in Home Assistant set them:
```
chmod 755 ./*
```

You should now be able to go to the Add-on store and see this add-on in the local
section.  If not, select "Check for Updates" from the 3-dot icon at upper right, 
then reload the page.  If it still does not show up, review the instructions above.

## To use the add-on measurements

For each camera, the add-on creates two MQTT topics of the form

  *HA/sensor/<camera_name>_audio_volume_mean*

  and

  *HA/sensor/<camera_name>_audio_volume_max*

If you prefer a prefix different than HA/sensor this can be configured in
*/config/cameravolume.yaml*.

To assign the MQTT data series' to Home Assistant variables that you can
use (to graph, or trigger automations, etc.) you will need to associate
the topics with Home Assistant variables.  You do this in your
*/config/configuration.yaml* file in the form of the
code block below. In this example, the cameras are named "foocam"
and "barcam." You may also have another scheme you use to name 
variables. As with camera names (or mqtt topics), these names can
be whatever works for you.

```
mqtt:
  sensor:
    - name: "foocam_volume_mean"
      state_topic: "HA/sensor/foocam_audio_volume_mean"
      unit_of_measurement: 'dB'
    - name: "foocam_volume_max"
      state_topic: "HA/sensor/foocam_audio_volume_max"
      unit_of_measurement: 'dB'
    - name: "barcam_volume_mean"
      state_topic: "HA/sensor/barcam_audio_volume_mean"
      unit_of_measurement: 'dB'
    - name: "barcam_volume_max"
      state_topic: "HA/sensor/barcam_audio_volume_max"
      unit_of_measurement: 'dB'
```

## A Note about FFmpeg volume measurements

FFmpeg measurements are in dBFS (decibels relative to Full Scale), where the maximum
possible volume level (digitally, from the point of view of the microphone) is 0 dBFS.
So these dBFS measurementsare negative numbers, and differ from the more commonly
seen dB SPL (Sound Pressure Level) measurements we see.  With my very 
limited poking around I see dBFS readings from this add-on in the -50 to -60 range
for a quiet evening without traffic noise, and about -40 playing Gimme Shelter near
the camera at a volume my Apple watch pegged at 75dB.

It's non-trivial to map dBFS to DB SPL, so this add-on is more aimed at detecting
changes or unusual sound events.
