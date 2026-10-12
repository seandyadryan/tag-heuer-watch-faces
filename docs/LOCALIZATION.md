# Localization

21 complete interface/pairing-guide locale resources: English (`en`), Indonesian (`id`/Android `in`), Spanish, French, German, Italian, Portuguese, Russian, Arabic, Hindi, Japanese, Korean, Simplified Chinese, Traditional Chinese, Thai, Vietnamese, Turkish, Dutch, Polish, Ukrainian, Malay.

Android resolves locale resources automatically; the phone guide also exposes a manual language selector. Android 13+ uses system application locales. Earlier Android versions persist an override in local preferences. System language resets the override. Arabic uses native RTL layout; brand typography and artwork remain fixed names/numerals.

Other languages fall back to English. Do not claim every language is translated. Draft translations have not been reviewed by native speakers, and regional terminology may differ. Store listings require their own translated metadata; these resources do not automatically translate Play listings.

Add translations to `tools/generate_locales.py`, run it with Python, then run `tools/verify_project.py`. It checks that every locale has the full set of interface strings. Rebuild and test language switching, long text, font scaling, Hindi/Thai glyphs, Arabic RTL and Chinese scripts. The watch editor accent label uses the same translations.
