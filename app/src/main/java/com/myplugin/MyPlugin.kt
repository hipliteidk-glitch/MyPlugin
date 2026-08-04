package com.myplugin

import android.content.Context
import com.aliucord.Utils
import com.aliucord.annotations.AliucordPlugin
import com.aliucord.entities.Plugin
import com.aliucord.patcher.*

@AliucordPlugin(requiresRestart = false)
@Suppress("unused")
class MyPlugin : Plugin() {
    override fun start(context: Context) {
        try {
            // Log deleted messages
            patcher.after(
                "com.discord.stores.StoreMessages",
                "deleteMessage"
            ) { param ->
                val message = param.args[0]
                Utils.log("📝 Deleted message: $message")
            }

            // Log edited messages
            patcher.after(
                "com.discord.stores.StoreMessages",
                "editMessage"
            ) { param ->
                val message = param.args[0]
                Utils.log("✏️ Edited message: $message")
            }

            Utils.showToast("MyPlugin started!")
        } catch (e: Exception) {
            Utils.log("❌ Plugin error: ${e.message}")
        }
    }

    override fun stop(context: Context) {
        try {
            patcher.unpatchAll()
            Utils.showToast("MyPlugin stopped!")
        } catch (e: Exception) {
            Utils.log("❌ Stop error: ${e.message}")
        }
    }
}
