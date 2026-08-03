package com.example.android.architecture.blueprints.todoapp

import dev.aliucord.api.Plugin
import dev.aliucord.api.events.ReceiveBroadcastEvent
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.Build
import android.util.Log

class TapPlugin : Plugin() {
    private var tapService: TapService? = null
    private var tapReceiver: TapReceiver? = null

    override fun onStart(context: Context) {
        Log.d("TapPlugin", "Starting TapPlugin")
        // Initialize the service
        tapService = TapService.getInstance()
        if (tapService == null) {
            // If service not created yet, create it
            TapService.createInstance(context)
            tapService = TapService.getInstance()
        }

        // Register the broadcast receiver to listen for TAP intents
        tapReceiver = TapReceiver()
        val filter = IntentFilter("com.example.TAP")
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            context.registerReceiver(tapReceiver, filter, Context.RECEIVER_NOT_EXPORTED)
        } else {
            context.registerReceiver(tapReceiver, filter)
        }

        Log.d("TapPlugin", "TapPlugin started successfully")
    }

    override fun onStop(context: Context) {
        Log.d("TapPlugin", "Stopping TapPlugin")
        try {
            context.unregisterReceiver(tapReceiver)
        } catch (e: Exception) {
            // Receiver already unregistered or not registered
        }
        tapService = null
        Log.d("TapPlugin", "TapPlugin stopped")
    }

    // Optional: expose a method to perform taps directly from other plugin code
    fun performTap(x: Int, y: Int) {
        tapService?.performTap(x, y)
    }
}
