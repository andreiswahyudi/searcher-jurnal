Searcher Journal: Research Data Acquisition Engine
Project Framework: Open-Source Systematic Literature Review (SLR) Tool

Version: 1.0.0-Stable

Lead Developer: AndreXyz

1. Executive Summary
Searcher Journal adalah instrumen berbasis Python yang dirancang untuk mengotomatisasi proses pengumpulan literatur ilmiah dari berbagai indeks database global. Dikembangkan dengan prinsip akurasi data dan kecepatan akuisisi, alat ini memungkinkan peneliti untuk melakukan web-crawling pada domain akademik guna mengunduh dokumen PDF secara masif berdasarkan kata kunci spesifik.

2. Methodology & Features
Sistem ini mengintegrasikan beberapa protokol pencarian tingkat tinggi untuk memastikan integritas data:

Multi-Index Discovery: Integrasi kueri otomatis ke mesin pencari dengan filter khusus untuk domain .edu, .ac.id, serta indeks prestisius seperti Scopus, Google Scholar, dan DOAJ.

Pagination Logic: Menggunakan teknik offset-looping untuk melampaui batasan hasil pencarian standar, memungkinkan penemuan hingga ratusan dokumen per sesi.

Real-time Audit Manifest: Fitur notifikasi yang menghitung populasi tautan (total temuan) dibandingkan dengan sampel yang berhasil diarsip secara fisik.

Unlimited Acquisition: Menghilangkan ambang batas kuota konvensional untuk mendukung kebutuhan riset berskala besar.

Encapsulated Interface: Antarmuka berbasis Streamlit dengan estetika monochrome-industrial untuk fokus maksimal pada data.

3. Technical Specifications
Proyek ini dibangun menggunakan stack teknologi berikut:

Engine: Python 3.11+

Automation: Selenium WebDriver (Chrome Engine)

UI Framework: Streamlit

Data Handling: Requests, Zipfile, & IO Buffer

Font Architecture: Courier Prime (Monospace)
