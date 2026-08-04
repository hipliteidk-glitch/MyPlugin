package com.myplugin

import android.content.Context
import com.aliucord.Utils
import com.aliucord.annotations.AliucordPlugin
import com.aliucord.api.CommandsAPI.CommandResult
import com.aliucord.entities.Plugin

@AliucordPlugin(requiresRestart = false)
@Suppress("unused")
class MyPlugin : Plugin() {
    override fun start(context: Context) {
        commands.registerCommand("ping", "Test command from MyPlugin") {
            CommandResult("Pong! MyPlugin is working!", null, false)
        }
        Utils.showToast("MyPlugin started!")
    }

    override fun stop(context: Context) {}
}
