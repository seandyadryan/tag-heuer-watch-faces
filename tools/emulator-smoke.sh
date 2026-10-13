#!/usr/bin/env bash
set -euo pipefail
device="$1"
package=com.deploydulupulangnanti.tagheuermclarenwf
mkdir -p evidence
adb logcat -c
adb shell input keyevent KEYCODE_WAKEUP
adb shell input keyevent KEYCODE_HOME
if [ "$device" = phone ]; then
  activity="com.deploydulupulangnanti.tagheuermclarenwf.companion.MainActivity"
  adb install -r "$(find packages -name companion-debug.apk -print -quit)"
  adb shell am start -W -n "$package/$activity"
  sleep 3
  adb shell dumpsys activity activities > evidence/activity.txt
  grep -q "$activity" evidence/activity.txt
  adb exec-out screencap -p > evidence/phone-en.png
  adb shell cmd locale set-app-locales "$package" --user 0 --locales id
  adb shell am force-stop "$package"
  adb shell am start -W -n "$package/$activity"
  sleep 2
  adb exec-out screencap -p > evidence/phone-id.png
  adb shell input swipe 540 1850 540 400 600
  sleep 1
  adb exec-out screencap -p > evidence/phone-guide-id.png
  adb shell cmd locale set-app-locales "$package" --user 0 --locales ar
  adb shell am force-stop "$package"
  adb shell am start -W -n "$package/$activity"
  sleep 2
  adb exec-out screencap -p > evidence/phone-ar.png
else
  adb install -r "$(find packages -name wear-debug.apk -print -quit)"
  adb shell pm path "$package" | tee evidence/installed-package.txt
  grep -q 'package:' evidence/installed-package.txt
  adb shell settings put global device_provisioned 1
  adb shell settings put secure user_setup_complete 1
  adb shell svc power stayon true
  selected=false
  rendered=false
  for attempt in $(seq 1 18); do
    sleep 5
    if [ "$selected" != true ]; then
      adb shell am broadcast -a com.google.android.wearable.app.DEBUG_SURFACE --es operation set-watchface --es watchFaceId "$package" | tee evidence/select-face.txt
      if grep -q 'Favorite Id=' evidence/select-face.txt; then selected=true; fi
    fi
    adb shell input keyevent KEYCODE_WAKEUP
    adb shell input keyevent KEYCODE_HOME
    adb exec-out screencap -p > evidence/wear-active.png
    if [ "$selected" = true ] && python3 tools/check_wear_screenshot.py evidence/wear-active.png; then
      rendered=true
      break
    fi
  done
  adb shell dumpsys wallpaper > evidence/wallpaper.txt
  adb shell dumpsys activity activities > evidence/activity.txt
  if [ "$rendered" != true ]; then
    adb logcat -d > evidence/logcat.txt
    echo 'Watch face has not become visible after boot'; exit 1
  fi
  grep -q 'DeclarativeWatchFaceRuntime' evidence/wallpaper.txt
fi
adb logcat -d > evidence/logcat.txt
if grep -q "Process: $package," evidence/logcat.txt; then
  echo 'Application crash detected'; exit 1
fi
if grep -q 'Process: com.google.wear.watchface.runtime,' evidence/logcat.txt; then
  echo 'WFF runtime crash detected'; exit 1
fi
echo 'Installation/launch smoke checks passed. Review screenshots for rendered UI evidence.'
