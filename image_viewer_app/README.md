# Image Viewer Android App

A simple Android app that displays images and lets you cycle through them.

## 📸 Changing Images

### Method 1: Edit the code (recommended for developers)
1. Open `app/src/main/java/com/example/imageviewer/MainActivity.java`
2. Find the `imageResources` array:
   ```java
   private int[] imageResources = {
       R.drawable.image1,
       R.drawable.image2,
       R.drawable.image3,
       R.drawable.image4,
       R.drawable.image5
   };
   ```
3. Add or remove image references:
   - To add: `R.drawable.your_new_image`
   - To remove: delete the line
4. Make sure your image files are in `app/src/main/res/drawable/`

### Method 2: Replace the image files
1. Go to `app/src/main/res/drawable/`
2. Replace `image1.png`, `image2.png`, etc. with your own images
3. Keep the same filenames or update the code to match

### Method 3: Regenerate sample images
1. Edit `generate_images.py` - change colors and text
2. Run: `python3 generate_images.py`
3. Rebuild the APK

## 🏗️ Building the APK

### Option A: Using Docker (recommended, no Android SDK needed)
```bash
chmod +x build_apk_docker.sh
./build_apk_docker.sh
```

The APK will be at `image_viewer.apk` in the parent folder.

### Option B: Using local Gradle (requires Android SDK)
```bash
./gradlew assembleDebug
```

### Option C: Using Android Studio
1. Open this project in Android Studio
2. Build → Build Bundle(s) / APK(s) → Build APK(s)

## 📱 App Features
- **Next/Prev buttons** to cycle through images
- **Long press image** to reset to first image
- **Clean dark theme**
- **Easy to customize**

## 📁 Project Structure
```
image_viewer_app/
├── app/
│   ├── src/main/
│   │   ├── java/com/example/imageviewer/
│   │   │   └── MainActivity.java    ← Edit image list here
│   │   ├── res/
│   │   │   ├── drawable/            ← Put your PNG images here
│   │   │   │   ├── image1.png
│   │   │   │   ├── image2.png
│   │   │   │   └── ...
│   │   │   └── layout/
│   │   │       └── activity_main.xml
│   │   └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle
├── settings.gradle
├── generate_images.py               ← Change colors/text here
└── build_apk_docker.sh              ← Build script
```

## 🔧 Customization Tips

### Change app name
Edit `app/src/main/AndroidManifest.xml`:
```xml
android:label="Your App Name"
```

### Change colors
Edit the colors in `generate_images.py` or replace the images directly.

### Change button text
Edit `app/src/main/res/layout/activity_main.xml`:
```xml
android:text="New Text"
```

### Add more images
1. Add your image to `app/src/main/res/drawable/`
2. Add `R.drawable.your_image` to the `imageResources` array in MainActivity.java

## 📝 Notes
- The app uses AndroidX and Material Design components
- Minimum Android version: Android 5.0 (API 21)
- All images are bundled in the APK
