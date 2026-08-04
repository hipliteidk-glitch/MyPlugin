@file:Suppress("UnstableApiUsage")

import com.aliucord.gradle.AliucordExtension
import org.jetbrains.kotlin.gradle.dsl.JvmTarget
import org.jetbrains.kotlin.gradle.dsl.KotlinAndroidExtension

plugins {
    alias(libs.plugins.android.library)
    alias(libs.plugins.aliucord.plugin)
    alias(libs.plugins.kotlin.android)
}

version = "1.0.0"

android {
    namespace = "com.myplugin"
    compileSdk = 36

    defaultConfig {
        minSdk = 21
    }

    buildFeatures {
        buildConfig = true
        resValues = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_21
        targetCompatibility = JavaVersion.VERSION_21
    }
}

configure<AliucordExtension> {
    author("hipliteidk", 0L, hyperlink = false)
    github("https://github.com/hipliteidk-glitch/MyPlugin")
}

configure<KotlinAndroidExtension> {
    compilerOptions {
        jvmTarget = JvmTarget.JVM_21
        optIn.add("kotlin.RequiresOptIn")
    }
}

dependencies {
    compileOnly(libs.discord)
    compileOnly(libs.aliucord)
    compileOnly(libs.kotlin.stdlib)
}
