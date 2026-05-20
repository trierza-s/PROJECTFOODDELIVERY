import os
from models.user import User

def load_data(self):
    """
    Fungsi untuk membaca data user dari file TXT dan memuatnya ke dalam dictionary sistem.
    """
    # Inisialisasi dictionary kosong agar tidak terjadi error 'NoneType'
    self.users = {}
    
    # Cek apakah folder 'data' dan filenya ada. Jika tidak, keluar dari fungsi.
    if not os.path.exists("data/data_user.txt"):
        return
        
    with open("data/data_user.txt", "r") as f:
        # Variabel sementara untuk menampung data sebelum dijadikan objek User
        uname, pwd, saldo = None, None, 0
        # Default sisa kuota promo jika tidak ditemukan di file
        s_hemat, s_puas, s_enak = 2, 3, 5 
        
        for line in f:
            line = line.strip() # Menghapus spasi/newline di awal dan akhir baris
            
            # Jika baris kosong atau berisi garis pemisah '---', tandanya satu blok data user selesai
            if not line or line.startswith("-"):
                if uname:
                    # Buat objek User baru dengan data yang sudah terkumpul
                    u = User(uname, pwd, saldo)
                    # Hitung balik penggunaan promo (Usage = Kuota Maksimal - Sisa di File)
                    u.promo_usage = {
                        "HEMAT10": 2 - s_hemat, 
                        "MAKANPUAS": 3 - s_puas, 
                        "MakanEnak": 5 - s_enak
                    }
                    # Simpan objek user ke dalam dictionary dengan key berupa username
                    self.users[uname] = u
                    
                    # Reset variabel untuk membaca user berikutnya di loop selanjutnya
                    uname, pwd, saldo, s_hemat, s_puas, s_enak = None, None, 0, 2, 3, 5
                continue
            
            # Proses parsing baris berdasarkan teks label sebelum tanda titik dua (:)
            if "Nama" in line: 
                uname = line.split(":")[1].strip()
            elif "Password" in line: 
                pwd = line.split(":")[1].strip()
            # Konversi teks saldo ke integer
            elif "Saldo" in line: 
                saldo = int(line.split(":")[1].strip()) 
            elif "Sisa Hemat" in line: 
                s_hemat = int(line.split(":")[1].strip())
            elif "Sisa Puas" in line: 
                s_puas = int(line.split(":")[1].strip())
            elif "Sisa Enak" in line: 
                s_enak = int(line.split(":")[1].strip())

def save_data(self):
    """
    Fungsi untuk menulis (menyimpan) seluruh data dari dictionary self.users ke file TXT.
    """
    # Pastikan folder 'data' tersedia sebelum menulis file agar tidak FileNotFoundError
    if not os.path.exists("data"):
        os.makedirs("data")

    with open("data/data_user.txt", "w") as f:
        # Loop melalui setiap objek user yang ada di dictionary
        for u in self.users.values():
            # Ambil data promo_usage milik user, gunakan default 0 jika belum ada atributnya
            usage = getattr(u, 'promo_usage', {"HEMAT10": 0, "MAKANPUAS": 0, "MakanEnak": 0})
            
            # Tulis data ke file dengan format label yang rapi agar mudah dibaca manusia (dan fungsi load_data)
            f.write(f"Nama         : {u.username}\n")
            f.write(f"Password     : {u.password}\n")
            f.write(f"Saldo        : {u.saldo}\n")
            # Simpan 'Sisa Kuota' ke file agar user tahu berapa kali lagi promo bisa dipakai
            f.write(f"Sisa Hemat   : {2 - usage.get('HEMAT10', 0)}\n")
            f.write(f"Sisa Puas    : {3 - usage.get('MAKANPUAS', 0)}\n")
            f.write(f"Sisa Enak    : {5 - usage.get('MakanEnak', 0)}\n")
            # Garis pembatas antar user
            f.write("-" * 30 + "\n") 