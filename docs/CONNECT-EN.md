# Install on a smartwatch

1. Confirm the watch runs Wear OS 4 or newer and has Google Play. Other watch platforms require separate implementations.
2. Pair the watch using its manufacturer's phone app. Use the same Google account on phone and watch.
3. Open Google Play **on the watch**, find TAG Heuer McLaren 30th, purchase and install after publication. Alternatively select the compatible watch from the phone's Play listing.
4. Long-press the current watch face, choose Add watch face, select TAG Heuer McLaren 30th. Menu names vary by manufacturer.
5. Choose Edit/Customize to select an accent. Phone preview preferences are separate. Always-on display is controlled by the watch system settings.

Installing the optional phone guide does not install or transfer the face. Missing listing? Check publication, country, Google account, Wear OS version and watch compatibility. Missing face? Check installation on the watch, use Add watch face, then restart if needed.

Developer wireless debugging: pair with `adb pair WATCH_IP:PAIRING_PORT`, enter the watch's code, connect with `adb connect WATCH_IP:CONNECTION_PORT`, then install `wear/build/outputs/apk/debug/wear-debug.apk` using `adb -s WATCH_IP:CONNECTION_PORT install -r`. Pairing and connection ports can differ. Use APK, not AAB. Disable wireless debugging after testing.
