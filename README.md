# 🤖 Discord Project Manager Bot

Bot Discord berbasis Python untuk **mengelola proyek pengguna** langsung melalui chat Discord.  
Bot ini memungkinkan setiap user menyimpan proyek, melihat daftar proyek, memperbarui informasi proyek, menambahkan skill, dan menghapus proyek dengan perintah sederhana.

---

## ✨ Fitur Utama

- 📌 Menambahkan proyek baru
- 📋 Melihat semua proyek milik user
- ✏️ Mengupdate data proyek (nama, deskripsi, link, status)
- 🧠 Menambahkan skill ke proyek
- 🗑️ Menghapus proyek
- 💾 Data disimpan ke database (SQLite)

---

## 🧾 Daftar Command

| Command | Fungsi |
|------|------|
| `!start` | Menampilkan pesan sambutan dan bantuan |
| `!info` | Menampilkan daftar command |
| `!new_project` | Menambahkan proyek baru |
| `!projects` | Menampilkan semua proyek user |
| `!update_projects` | Mengupdate data proyek |
| `!skills` | Menambahkan skill ke proyek |
| `!delete` | Menghapus proyek |

---

## 🧠 Cara Kerja Bot

1. User mengetik command
2. Bot akan meminta input melalui chat
3. Bot memvalidasi input user
4. Data disimpan / diperbarui di database
5. Bot mengirimkan konfirmasi

Semua input hanya dibaca dari **user dan channel yang sama** untuk keamanan.

---

## 🛠️ Teknologi yang Digunakan

- Python 3
- discord.py
- SQLite
- Git & GitHub

---

## 📂 Struktur Project

```bash
project/
│
├── bot.py          # File utama bot
├── logic.py        # DB_Manager (query database)
├── config.py       # TOKEN dan DATABASE
├── database.db     # Database SQLite
├── README.md       # Dokumentasi project
