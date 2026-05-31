import json
import os
from models.user import User

def simpan_semua_cart(app):
    """Menyimpan keranjang semua user ke file JSON di dalam folder 'data'."""
    # Mengecek dan membuat folder 'data' secara otomatis jika belum ada
    os.makedirs("data", exist_ok=True) 
    
    # Path diarahkan ke dalam folder data
    file_path = os.path.join("data", "carts_backup.json") 
    
    try:
        with open(file_path, "w") as f:
            # app merepresentasikan 'self' dari class FoodDeliveryCLI
            data = {uname: user.cart for uname, user in app.users.items()}
            json.dump(data, f)
    except Exception as e:
        print(f"Gagal menyimpan keranjang: {e}")

def muat_semua_cart(app):
    """Memuat keranjang user dari file JSON saat aplikasi dijalankan."""
    file_path = os.path.join("data", "carts_backup.json")
    
    # Jika filenya belum ada (misal saat program pertama kali dijalankan), abaikan
    if not os.path.exists(file_path):
        return
        
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            for uname, cart in data.items():
                if uname in app.users:
                    # Kembalikan tipe data ke dalam Tuple (Nama, Harga)
                    app.users[uname].cart = [tuple(item) for item in cart]
    except Exception as e:
        print(f"Gagal memuat keranjang: {e}")

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
        sisa_hemat, sisa_puas, sisa_enak = 2, 3, 5 
        
        for line in f:
            # Menghapus spasi/newline di awal dan akhir baris
            line = line.strip() 
            
            # Jika baris kosong atau berisi garis pemisah '---', tandanya satu blok data user selesai
            if not line or line[0] == "-":
                if uname:
                    # Buat objek User baru dengan data yang sudah terkumpul
                    u = User(uname, pwd, saldo)
                    # Hitung balik penggunaan promo (Usage = Kuota Maksimal - Sisa di File)
                    u.promo_usage = {
                        "HEMAT10": 2 - sisa_hemat, 
                        "MAKANPUAS": 3 - sisa_puas, 
                        "MakanEnak": 5 - sisa_enak
                    }
                    # Simpan objek user (u) ke dalam dictionary dengan key berupa username (uname)
                    self.users[uname] = u
                    
                    # Reset variabel untuk membaca user berikutnya di loop selanjutnya
                    uname, pwd, saldo, sisa_hemat, sisa_puas, sisa_enak = None, None, 0, 2, 3, 5
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
                sisa_hemat = int(line.split(":")[1].strip())
            elif "Sisa Puas" in line: 
                sisa_puas = int(line.split(":")[1].strip())
            elif "Sisa Enak" in line: 
                sisa_enak = int(line.split(":")[1].strip())

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
            f.write("-" * 30 + "\n") # Garis pembatas antar user