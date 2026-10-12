package com.deploydulupulangnanti.tagheuermclarenwf.companion

import android.app.Activity
import android.app.AlertDialog
import android.app.LocaleManager
import android.content.Context
import android.content.Intent
import android.content.res.Configuration
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.LocaleList
import android.view.Gravity
import android.view.View
import android.widget.*
import java.util.Locale

class MainActivity : Activity() {
    override fun attachBaseContext(newBase: Context) {
        val tag = newBase.getSharedPreferences("settings", MODE_PRIVATE).getString("language", "") ?: ""
        if (tag.isEmpty() || Build.VERSION.SDK_INT >= 33) { super.attachBaseContext(newBase); return }
        val config = Configuration(newBase.resources.configuration)
        config.setLocales(LocaleList(Locale.forLanguageTag(tag)))
        super.attachBaseContext(newBase.createConfigurationContext(config))
    }

    private val orange = Color.rgb(255, 135, 0)
    private fun dp(v: Int) = (v * resources.displayMetrics.density).toInt()
    private fun label(value: String, size: Float = 16f, color: Int = Color.LTGRAY) = TextView(this).apply {
        text = value; textSize = size; setTextColor(color)
        setPadding(0, dp(8), 0, dp(8))
    }
    private fun button(title: Int, action: () -> Unit) = Button(this).apply {
        setText(title); isAllCaps = false; setTextColor(Color.WHITE)
        setOnClickListener { action() }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val scroll = ScrollView(this).apply { setBackgroundColor(Color.rgb(11, 12, 15)); isFillViewport = true }
        val body = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL; setPadding(dp(24), dp(20), dp(24), dp(24))
        }
        scroll.addView(body)
        // Insets keep content clear of cutouts, gesture navigation and Android 15 edge-to-edge.
        scroll.setOnApplyWindowInsetsListener { v, insets ->
            if (Build.VERSION.SDK_INT >= 30) {
                val bars = insets.getInsets(android.view.WindowInsets.Type.systemBars() or android.view.WindowInsets.Type.displayCutout())
                v.setPadding(bars.left, bars.top, bars.right, bars.bottom)
            } else {
                @Suppress("DEPRECATION")
                v.setPadding(insets.systemWindowInsetLeft, insets.systemWindowInsetTop, insets.systemWindowInsetRight, insets.systemWindowInsetBottom)
            }
            insets
        }
        body.addView(label("FORMULA 1  /  30TH ANNIVERSARY", 11f, orange).apply { letterSpacing = 0.14f })
        body.addView(label("TAG Heuer\nMcLaren", 36f, Color.WHITE).apply { typeface = Typeface.DEFAULT_BOLD })
        body.addView(label(getString(R.string.subtitle), 14f))
        val preview = DialPreview(this)
        body.addView(preview, LinearLayout.LayoutParams(-1, dp(330)))
        body.addView(label(getString(R.string.preview_style), 14f, Color.WHITE))
        val swatches = LinearLayout(this).apply { gravity = Gravity.CENTER }
        listOf(orange, Color.rgb(95, 191, 255), Color.rgb(216, 222, 231)).forEach { color ->
            val swatch = Button(this).apply {
                text = "●"; textSize = 28f; setTextColor(color)
                contentDescription = String.format("#%06X", color and 0xFFFFFF)
                setOnClickListener { preview.accent = color; preview.invalidate() }
            }
            swatches.addView(swatch, LinearLayout.LayoutParams(0, dp(56), 1f))
        }
        body.addView(swatches)
        body.addView(Switch(this).apply {
            setText(R.string.ambient); setTextColor(Color.WHITE)
            setOnCheckedChangeListener { _, checked -> preview.ambient = checked; preview.invalidate() }
        })
        body.addView(label(getString(R.string.compatibility), 14f))
        body.addView(button(R.string.open_store) { openStore() })
        body.addView(label(getString(R.string.guide), 24f, Color.WHITE).apply { typeface = Typeface.DEFAULT_BOLD })
        listOf(R.string.step_pair, R.string.step_install, R.string.step_select, R.string.troubleshoot).forEachIndexed { index, id ->
            val card = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL; setPadding(dp(16), dp(10), dp(16), dp(10))
                background = GradientDrawable().apply { setColor(Color.rgb(24, 26, 31)); cornerRadius = dp(16).toFloat() }
            }
            card.addView(label(if (index < 3) "0${index + 1}" else "?", 14f, orange))
            card.addView(label(getString(id), 16f, Color.WHITE))
            body.addView(card, LinearLayout.LayoutParams(-1, -2).apply { bottomMargin = dp(12) })
        }
        body.addView(button(R.string.language) { chooseLanguage() })
        body.addView(label(getString(R.string.privacy), 13f))
        body.addView(label(getString(R.string.disclaimer), 12f))
        setContentView(scroll)
        scroll.requestApplyInsets()
    }

    private fun openStore() {
        val uri = Uri.parse("https://play.google.com/store/apps/details?id=com.deploydulupulangnanti.tagheuermclarenwf")
        try { startActivity(Intent(Intent.ACTION_VIEW, uri)) }
        catch (_: android.content.ActivityNotFoundException) {
            AlertDialog.Builder(this).setMessage(R.string.no_browser).setPositiveButton(android.R.string.ok, null).show()
        }
    }

    private fun chooseLanguage() {
        val tags = mutableListOf("")
        val parser = resources.getXml(R.xml.locales_config)
        while (parser.eventType != org.xmlpull.v1.XmlPullParser.END_DOCUMENT) {
            if (parser.eventType == org.xmlpull.v1.XmlPullParser.START_TAG && parser.name == "locale") {
                tags.add(parser.getAttributeValue("http://schemas.android.com/apk/res/android", "name"))
            }
            parser.next()
        }
        parser.close()
        val names = tags.map { if (it.isEmpty()) getString(R.string.system_language) else Locale.forLanguageTag(it).let { l -> l.getDisplayName(l) } }
        AlertDialog.Builder(this).setTitle(R.string.language).setItems(names.toTypedArray()) { _, position ->
            val tag = tags[position]
            getSharedPreferences("settings", MODE_PRIVATE).edit().putString("language", tag).apply()
            if (Build.VERSION.SDK_INT >= 33) getSystemService(LocaleManager::class.java).applicationLocales = LocaleList.forLanguageTags(tag)
            recreate()
        }.show()
    }
}
