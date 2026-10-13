# Menghubungkan dan memasang watch face

## Instalasi pengguna dari Google Play

1. Cek **Wear OS 4 atau lebih baru**, bukan hanya merek/model jam. APK ini tidak mendukung Apple Watch, Garmin, Amazfit, Huawei atau Tizen.
2. Charge jam dan hubungkan internet. Pasangkan jam lewat aplikasi resmi produsen (misalnya Galaxy Wearable, Google Pixel Watch, atau aplikasi produsen yang sesuai). Project ini tidak menggantikan proses pairing produsen.
3. Gunakan akun Google yang sama di ponsel dan jam. Buka Play Store **di jam**, cari **TAG Heuer McLaren 30th**, lalu beli/instal sesuai listing setelah dipublikasikan.
4. Alternatif: buka listing watch face dari ponsel, pilih perangkat jam yang ditawarkan Google Play. Jika jam tidak ditawarkan, instal langsung melalui Play Store jam. Instalasi aplikasi panduan di ponsel saja tidak memasang watch face.
5. Tekan lama tampilan jam saat ini → Tambah watch face → pilih **TAG Heuer McLaren 30th**. Nama menu dapat berbeda menurut produsen.
6. Buka Edit/Customize dan pilih warna aksen. Warna pada preview ponsel tidak disinkronkan ke jam.
7. Always-on Display mengikuti pengaturan sistem jam. Project menampilkan jarum dan waktu digital redup; detik dan dial dekoratif disembunyikan di ambient.

Tautan listing baru berfungsi setelah aplikasi dipublikasikan, tersedia di negara pengguna, serta kompatibel dengan perangkat. Pembelian tidak dilakukan melalui aplikasi panduan.

## Troubleshooting

- Tidak muncul di daftar: pastikan modul `wear` sudah dipasang di jam, OS minimum sesuai, dan cari melalui Tambah watch face.
- Tidak ditemukan di Play: listing mungkin belum dirilis, negara/perangkat tidak diaktifkan atau perangkat belum memenuhi persyaratan.
- Setelah install: tunggu unduhan selesai dan restart jam bila perlu.
- Tidak bisa pairing: gunakan bantuan produsen jam; aplikasi ini tidak memiliki akses Bluetooth atau pairing otomatis.

## Instalasi developer lewat ADB Wi-Fi

Aktifkan Developer options di jam (tap Build number beberapa kali), lalu Wireless debugging. Ponsel/komputer dan jam harus berada pada jaringan yang sama. Catat alamat serta port pairing dan port koneksi dari jam; **keduanya dapat berbeda**.

```powershell
adb pair IP_JAM:PORT_PAIRING
# Masukkan kode pairing yang ditampilkan di jam.
adb connect IP_JAM:PORT_KONEKSI
adb devices
adb -s IP_JAM:PORT_KONEKSI install -r wear/build/outputs/apk/debug/wear-debug.apk
```

Pilih watch face melalui UI jam. Untuk ponsel/emulator Android:

```powershell
adb -s SERIAL_PONSEL install -r companion/build/outputs/apk/debug/companion-debug.apk
adb -s SERIAL_PONSEL shell am start -n com.deploydulupulangnanti.tagheuermclarenwf/com.deploydulupulangnanti.tagheuermclarenwf.companion.MainActivity
```

Gunakan APK untuk ADB, bukan AAB. Instalasi Play adalah jalur pengguna akhir. Matikan Wireless debugging setelah pengujian. Jangan campurkan APK debug dan release dengan signing key berbeda; uninstall versi pengujian lebih dahulu jika muncul konflik signature.
