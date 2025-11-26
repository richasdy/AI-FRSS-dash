Jadi sistem ini punya backend yang kerjanya berat-berat kayak ngolah video dan deteksi objek, terus ada frontend sederhana buat nampilin hasilnya. Backend-nya bakal capture frame dari video stream, terus dioleh pakai AI (YOLOv8) buat nyari manusia. Kalau ketemu, sistem bakal nyimpen foto orangnya (di-crop) dan kirim alert ke dashboard kita.

Fitur-fitur utamanya:
- Live streaming video yang udah ada kotak hijaunya kalau ada orang kedeteksi.
- Notifikasi langsung (live alerts) yang muncul di dashboard tanpa perlu refresh halaman.
- Ada logika biar gak spam notifikasi kalau orangnya sama terus (deduplication).
- Udah dioptimasi buat jalan di Apple Silicon (Mac M1/M2/M3) pakai MPS, tapi di laptop lain juga harusnya aman.

## Persiapan Dulu

Sebelum coba jalanin, pastiin di laptop udah ada Python versi 3.11. Proyek ini butuh beberapa library kayak FastAPI, OpenCV, sama Ultralytics YOLO.

## Cara Install

1.  **Install Library yang Dibutuhkan**

    Masuk dulu ke folder proyeknya lewat terminal, terus jalanin perintah ini buat install semua dependensinya:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Cek Model AI**

    Pastiin file model YOLOv8 ada di folder `yolo_models/People_yolov8s_trained.pt`. Kalau kalian mau ganti model atau nama filenya beda, bisa diatur di `app/core/config.py`.

## Pengaturan (Config)

Semua pengaturan penting ada di file `app/core/config.py`. Kalian bisa ubah-ubah kayak:

-   `VIDEO_SOURCE`: Link stream video MJPEG dari kameranya.
-   `CONFIDENCE_THRESHOLD`: Batas minimal keyakinan si AI buat bilang itu orang. Kalau terlalu rendah nanti salah deteksi, kalau ketinggian nanti orangnya gak ke-detect.
-   `MAX_FPS`: Buat batesin kecepatan proses biar laptop gak panas banget.

## Cara Jalanin Server

Buat nyalain server backend-nya, ketik perintah ini di terminal:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Kalau server udah jalan dan gak ada error, buka browser (Chrome atau Safari) terus akses:

http://localhost:8000

## Tampilan Dashboard

Di dashboard-nya nanti bakal kelihatan:

-   **Processed Stream (AI)**: Video yang udah diproses sama AI, ada kotak hijau di sekeliling orang yang terdeteksi.
-   **Raw Stream (Source)**: Video asli dari kamera tanpa editan apa-apa.
-   **Live Alerts**: Daftar notifikasi di sebelah kanan. Tiap kali ada orang lewat, bakal muncul kartu baru yang ada jam kejadian sama foto orangnya.

Pas dashboard baru dibuka, dia juga bakal muat foto-foto deteksi yang udah kesimpen sebelumnya, jadi kita bisa lihat history-nya.

## Struktur Folder Proyek

-   `main.py`: Ini file utamanya. Dia yang ngatur API, koneksi WebSocket, sama tugas-tugas background.
-   `app/services/`: Isinya logika-logika beratnya.
    -   `detector.py`: Buat urusan load model AI dan deteksi frame.
    -   `stream_capture.py`: Buat nyambungin ke video stream dan ambil gambar.
    -   `image_processor.py`: Buat nyimpen hasil crop dan ngecek gambar duplikat biar gak spam.
-   `app/core/config.py`: Tempat nyimpen settingan.
-   `app/crops/`: Folder tempat nyimpen foto-foto orang yang ketangkap kamera.
-   `index.html`: Tampilan web dashboard-nya.

## Kalau Ada Masalah (Troubleshooting)

Kalau live alerts-nya gak muncul:
-   Coba cek terminal, ada error apa gak.
-   Pastiin link videonya bener dan bisa diakses.
-   Coba turunin `CONFIDENCE_THRESHOLD` di config, siapa tau AI-nya kurang yakin itu orang.

Kalau videonya patah-patah, biasanya karena koneksi internet ke kameranya kurang stabil atau emang stream-nya berat. Sistem udah dibuat biar tetep jalan walaupun koneksi agak lemot, tapi ya tetep ngaruh ke tampilannya.
