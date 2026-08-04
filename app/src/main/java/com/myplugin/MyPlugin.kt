package com.myplugin

import com.aliucord.entities.Plugin
import com.aliucord.api.PatcherAPI
import com.aliucord.api.API
import com.aliucord.utils.Utils

class MyPlugin : Plugin() {
    override fun start() {
        try {
            // Log deleted messages
            PatcherAPI.patch(
                "com.discord.stores.StoreMessages",
                "deleteMessage",
                { args ->
                    val message = args[0]
                    Utils.log("📝 Deleted message: $message")
                }
            )

            // Log edited messages
            PatcherAPI.patch(
                "com.discord.stores.StoreMessages",
                "editMessage",
                { args ->
                    val message = args[0]
                    Utils.log("✏️ Edited message: $message")
                }
            )

            Utils.showToast("MyPlugin started!")
        } catch (e: Exception) {
            Utils.log("❌ Plugin error: ${e.message}")
        }
    }

    override fun stop() {
        try {
            PatcherAPI.unpatchAll()
            Utils.showToast("MyPlugin stopped!")
        } catch (e: Exception) {
            Utils.log("❌ Stop error: ${e.message}")
        }
    }
}
