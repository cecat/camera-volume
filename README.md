# Camera-volume add-on for Home Assistant

Monitor volume levels from microphones on remote cameras using ffmpeg to parse rtsp feeds.

# Simple install as a local addon

1. Customize cameravolume.yaml with specifics regarding your MQTT broker address, MQTT username and password, and RTSP feeds (the same feeds you use in Frigate, which will have embedded credentils (so treat this as a secrets file)).

2. Move cameravolume.yaml to /config in Home Assistant

3. If you don't already have /addons/local in Home Assistant, create it. Then create a directory for this particular local addon, named cameravolume.  Thus you now have /addons/local/cameravolume in Home Assistant.

4. Move all of the files in the src directory into a /addons/local/caameravolume

Now the add-on should appear in your add-on store categorized as a local addon.


