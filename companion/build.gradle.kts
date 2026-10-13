plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android {
    namespace = "com.deploydulupulangnanti.tagheuermclarenwf.companion"
    compileSdk = 36
    defaultConfig {
        applicationId = "com.deploydulupulangnanti.tagheuermclarenwf.companion"
        minSdk = 26
        targetSdk = 36
        versionCode = 6
        versionName = "6.0.0"
    }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
    kotlinOptions { jvmTarget = "17" }
    val signingPath = providers.environmentVariable("RELEASE_STORE_FILE").orNull
    if (signingPath != null) {
        signingConfigs.create("production") {
            storeFile = file(signingPath)
            storePassword = providers.environmentVariable("RELEASE_STORE_PASSWORD").get()
            keyAlias = providers.environmentVariable("RELEASE_KEY_ALIAS").get()
            keyPassword = providers.environmentVariable("RELEASE_KEY_PASSWORD").get()
        }
    }
    buildTypes { release { if (signingPath != null) signingConfig = signingConfigs.getByName("production") } }
}
