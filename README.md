Searcher Journal 
Instrumen otomatisasi berbasis Python untuk akuisisi literatur ilmiah secara masif. Alat ini mengintegrasikan protokol Multi-Index Discovery untuk mengekstraksi dokumen PDF dari berbagai basis data akademik global.

Features
🔍 Multi-Index Search: Melakukan kueri simultan ke Google Scholar, Scopus, DOAJ, SINTA, hingga domain .edu dan .ac.id.

🔄 Smart Pagination: Logika navigasi otomatis yang mampu menembus limitasi halaman mesin pencari untuk mencapai kuota unduhan yang tinggi.

📊 Audit Manifest: Fitur pemantauan real-time untuk memvalidasi jumlah tautan yang ditemukan dibandingkan dengan data yang berhasil diarsip.

📦 Bulk Archiving: Mengotomatisasi proses kompresi seluruh dokumen yang diakuisisi ke dalam format .zip siap pakai.

🛡️ Resilient Acquisition: Dilengkapi dengan mekanisme timeout dan penanganan CAPTCHA manual untuk menjaga kelangsungan proses crawling.

Prerequisites
Python: Proyek ini memerlukan Python 3.11 atau versi terbaru sebagai runtime utama.

Google Chrome: Diperlukan untuk menjalankan Selenium engine.

Driver Management: Menggunakan webdriver-manager sehingga Anda tidak perlu mengunduh ChromeDriver secara manual.

Installation
1. Clone the repository:
Bash
git clone https://github.com/andreiswahyudi/searcher-jurnal.git
cd searcher-jurnal
2. Install dependencies:
Bash
pip install streamlit selenium webdriver-manager requests
Usage
Run the application:
Bash
streamlit run pdf.py
Prosedur Operasional:

Masukkan Target Keyword riset Anda.

Tentukan Quota dokumen yang ingin diambil.

Pilih Database Protocol (Disarankan: ALL INDEX untuk populasi data maksimal).

Klik PROCESS dan pantau jendela browser otomatis yang muncul.

Gunakan tombol Download .ZIP Archive setelah status menunjukkan COMPLETE.

Tips Pengembang:
Jika muncul verifikasi robot (CAPTCHA), cukup selesaikan secara manual pada jendela browser yang terbuka, dan skrip akan melanjutkan tugasnya secara otomatis.
