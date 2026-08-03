#!/bin/bash
# Build APK using Docker (no Android SDK needed locally)

echo "📦 Building Image Viewer APK using Docker..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   On Termux: pkg install docker"
    echo "   Or install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Create a Dockerfile for Android build
cat > Dockerfile.android << 'EOF'
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    wget \
    unzip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Android SDK
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools

RUN mkdir -p $ANDROID_SDK_ROOT/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O /tmp/cmdline-tools.zip && \
    unzip /tmp/cmdline-tools.zip -d $ANDROID_SDK_ROOT/cmdline-tools && \
    mv $ANDROID_SDK_ROOT/cmdline-tools/cmdline-tools $ANDROID_SDK_ROOT/cmdline-tools/latest && \
    rm /tmp/cmdline-tools.zip

# Accept licenses
RUN yes | sdkmanager --licenses > /dev/null 2>&1 || true

# Install build tools
RUN sdkmanager "build-tools;33.0.0" "platforms;android-33" > /dev/null 2>&1

WORKDIR /app
CMD ["./gradlew", "assembleDebug"]
EOF

echo "Building Docker image..."
docker build -f Dockerfile.android -t android-builder .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed. Make sure Docker is running."
    exit 1
fi

echo ""
echo "Compiling APK..."
docker run --rm -v $(pwd):/app android-builder

if [ -f "app/build/outputs/apk/debug/app-debug.apk" ]; then
    echo ""
    echo "✅ APK built successfully!"
    echo "📱 APK location: app/build/outputs/apk/debug/app-debug.apk"
    cp app/build/outputs/apk/debug/app-debug.apk ../image_viewer.apk
    echo "📋 Also copied to: ../image_viewer.apk"
    echo ""
    echo "📝 To change the images:"
    echo "   1. Edit generate_images.py - modify the colors and text"
    echo "   2. Or replace the PNGs in app/src/main/res/drawable/"
    echo "   3. Run this script again to rebuild"
else
    echo "❌ Build failed. Check the output above for errors."
    exit 1
fi
