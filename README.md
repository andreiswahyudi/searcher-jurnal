Searcher Journal: Research Data Acquisition Engine
Project Framework: Open-Source Systematic Literature Review (SLR) Tool

Version: 1.0

🛠️ Panduan Operasional: Searcher Journal
Skrip ini dirancang untuk melakukan akuisisi literatur digital secara otomatis dengan efisiensi tinggi. Pastikan seluruh dependensi telah terpenuhi sebelum menjalankan mesin ini.

1. Spesifikasi Persyaratan
Runtime: Python 3.11 atau lebih tinggi.

Web Engine: Google Chrome Browser (Versi terbaru).

Driver: Selenium WebDriver (Dikelola otomatis oleh webdriver-manager).

2. Instalasi Dependensi
Jalankan perintah berikut pada terminal atau Command Prompt untuk menginstal library yang diperlukan:

Bash
pip install streamlit selenium webdriver-manager requests
3. Eksekusi Program
Gunakan perintah Streamlit untuk mengaktifkan antarmuka grafis:

Bash
streamlit run pdf.py
4. Alur Kerja Akuisisi
Untuk mendapatkan hasil maksimal (target >100 dokumen), ikuti langkah-langkah berikut:

Keyword Definition: Masukkan kata kunci spesifik. Gunakan operator pencarian jika perlu (contoh: "Machine Learning" untuk frase eksak).

Quota Setting: Masukkan jumlah target dokumen. Sistem menggunakan Pagination Logic yang akan memindai halaman demi halaman Google Search secara otomatis hingga kuota terpenuhi.

Protocol Selection: Pilih indeks basis data yang diinginkan. Opsi ALL INDEX disarankan untuk cakupan riset yang luas (mencakup Scopus, Google Scholar, dan domain akademik).

Monitoring & Audit: Pantau panel Audit Manifest. Panel ini menampilkan total tautan PDF yang terdeteksi dibandingkan dengan jumlah yang berhasil diunduh.

5. Penanganan Kendala (Troubleshooting)
Manual Captcha: Jika sistem terdeteksi sebagai bot oleh mesin pencari, jendela browser otomatis akan menampilkan Captcha. Selesaikan Captcha tersebut secara manual, dan skrip akan melanjutkan proses pengunduhan secara otomatis.

Timeout: Jika koneksi tidak stabil, skrip telah dilengkapi dengan fitur retry dan timeout selama 20 detik per dokumen untuk menjaga integritas data.
