#!/bin/bash
# Simple build script for Android (tries multiple methods)

echo "📦 Building Image Viewer APK..."
echo ""

# Try to find Android SDK
ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
if [ -d "$ANDROID_HOME" ]; then
    echo "✅ Found Android SDK at: $ANDROID_HOME"
    export ANDROID_HOME
    export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$PATH"
    
    # Try gradlew
    if [ -f "./gradlew" ]; then
        echo "Building with gradlew..."
        ./gradlew assembleDebug
    else
        echo "❌ gradlew not found"
    fi
else
    echo "❌ Android SDK not found"
    echo ""
    echo "📝 You have two options:"
    echo ""
    echo "1. Use Docker (recommended):"
    echo "   chmod +x build_apk_docker.sh"
    echo "   ./build_apk_docker.sh"
    echo ""
    echo "2. Install Android SDK and build locally:"
    echo "   - Install Android Studio or command-line tools"
    echo "   - Set ANDROID_HOME environment variable"
    echo "   - Run ./gradlew assembleDebug"
    echo ""
    echo "3. Or just use the web version: image_viewer.html"
fi
