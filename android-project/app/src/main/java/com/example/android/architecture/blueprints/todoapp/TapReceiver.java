package com.example.android.architecture.blueprints.todoapp;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class TapReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent.getAction().equals("com.example.TAP")) {
            int x = intent.getIntExtra("x", 300);
            int y = intent.getIntExtra("y", 1000);
            TapService service = TapService.getInstance();
            if (service != null) {
                service.performTap(x, y);
            }
        }
    }
}