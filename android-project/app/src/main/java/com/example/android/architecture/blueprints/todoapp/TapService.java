package com.example.android.architecture.blueprints.todoapp;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.GestureDescription;
import android.content.Context;
import android.content.Intent;
import android.graphics.Path;
import android.os.Build;
import android.view.accessibility.AccessibilityEvent;

public class TapService extends AccessibilityService {
    private static TapService instance;
    private static Context appContext;

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {}

    @Override
    public void onInterrupt() {}

    @Override
    public void onServiceConnected() {
        instance = this;
    }

    @Override
    public void onDestroy() {
        instance = null;
        super.onDestroy();
    }

    public static TapService getInstance() {
        return instance;
    }

    // Helper to create the service context for plugin usage
    public static void createInstance(Context context) {
        appContext = context.getApplicationContext();
        // In a real plugin, we might need to bind the service
        // For now we store the context for later use
    }

    public static Context getAppContext() {
        return appContext;
    }

    public void performTap(int x, int y) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            Path path = new Path();
            path.moveTo(x, y);
            GestureDescription.Builder gestureBuilder = new GestureDescription.Builder();
            gestureBuilder.addStroke(new GestureDescription.StrokeDescription(path, 0, 100));
            dispatchGesture(gestureBuilder.build(), null, null);
        }
    }

    // Start the accessibility service (for standalone app usage)
    public static void startService(Context context) {
        Intent intent = new Intent(context, TapService.class);
        context.startService(intent);
    }
}
