# Persiapan penjualan Google Play

Project ini menghasilkan file instalasi dan signed AAB; belum menjadi aplikasi yang disetujui Google Play.

1. Dapatkan izin tertulis untuk nama/desain/merek TAG Heuer dan McLaren. Project ini independen. Tulisan disclaimer tidak menggantikan lisensi. [Kebijakan IP Google Play](https://support.google.com/googleplay/android-developer/answer/9888072).
2. Pilih akun developer dan verifikasi identitas. Daftarkan package watch face `com.deploydulupulangnanti.tagheuermclarenwf`; listing pendamping opsional menggunakan suffix `.companion`.
3. Backup keystore offline. Alias `tag-heuer-watch-faces`. Gunakan Play App Signing dan ikuti pilihan upload key/app signing key di Console. Jangan menghapus atau meregenerasi key yang sudah dipakai tanpa proses rotasi resmi.
4. Jalankan CI, release workflow, validator WFF dan evaluator memori. Uji pada jam Wear OS 4 minimum serta versi baru, layar kecil/besar, perubahan zona waktu, format 12/24, ambient, warna, penggunaan baterai dan instalasi melalui track Play.
5. Lengkapi listing berbayar, kategori watch face, negara distribusi, harga dan pajak. Ketersediaan Google Play/pembayaran berbeda menurut negara; jangan menjanjikan semua negara/perangkat.
6. Buat screenshot aktual di jam, icon/feature graphic sesuai spesifikasi Console, deskripsi yang akurat, email support dan URL privacy policy publik. Preview dari source bukan screenshot pengujian perangkat.
7. Lengkapi Data safety, rating konten, deklarasi iklan (tidak ada), dan deklarasi lainnya berdasarkan APK final. File privacy policy adalah draft; identitas/contact developer belum tersedia.
8. Upload **wear-release.aab** ke listing Wear OS. Pendamping Kotlin dibuat sebagai listing terpisah bila diterbitkan. Tautan companion ke Play baru berfungsi setelah listing watch face tersedia.
9. Selesaikan internal/closed testing serta persyaratan akun yang ditampilkan Console sebelum production. Terjemahan perlu review penutur asli dan listing perlu terjemahan terpisah.
10. Naikkan `versionCode` pada setiap upload berikutnya. Jangan mengganti `applicationId` setelah publikasi.

Tidak ada auto-publish atau kredensial Play Console di repository. GitHub Actions hanya membuat artifact untuk diunduh. Persyaratan Google dapat berubah; cek [kualitas aplikasi Wear](https://developer.android.com/docs/quality-guidelines/wear-app-quality) dan Console saat rilis.
