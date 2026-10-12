#!/usr/bin/env bash
set -euo pipefail
device="$1"
package=com.deploydulupulangnanti.tagheuermclarenwf
mkdir -p evidence
adb logcat -c
adb shell input keyevent KEYCODE_WAKEUP
adb shell input keyevent KEYCODE_HOME
if [ "$device" = phone ]; then
  package="$package.companion"
  adb install -r "$(find packages -name companion-debug.apk -print -quit)"
  adb shell am start -W -n "$package/.MainActivity"
  sleep 3
  adb shell dumpsys activity activities > evidence/activity.txt
  grep -q "$package/.MainActivity" evidence/activity.txt
  adb exec-out screencap -p > evidence/phone-en.png
  adb shell cmd locale set-app-locales "$package" --user 0 --locales id
  adb shell am force-stop "$package"
  adb shell am start -W -n "$package/.MainActivity"
  sleep 2
  adb exec-out screencap -p > evidence/phone-id.png
  adb shell cmd locale set-app-locales "$package" --user 0 --locales ar
  adb shell am force-stop "$package"
  adb shell am start -W -n "$package/.MainActivity"
  sleep 2
  adb exec-out screencap -p > evidence/phone-ar.png
else
  adb install -r "$(find packages -name wear-debug.apk -print -quit)"
  adb shell pm path "$package" | tee evidence/installed-package.txt
  grep -q 'package:' evidence/installed-package.txt
  adb shell settings put global device_provisioned 1
  adb shell settings put secure user_setup_complete 1
  adb shell am broadcast -a com.google.android.wearable.app.DEBUG_SURFACE --es operation set-watchface --es watchFaceId "$package" | tee evidence/select-face.txt
  sleep 10
  adb shell input keyevent KEYCODE_HOME
  sleep 2
  adb exec-out screencap -p > evidence/wear-active.png
  adb shell dumpsys wallpaper > evidence/wallpaper.txt
fi
adb logcat -d > evidence/logcat.txt
if grep -q "Process: $package," evidence/logcat.txt; then
  echo 'Application crash detected'; exit 1
fi
echo 'Installation/launch smoke checks passed. Review screenshots for rendered UI evidence.'
