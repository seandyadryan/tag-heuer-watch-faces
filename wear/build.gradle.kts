plugins { id("com.android.application") }
android {
    namespace = "com.deploydulupulangnanti.tagheuermclarenwf"
    compileSdk = 36
    defaultConfig {
        applicationId = "com.deploydulupulangnanti.tagheuermclarenwf"
        minSdk = 33
        targetSdk = 36
        versionCode = 5
        versionName = "5.0.0"
    }
    val signingPath = providers.environmentVariable("RELEASE_STORE_FILE").orNull
    if (signingPath != null) {
        signingConfigs.create("production") {
            storeFile = file(signingPath)
            storePassword = providers.environmentVariable("RELEASE_STORE_PASSWORD").get()
            keyAlias = providers.environmentVariable("RELEASE_KEY_ALIAS").get()
            keyPassword = providers.environmentVariable("RELEASE_KEY_PASSWORD").get()
        }
    }
    buildTypes {
        debug {
            // Remove generated R classes so the WFF APK contains resources only.
            isMinifyEnabled = true
            isShrinkResources = false
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = false
            if (signingPath != null) signingConfig = signingConfigs.getByName("production")
        }
    }
}
