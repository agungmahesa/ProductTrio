# SOP-GA-01 Kontrol Area

| Kolom | Isi |
|---|---|
| Perusahaan | PT Acme Tea Indonesia |
| No. SOP | SOP-GA-01 |
| Judul | Kontrol Area |
| Departemen / pemilik proses | General Affair (GA) / Kepala GA |
| Versi | 1.0 |
| Status | Draft |
| Tanggal berlaku | TBD |
| Review berikutnya | 2027-11 |
| Disusun oleh | Staf GA |
| Disetujui oleh | TBD - Kepala GA |

## 1. Tujuan
Memastikan seluruh area kantor dan unit PT Acme Tea Indonesia selalu bersih, aman dan berfungsi baik, dengan temuan yang ditindaklanjuti dalam batas waktu yang jelas.

## 2. Ruang Lingkup
**Berlaku untuk:** pemeriksaan harian area kantor dan unit (lobi, ruang kerja, toilet, pantry, gudang, area luar), mulai dari pemeriksaan sampai tindak lanjut temuan selesai.
**Tidak mencakup:** perawatan berkala mesin dan gedung (SOP-ENG-01), pengadaan perlengkapan kebersihan (SOP-GA-03).

## 3. Definisi
| Istilah | Arti |
|---|---|
| CS | Cleaning Service, petugas kebersihan (internal atau vendor) |
| WO | Work Order, permintaan perbaikan tertulis ke Tim Engineering |
| Temuan | Kondisi yang tidak memenuhi standar di checklist F-01 |

## 4. Referensi
- F-01 Checklist Kontrol Area
- F-02 Work Order
- Kebijakan Kebersihan dan Keselamatan Kerja perusahaan
- SOP-ENG-01 Perawatan Berkala

## 5. Peran dan Tanggung Jawab
| Peran | Tanggung jawab dalam SOP ini |
|---|---|
| Staf GA | Melakukan kontrol area, mencatat temuan, meminta tindak lanjut, memverifikasi hasil |
| Cleaning Service | Membersihkan ulang area sesuai temuan |
| Tim Engineering | Memperbaiki temuan teknis sesuai WO |
| Kepala GA | Pemilik SOP; memeriksa checklist harian dan menerima eskalasi |

## 6. Prosedur
Pemicu: jadwal kontrol pukul 08:00 dan 14:00 setiap hari kerja. Hasil: semua temuan selesai ditindaklanjuti dan checklist diarsipkan.

| No | Aktivitas | Tanggung Jawab | Input / alat | Dokumen | Waktu / SLA | Catatan dan kontrol | BPMN |
|---|---|---|---|---|---|---|---|
| 1 | Mulai kontrol area sesuai jadwal dengan membawa checklist F-01 dan ponsel untuk foto. | Staf GA | F-01 | - | 08:00 dan 14:00 | Jika berhalangan, Kepala GA menunjuk pengganti. | E-01 |
| 2 | Periksa setiap area sesuai urutan di F-01: lantai, toilet, pantry, tempat sampah, AC, lampu dan kondisi bangunan. | Staf GA | F-01 | - | 30 menit | Gunakan standar di kolom "Standar" F-01, bukan perkiraan. | T-01 |
| 3 | Catat hasil setiap item (OK / Tidak OK) dan foto setiap temuan. | Staf GA | Ponsel | F-01 | Saat pemeriksaan | **[Control]** Setiap "Tidak OK" wajib punya foto dan lokasi. | T-02 |
| 4 | Tentukan jenis temuan. Kebersihan: lanjut ke 5. Teknis (AC, lampu, bangunan): lanjut ke 8. Keduanya: jalankan 5 dan 8. Tidak ada temuan: lanjut ke 11. | Staf GA | F-01 | - | - | - | G-01 |
| 5 | Minta supervisor CS membersihkan ulang area, sebutkan lokasi dan temuannya. | Staf GA | F-01 | F-01 kolom tindak lanjut | Dalam 15 menit | - | T-03 |
| 6 | Bersihkan ulang area sesuai temuan, lalu laporkan ke Staf GA. | Cleaning Service | Peralatan kebersihan | - | Dalam 60 menit | - | T-04 |
| 7 | Periksa ulang area dan tandai "Selesai" di F-01. | Staf GA | F-01 | F-01 | Setelah laporan CS | Jika masih belum sesuai standar, ulangi langkah 5 satu kali, lalu eskalasi ke Kepala GA. | T-05 |
| 8 | Buat Work Order (F-02), tandatangani, dan serahkan ke Tim Engineering. | Staf GA | F-02 | F-02 | Hari yang sama | **[Control]** Satu temuan teknis = satu WO bernomor. | T-06 |
| 9 | Perbaiki temuan sesuai WO, lalu isi tindakan dan waktu selesai di F-02. | Tim Engineering | F-02 | F-02 | Darurat 4 jam; normal 3 hari kerja | Prioritas darurat: kebocoran, listrik, risiko keselamatan. | T-07 |
| 10 | Periksa hasil perbaikan, lalu tutup WO dengan tanda tangan. | Staf GA | F-02 | F-02 ditutup | Hari kerja yang sama dengan laporan selesai | - | T-08 |
| 11 | Serahkan F-01 yang sudah lengkap ke Kepala GA dan arsipkan. | Staf GA | F-01 | F-01 diarsipkan | Setiap hari 16:00 | **[Control]** Kepala GA memaraf checklist harian. | G-02, T-09, E-10 |

## 7. Diagram Alir
Diagram BPMN 2.0: [flow.html](flow.html) · [flow.bpmn](flow.bpmn).

## 8. Pengecualian dan Eskalasi
| Situasi | Tindakan | Oleh | Batas waktu | Eskalasi ke |
|---|---|---|---|---|
| Area masih belum bersih setelah dibersihkan ulang | Eskalasi dengan foto | Staf GA | Hari yang sama | Kepala GA |
| WO melewati SLA | Hubungi Chief Engineering | Staf GA | Saat SLA lewat | Kepala GA |
| Temuan berisiko keselamatan (kabel terbuka, lantai licin, kebocoran) | Pasang tanda bahaya dan tutup area, lalu buat WO darurat | Staf GA | Segera | Kepala GA dan Chief Engineering |

## 9. Catatan dan Formulir
| Formulir / catatan | Diisi oleh | Disimpan di | Masa simpan |
|---|---|---|---|
| [F-01 Checklist Kontrol Area](forms/F-01-checklist-kontrol-area.md) | Staf GA | Map GA-01 | 1 tahun |
| [F-02 Work Order](forms/F-02-work-order.md) | Staf GA dan Tim Engineering | Map GA-02 | 2 tahun |

## 10. Kontrol dan KPI
| Kontrol / KPI | Target | Diperiksa oleh | Frekuensi |
|---|---|---|---|
| Checklist harian lengkap dan diparaf | 100% | Kepala GA | Harian |
| Temuan kebersihan selesai dalam 60 menit | ≥ 95% | Kepala GA | Mingguan |
| WO selesai sesuai SLA | ≥ 90% | Kepala GA | Bulanan |

## 11. Pelatihan dan Pengesahan
| Nama | Peran | Dilatih oleh | Tanggal | Tanda tangan |
|---|---|---|---|---|
| | | | | |

## 12. Riwayat Revisi
| Versi | Tanggal | Perubahan | Oleh |
|---|---|---|---|
| 1.0 | 2026-11-08 | Ditulis ulang: kriteria terukur, SLA, jalur teknis via WO, eskalasi | Staf GA |

*PT Acme Tea Indonesia dan seluruh data dalam contoh ini fiktif.*
