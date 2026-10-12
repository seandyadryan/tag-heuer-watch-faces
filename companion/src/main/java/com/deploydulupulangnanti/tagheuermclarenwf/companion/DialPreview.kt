package com.deploydulupulangnanti.tagheuermclarenwf.companion

import android.content.Context
import android.graphics.*
import android.view.View
import java.time.ZonedDateTime
import java.time.format.DateTimeFormatter
import java.util.Locale

/** Phone preview only. The wearable uses the system WFF renderer and system clock. */
class DialPreview(context: Context) : View(context) {
    var accent = Color.rgb(255, 135, 0)
    var ambient = false
    private val dial = BitmapFactory.decodeResource(resources, R.drawable.dial)
    private val mask = BitmapFactory.decodeResource(resources, R.drawable.accent)
    private val hour = BitmapFactory.decodeResource(resources, R.drawable.hour)
    private val minute = BitmapFactory.decodeResource(resources, R.drawable.minute)
    private val second = BitmapFactory.decodeResource(resources, R.drawable.second)
    private val paint = Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
    private val ticker = object : Runnable {
        override fun run() { invalidate(); postDelayed(this, 1000L) }
    }
    init { importantForAccessibility = IMPORTANT_FOR_ACCESSIBILITY_NO }
    override fun onAttachedToWindow() { super.onAttachedToWindow(); post(ticker) }
    override fun onDetachedFromWindow() { removeCallbacks(ticker); super.onDetachedFromWindow() }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val now = ZonedDateTime.now()
        val scale = minOf(width, height) / 450f
        canvas.save()
        canvas.translate((width - 450 * scale) / 2, (height - 450 * scale) / 2)
        canvas.scale(scale, scale)
        paint.colorFilter = null
        if (!ambient) {
            canvas.drawBitmap(dial, null, RectF(0f, 0f, 450f, 450f), paint)
            paint.colorFilter = PorterDuffColorFilter(accent, PorterDuff.Mode.SRC_IN)
            canvas.drawBitmap(mask, null, RectF(0f, 0f, 450f, 450f), paint)
            paint.colorFilter = null
        }
        fun hand(bitmap: Bitmap, angle: Float, rect: RectF) {
            canvas.save(); canvas.rotate(angle, 225f, 225f)
            canvas.drawBitmap(bitmap, null, rect, paint); canvas.restore()
        }
        paint.alpha = if (ambient) 150 else 255
        hand(hour, (now.hour % 12) * 30f + now.minute * 0.5f, RectF(214f, 110f, 236f, 245f))
        hand(minute, now.minute * 6f + now.second * 0.1f, RectF(218f, 56f, 232f, 246f))
        paint.alpha = 255
        if (!ambient) {
            paint.colorFilter = PorterDuffColorFilter(accent, PorterDuff.Mode.SRC_IN)
            hand(second, now.second * 6f, RectF(222f, 37f, 228f, 252f))
            paint.colorFilter = null
        }
        paint.color = if (ambient) Color.GRAY else accent
        canvas.drawCircle(225f, 225f, 7f, paint)
        paint.typeface = Typeface.create("sans-serif", Typeface.BOLD)
        paint.textAlign = Paint.Align.CENTER; paint.textSize = 26f; paint.color = if (ambient) Color.GRAY else Color.WHITE
        val locale = resources.configuration.locales[0] ?: Locale.getDefault()
        val format = if (android.text.format.DateFormat.is24HourFormat(context)) "HH:mm" else "hh:mm"
        canvas.drawText(now.format(DateTimeFormatter.ofPattern(format, locale)), 225f, 320f, paint)
        canvas.restore()
    }
}
