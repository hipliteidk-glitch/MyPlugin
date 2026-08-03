#!/bin/bash
# Build the APK for the Image Viewer app

echo "Building Image Viewer APK..."

# Clean any previous builds
./gradlew clean

# Build the debug APK
./gradlew assembleDebug

if [ -f "app/build/outputs/apk/debug/app-debug.apk" ]; then
    echo "✅ APK built successfully!"
    echo "📱 APK location: app/build/outputs/apk/debug/app-debug.apk"
    cp app/build/outputs/apk/debug/app-debug.apk ../image_viewer.apk
    echo "📋 Copied to: ../image_viewer.apk"
else
    echo "❌ Build failed. Check the output above for errors."
fi
