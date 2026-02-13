# Judul: Fitur Sistem Deteksi Orang Real-time dengan Live Alerts & Dashboard

## Deskripsi
PR buat fitur deteksi orang secara real-time dari kamera CCTV. Jadi intinya sistem ini bakal baca stream video, terus pakai AI (YOLOv8) buat nyari orang. Kalau ketemu, dia bakal kirim notifikasi ke dashboard web secara langsung.

Tujuannya biar bisa monitoring siapa aja yang lewat, terus foto orangnya bakal dicrop dan disimpen otomatis. Di dashboard juga ada live video yang udah dikasih kotak ijo (bounding box) biar jelas mana yang kedeteksi.

## Perubahan Utama

### Bagian Backend (FastAPI + Python)
- **Integrasi YOLOv8**: Nambahin service `PeopleDetector` yang pakai `ultralytics`. Udah support akselerasi Mac (MPS) jadi ngebut.
- **Stream Capture**: Bikin `StreamCapture` yang pakai OpenCV (`cv2`) buat nangkep video MJPEG. Udah dites biar gak ngelag walaupun FPS kameranya rendah.
- **Image Processing**: Nambahin logika biar gak spam notifikasi kalau orangnya sama terus (pakai dHash buat cek kemiripan).
- **WebSocket Service**: Bikin endpoint WebSocket `/ws/people-detection` biar bisa broadcast notifikasi ke frontend tanpa refresh.
- **Video Streaming**: Nambahin endpoint `/video_feed` yang alurnya asinkron (async) biar video jalan terus tanpa bikin server macet.
- **Static Files**: Ngebuka akses folder `/crops` biar foto hasil deteksi bisa dilihat di web.

### Bagian Frontend (HTML/JS)
- **Dashboard Keren**: Bikin halaman `index.html` yang isinya:
  - **Processed Stream**: Video live yang udah ada kotak ijo dari AI.
  - **Raw Stream**: Video asli dari kamera.
  - **Live Alerts**: Daftar notifikasi real-time yang ada jam sama fotonya.
- **Load History**: Pas web dibuka, dia langsung ngambil foto-foto yang udah ada sebelumnya, jadi gak kosong melompong.
- **WebSocket**: Udah ada logika auto-reconnect kalau internet putus.

## Detail Teknis
- **Concurrency**: Video generator-nya dibikin `async` biar event loop gak keblokir pas lagi streaming video. Ini penting banget biar WebSocket tetep lancar.
- **Optimasi**: Threshold deteksi diturunin jadi `0.1` soalnya kadang kameranya agak jauh/burem, jadi biar lebih sensitif.
- **Config**: Semua settingan ditaruh di `app/core/config.py` biar gampang diubah.

## Cara Ngetesnya
1. Install dulu library-nya: `pip install -r requirements.txt`
2. Jalanin servernya: `uvicorn main:app --host 0.0.0.0 --port 8000`
3. Buka browser ke: http://localhost:8000
4. Cek videonya jalan apa nggak (kiri & kanan).
5. Tungguin bentar sampai ada orang lewat, harusnya muncul notif di panel kanan.

## Checklist
- [x] Kode aman, udah dicoba jalan lancar.
- [x] Deteksi orang & alert udah dites dan work.
- [x] UI nampilin video & alert dengan bener.
- [x] Dokumentasi (README.md)
