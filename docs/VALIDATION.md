# Validation evidence

## Reference dial update — 1.1.0

- [CI passed](https://github.com/seandyadryan/tag-heuer-watch-faces/actions/runs/38232787289): both builds/lint, WFF schema, resource references and pivots, full locale sets, and official memory test.
- [Signed release passed](https://github.com/seandyadryan/tag-heuer-watch-faces/actions/runs/38232790676): version code 2 / 1.1.0 AABs and APKs for both modules. APK signer matches the existing keystore SHA-256 below.
- [Emulator checks passed](https://github.com/seandyadryan/tag-heuer-watch-faces/actions/runs/38232798899): the red reference dial is visible on Wear OS API 33, with separate moving subdial hands and the actual day-of-month rendered in the date aperture. Android API 36 phone preview and locale checks also passed.
- The composed preview and actual Wear OS screenshot were visually inspected. Conservative decoded artwork upper bound is 3.89 MiB, including retained original assets. The high-resolution source master is outside Android resources and is not shipped in the APK.

![Red dial actually running on Wear OS 4](images/wear-os4-red.png)

## Verified on 12 October 2026

- [Android CI passed](https://github.com/seandyadryan/tag-heuer-watch-faces/actions/runs/38229884979): builds/lint for both modules, full 21-locale resource contracts, official WFF v1 schema validator, and official memory-footprint test (10 MB ambient / 100 MB active limits).
- [Signed release passed](https://github.com/seandyadryan/tag-heuer-watch-faces/actions/runs/38228479264): both release AABs/APKs, target API 35 for Wear OS and 36 for the phone. Application source is unchanged by subsequent smoke-test/runner/documentation commits.
- [Emulator smoke checks passed](https://github.com/seandyadryan/tag-heuer-watch-faces/actions/runs/38229887160): Wear OS API 33 install, WFF runtime selection and a visible papaya dial; Android API 36 phone launch, English/Indonesian/Arabic locale switching, and scrolling the Indonesian installation guide. Screenshots were visually reviewed.
- Wear APK and AAB contain no DEX. APK signature verified with Android `apksigner`; AAB signature verified with `jarsigner`. Signer matches the local keystore certificate: SHA-256 `5acee92e74307870f22a517136bbba0b1e61c1ea2b12becc797caeddad1c0a27`.
- Toolchain: JDK 17, AGP 8.10.1, Kotlin 2.1.21, Gradle 8.11.1. GitHub-hosted runner pinned to Ubuntu 24.04.

![Actual watch face running on Wear OS 4 emulator](images/wear-os4.png)

[Actual Indonesian installation guide screenshot](images/phone-guide-id.png)

Automated checks cover builds/lint, the pinned official WFF v1 validator, reference integrity, hand-pivot coordinates, ambient second-hand visibility, complete locale key sets, and absence of DEX in wearable APK. The official memory-footprint evaluator is configured in GitHub CI. Logs and APKs are downloadable from Actions.

The decoded image upper bound script is a conservative artwork check, not a replacement for Google's official evaluator or device performance testing. No test proves compatibility with every smartwatch or every language. Only one Wear OS emulator profile and one phone emulator profile have been tested; the other 18 interface locales have resource-completeness checks but no emulator/native-speaker review.

Before commercial release, validate installation from Play internal testing on physical devices, ambient brightness/burn-in behavior, battery impact, timezone/DST changes, 12/24-hour settings, watch customization, small and large screens, phone large-font layouts and all locale translations. Play Console review and trademark authorization remain outside automated build validation.
