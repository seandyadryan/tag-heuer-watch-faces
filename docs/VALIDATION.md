# Validation evidence

Automated checks cover builds/lint, the pinned official WFF v1 validator, reference integrity, hand-pivot coordinates, ambient second-hand visibility, complete locale key sets, and absence of DEX in wearable APK. The official memory-footprint evaluator is configured in GitHub CI. Logs and APKs are downloadable from Actions.

The decoded image upper bound script is a conservative artwork check, not a replacement for Google's official evaluator or device performance testing. No test proves compatibility with every smartwatch or every language.

Before commercial release, validate installation from Play internal testing on physical devices, ambient brightness/burn-in behavior, battery impact, timezone/DST changes, 12/24-hour settings, watch customization, small and large screens, phone large-font layouts and all locale translations. Play Console review and trademark authorization remain outside automated build validation.
