import sys
from models.user import User
from structures.graph import GraphPeta
from utility.menu import init_menu_tree
from structures.circular_linked_list import CircularLinkedList
from structures.double_linked_list import DoubleLinkedList
from utility.file_handler import load_data, save_data, simpan_semua_cart, muat_semua_cart
from utility.searching import binary_search
from utility.sorting import merge_sort

class FoodDeliveryCLI:
    def __init__(self):
        # Hash Table (Dictionary) untuk menyimpan data seluruh user
        self.users = {} 
        
        # Menyimpan data user yang sedang aktif/login
        self.logged_in_user = None 
        
        # Stack (LIFO) untuk fitur navigasi "Back" antar halaman
        self.history_stack = [] 
        
        # Konfigurasi Promo dan Harga Ongkir Dasar
        self.kode_promo_aktif = {"HEMAT10", "MAKANPUAS", "MakanEnak"}
        self.ongkir = {"motor": 2000, "mobil": 5000}
        
        # (TREE) Membangun struktur hierarki menu restoran (Root -> Kategori -> Menu)
        self.menu_tree = init_menu_tree()
        
        # (DOUBLE LINKED LIST (DLL)) Menyimpan dan menampilkan katalog promo
        dll = DoubleLinkedList()
        dll.insert_tail("HEMAT10 -> Potongan Ongkir Rp.5000")
        dll.insert_tail("MAKANPUAS -> Diskon Ongkir 15%")
        dll.insert_tail("MakanEnak -> Diskon Makanan 5%") 
        
        # Menyimpan titik awal (head) dari DLL Promo
        self.head_promo = dll.head 
        
        # (GRAPH) Menyimpan data peta rute pengiriman dan jarak antar lokasi
        self.peta = GraphPeta()

        # (CIRCULAR LINKED LIST (CLL)) Digunakan untuk rotasi penugasan driver
        cll = CircularLinkedList()
        cll.insert_tail("Andi (Motor)")
        cll.insert_tail("Budi (Motor)")
        cll.insert_tail("Siti (Mobil)") 
        
        # Menyimpan driver giliran pertama
        self.current_driver = cll.data_driver 

        # Menyimpan menu
        self.menu_tree = init_menu_tree()
        
        # Memuat data user dari file txt ke dalam self.users saat aplikasi pertama dibuka
        load_data(self)
        
        # Memuat data pesanan/cart yang tersimpan agar tidak hilang
        muat_semua_cart(self)

    # ==============================================
    # BAGIAN 1: SISTEM AUTENTIKASI (LOGIN & DAFTAR)
    # ==============================================

    def login(self):
        """Method untuk memverifikasi pengguna dan mengelola sesi login."""
        try:
            uname = input("Username: ").strip()
            # Mencari data user di dalam dictionary berdasarkan key (username)
            user = self.users.get(uname)
            
            # Jika username tidak ada di data
            if not user:
                print("Gagal: Username tidak ditemukan!")
                input("Tekan Enter untuk kembali...")
                # Langsung keluar dari fungsi jika user tidak ada
                return 

            pwd = input("Password: ").strip()
            
            # Verifikasi kecocokan password
            if user.password == pwd:
                # Tandai user x sedang login
                self.logged_in_user = user 
                
                # Masukkan halaman dashboard ke dalam Stack Navigasi agar layar berpindah
                self.history_stack.append(self.menu_dashboard)
            else:
                print("\nGagal: Password yang Anda masukkan salah!")
                lupa = input("Lupa password dan ingin membuat yang baru? (y/n): ").strip().lower()
                
                # Fitur ganti password jika lupa
                if lupa == 'y':
                    # Perulangan sampai syarat password terpenuhi
                    while True: 
                        password_baru = input("Masukkan Password Baru Anda (minimal 8 karakter): ").strip()
                        
                        if len(password_baru) >= 8:
                            user.password = password_baru
                            # Simpan perubahan ke file
                            save_data(self) 
                            print("Sukses: Password berhasil diubah! Silakan login ulang.")
                            # Hentikan perulangan jika sukses
                            break 
                        else:
                            print("Gagal: Password terlalu pendek! Harus minimal 8 karakter.\n")
                
                input("Tekan Enter untuk kembali...")
        except Exception as e:
            print(f"Error: {e}")

    """Method untuk menangani proses pendaftaran akun pengguna baru."""
    def daftar(self):
        try:
            # Perulangan sampai syarat username terpenuhi (minimal 4 karakter)
            while True:
                uname = input("Username: ").strip()

                # Validasi kelayakan username
                if len(uname) >= 4:
                    if not uname:
                        print("Gagal: Username tidak boleh kosong!")
                    
                    # Cek apakah username sudah dipakai (mencegah duplikasi)
                    elif uname in self.users: 
                        print("Gagal: Username sudah terdaftar!")
                    else:
                        # Jika username valid, lanjut ke pembuatan password
                        while True:
                            pwd = input("Password: ").strip()
                            
                            if len(pwd) >= 8:
                                # Buat objek User baru dan masukkan ke dalam Hash Table self.users
                                self.users[uname] = User(uname, pwd, 0)
                                
                                # Langsung simpan data ke file
                                save_data(self) 
                                print("Sukses: Akun berhasil dibuat!")
                                
                                # Keluar dari loop password
                                break 
                            else:
                                print("Password terlalu pendek, minimal 8 karakter\n")
                        
                        # Keluar dari loop username karena pendaftaran selesai
                        break 
                else:
                    print("Username terlalu pendek, minimal 4 karakter\n")

                input("Tekan Enter untuk melanjutkan...")
        except Exception as e:
            print(f"Error: {e}")

    # ==========================================
    # BAGIAN 2: UTILITAS TAMPILAN
    # ==========================================

    """Method untuk membersihkan layar terminal agar UI terlihat rapi."""
    def clear_screen(self):
        print("\n" * 0) 

    """Method untuk Menampilkan promo dari depan ke belakang."""
    def tampilkan_promo_dll(self):
        current = self.head_promo
        print("\n=== DAFTAR PROMO (DOUBLE LINKED LIST) ===")
        
        # Selama current tidak kosong (None), cetak isinya, lalu maju ke node selanjutnya
        while current:
            print(f"- {current.promo}")
            current = current.next

    # ============================================
    # BAGIAN 3: SISTEM NAVIGASI (STACK) & MENU UI
    # ============================================

    def run(self):
        """Sistem Utama Aplikasi. 
        Menggunakan konsep Stack (LIFO: Last In First Out) untuk mengatur perpindahan halaman.
        """
        # Halaman pertama yang dimasukkan ke stack adalah menu_utama (halaman login)
        self.history_stack.append(self.menu_utama)
        
        # Loop akan terus berjalan selama isi stack tidak kosong
        while self.history_stack:
            try:
                # Mengambil halaman paling atas dari stack (indeks -1) tanpa menghapusnya
                current_page = self.history_stack[-1]
                
                # Menjalankan fungsi halaman tersebut
                current_page()
            except KeyboardInterrupt:
                # Mencegah program error berantakan jika user menekan Ctrl+C
                print("\nProgram dihentikan paksa oleh pengguna. Menyimpan data...")
                save_data(self)
                simpan_semua_cart(self)
                # Menghentikan seluruh program
                sys.exit()

    def menu_utama(self):
        """Halaman Awal (Landing Page) saat aplikasi baru dibuka."""
        self.clear_screen()
        print("=== FOOD DELIVERY ===")
        print("1. Login")
        print("2. Daftar Akun")
        print("0. Terima Kasih Sudah Menggunakan Sistem ini!")
        try:
            pilih = input("Pilih: ").strip()
            if pilih == "1":
                self.login()
            elif pilih == "2":
                self.daftar()
            elif pilih == "0":
                save_data(self)
                simpan_semua_cart(self)
                # Menghentikan seluruh program
                sys.exit() 
            else:
                print("Pilihan tidak valid")
        except Exception as e:
            print(f"Error: {e}")

    def tampilkan_kategori_resto(self, resto_node):
        """Menampilkan kategori yang ada di dalam sebuah Node Restoran (Tree Level 2)."""
        
        # Membuat fungsi lokal agar fungsi ini bisa dibungkus dan dimasukkan ke dalam Stack Navigasi
        def menu_kategori():
            self.clear_screen()
            print(f"=== KATEGORI {resto_node.nama.upper()} ===")
            
            # Looping mengambil anak-anak dari node Restoran (yaitu node Kategori)
            for i, child in enumerate(resto_node.children, 1):
                print(f"{i}. {child.nama}")
            print("99. Back")
            
            try:
                pilih = input("Pilih kategori: ").strip()
                if pilih == "99":
                    # Menghapus halaman ini dari Stack, sehingga aplikasi otomatis kembali ke halaman sebelumnya (Dashboard)
                    self.history_stack.pop()
                else:
                    try:
                        pilih_angka = int(pilih)
                        
                        # Cek apakah angka berada di dalam rentang jumlah menu
                        if 1 <= pilih_angka <= len(resto_node.children):
                            kategori_dipilih = resto_node.children[pilih_angka - 1]
                            self.tampilkan_menu_item(kategori_dipilih)
                        else:
                            print("Pilihan tidak valid! Masukkan nomor yang ada di daftar menu.")
                            input("Enter...")
                            
                    except ValueError:
                        # Muncul jika user sengaja memasukkan huruf, simbol, atau menekan enter kosong
                        print("Pilihan tidak valid! Harap masukkan berupa angka.")
                        input("Enter...")
            except Exception as e:
                print(f"Error: {e}")
                
        # Memasukkan halaman yang baru dibuat ini ke dalam Stack navigasi
        self.history_stack.append(menu_kategori)

    def tampilkan_menu_item(self, kategori_node):
        """Menampilkan menu makanan/minuman dari suatu Kategori (Tree Level 3)."""
        def menu_item():
            self.clear_screen()
            print(f"=== MENU {kategori_node.nama.upper()} ===")
            
            # Looping mengambil anak-anak dari node Kategori (yaitu Node Menu Akhir)
            for i, item in enumerate(kategori_node.children, 1):
                print(f"{i}. {item.nama} - Rp{item.harga}")
            print("99. Back")
            
            try:
                pilih = input("Pilih untuk tambah ke cart: ").strip()
                if pilih == "99":
                    # Buang halaman ini dari stack agar kembali ke layar Kategori
                    self.history_stack.pop() 
                else:
                    try:
                        pilih_angka = int(pilih)
                        
                        # Cek apakah angka berada di dalam rentang jumlah item menu
                        if 1 <= pilih_angka <= len(kategori_node.children):
                            item_dipilih = kategori_node.children[pilih_angka - 1]
                            
                            # Simpan data makanan ke dalam keranjang user berbentuk Tuple: (Nama, Harga)
                            self.logged_in_user.cart.append((item_dipilih.nama, item_dipilih.harga))
                            save_data(self)
                            simpan_semua_cart(self)  # Simpan cart
                            print(f"{item_dipilih.nama} berhasil masuk keranjang!")
                            input("Enter...")
                        else:
                            print("Pilihan tidak valid! Masukkan nomor yang ada di daftar menu.")
                            input("Enter...")
                            
                    except ValueError:
                        # Muncul jika input berupa huruf, simbol, atau kosong
                        print("Pilihan tidak valid! Harap masukkan berupa angka.")
                        input("Enter...")
            except Exception as e:
                print(f"Error: {e}")
                
        self.history_stack.append(menu_item)

    # ===============================================
    # BAGIAN 4: FITUR PENCARIAN (SORTING & SEARCHING)
    # ===============================================

    def cari_menu_global(self):
        """Fitur untuk mencari menu dari seluruh restoran."""
        try:
            semua_menu = []
            
            # Mengubah struktur Tree yang bercabang menjadi satu List panjang (1 Dimensi)
            for resto in self.menu_tree.children:
                for kategori in resto.children:
                    for item in kategori.children:
                        semua_menu.append((item.nama, item.harga))
            
            # (SORTING) Mengurutkan list menu berdasarkan nama menggunakan algoritma Merge Sort
            # Binary Search WAJIB dilakukan pada data yang sudah terurut (Sorted)
            merge_sort(semua_menu)
            print("\nMenu Tersedia (Sorted):", [m[0] for m in semua_menu])
            
            target = input("Ketik nama menu yang dicari: ").strip()
            
            # (SEARCHING) Mencari menu menggunakan algoritma Binary Search (membelah data jadi dua terus menerus)
            hasil = binary_search(semua_menu, target)
            
            if hasil:
                print(f"Ketemu! {hasil[0]} harganya Rp{hasil[1]}")
                while True:
                    if input("Tambah ke keranjang? (y/n): ").strip().lower() == "y":
                        self.logged_in_user.cart.append(hasil)
                        save_data(self)
                        simpan_semua_cart(self)  
                        print(f"Pesanan {hasil} berhasil ditambahkan")
                        break
                    else:
                        print("Pilihan tidak valid")
            else:
                print("Menu tidak ditemukan.")
            input("Enter...")
        except Exception as e:
            print(f"Error: {e}")

    def menu_dashboard(self):
        self.clear_screen()
        """Halaman utama saat user berhasil login."""
        print(f"=== DASHBOARD | {self.logged_in_user.username} ===")
        print(f"Saldo: Rp{self.logged_in_user.saldo}")
        
        print("1. Top-Up Saldo")
        print("2. Restoran A")
        print("3. Restoran B")
        print("4. Cari Menu (Binary Search)")
        print("5. Lihat Keranjang & Checkout")
        print("6. Riwayat Pesanan (SLL)")
        print("7. Katalog Promo (DLL)")
        print("0. Logout")
        
        try:
            pilih = input("Pilih: ").strip()
            
            if pilih == "1":
                try:
                    nom = int(input("Nominal Top-Up: "))
                    if nom > 0:
                        # Menambahkan saldo user yang sedang login
                        self.logged_in_user.saldo += nom
                        save_data(self)
                        print(f"Saldo berhasil ditambahkan! Saldo Anda: Rp{self.logged_in_user.saldo}")
                    else:
                        print("Nominal harus lebih dari 0!")
                except ValueError:
                    print("Gagal: Masukkan angka yang valid!")
                input("Enter...")
                
            elif pilih == "2":
                # Mengirim node 'Restoran A' ke fungsi pembuat layar Kategori
                resto_dipilih = self.menu_tree.children[0]
                self.tampilkan_kategori_resto(resto_dipilih)
                
            elif pilih == "3":
                # Mengirim node 'Restoran B' ke fungsi pembuat layar Kategori
                resto_dipilih = self.menu_tree.children[1]
                self.tampilkan_kategori_resto(resto_dipilih)
                
            elif pilih == "4":
                self.cari_menu_global()
                
            elif pilih == "5":
                self.checkout()
                
            elif pilih == "6":
                print("\n=== RIWAYAT PESANAN ===")
                
                # Mengakses object Single Linked List (SLL) milik user dan memanggil method display()-nya
                self.logged_in_user.history.display()
                input("Enter...")
                
            elif pilih == "7":
                # Validasi bisnis, user harus punya isi keranjang untuk lihat promo
                if len(self.logged_in_user.cart) > 0:
                    self.clear_screen()
                    self.tampilkan_promo_dll()
                else:
                    print("\n[!] Maaf, kamu harus memesan menu terlebih dahulu untuk melihat katalog promo.")
                input("\nTekan Enter untuk kembali...")
                
            elif pilih == "0":
                # Proses Logout, Putuskan sesi dan buang Dashboard dari Stack agar kembali ke Menu Utama
                self.logged_in_user = None
                self.history_stack.pop()
            else:
                print("Pilihan tidak valid.")
                input("Enter...")
        except Exception as e:
            print(f"Error: {e}")

    # =====================================================
    # BAGIAN 5: SISTEM PEMBAYARAN & LOGIKA GRAPH (CHECKOUT)
    # =====================================================

    def checkout(self):
        """Fitur untuk menghitung total belanja, mengecek jarak rute, dan mengeksekusi pesanan."""
        try:
            cart = self.logged_in_user.cart
            if not cart:
                print("Keranjang kosong!")
                input("Enter...") 
                return
            
            # Menghitung total harga makanan dari tuple (item[1] adalah harga)
            harga_makanan = sum(item[1] for item in cart)
            print(f"\n--- DETAIL PESANAN ---")
            print(f"Item: {[i[0] for i in cart]}")
            print(f"Harga Makanan: Rp{harga_makanan}")
        
            # --- (GRAPH) VALIDASI LOKASI & RUTE PENGIRIMAN ---
            jarak, rute = 0, []
            lokasi_user = ""
            while True:
                lokasi_user = input("Locations Pengiriman (Kampus/Kost/Mall) atau 'batal': ").strip().title()
                if lokasi_user.lower() == 'batal': 
                    return
            
                # Mencari jalur dari Restoran A ke lokasi user menggunakan fungsi rekursif pencarian Graph
                jarak, rute = self.peta.cari_jarak_rekursif("Restoran A", lokasi_user)
            
                if rute: 
                    # Jika Graph mengembalikan rute yang valid
                    ongkir_awal = jarak * self.ongkir["motor"]
                    print(f"--> Rute Ditemukan: {' -> '.join(rute)}")
                    print(f"--> Total Jarak: {jarak} km")
                    break
                else:
                    print("--> Lokasi tidak valid!\n")
        
            # --- MANAJEMEN PROMO ---
          
            # Menggunakan Set agar tidak ada promo ganda di satu pesanan
            promo_terpakai_saat_ini = set() 
            total_diskon_ongkir = 0
            total_diskon_makanan = 0 
        
            while len(promo_terpakai_saat_ini) < 3:
                # Cek sisa kuota promo yang bisa dipakai oleh user ini
                sisa_h = max(0, 2 - self.logged_in_user.promo_usage["HEMAT10"])
                sisa_p = max(0, 3 - self.logged_in_user.promo_usage["MAKANPUAS"])
                sisa_m = max(0, 5 - self.logged_in_user.promo_usage["MakanEnak"])

                print(f"\n--- PROMO TERSEDIA ---")
                if "HEMAT10" not in promo_terpakai_saat_ini:
                    print(f"1. HEMAT10  (sisa {sisa_h}) -> Potongan Rp5.000")
                if "MAKANPUAS" not in promo_terpakai_saat_ini:
                    print(f"2. MAKANPUAS (sisa {sisa_p}) -> Diskon Ongkir 15%")
                if "MakanEnak" not in promo_terpakai_saat_ini:
                    print(f"3. MakanEnak (sisa {sisa_m}) -> Diskon Makanan 5%") 

                pilihan = input("\nPilih nomor promo atau Enter untuk lewati: ").strip()
            
                if pilihan == "": 
                    # Langsung ke pembayaran jika user menekan Enter kosong
                    break 

                # Mapping input angka ke ID promo
                mapping = {"1": "HEMAT10", "2": "MAKANPUAS", "3": "MakanEnak"}
                promo_id = mapping.get(pilihan)

                if not promo_id:
                    print("-> Pilihan tidak valid.")
                    continue
            
                if promo_id in promo_terpakai_saat_ini:
                    print(f"-> Promo {promo_id} sudah terpasang!")
                    continue

                # Logika kalkulasi perhitungan diskon berdasarkan promo
                diskon_ongkir_saat_ini = 0
                diskon_makanan_saat_ini = 0
                
                if pilihan == "1" and sisa_h > 0:
                    diskon_ongkir_saat_ini = 5000
                elif pilihan == "2" and sisa_p > 0:
                    diskon_ongkir_saat_ini = int(ongkir_awal * 0.15)
                elif pilihan == "3" and sisa_m > 0:
                    diskon_makanan_saat_ini = int(harga_makanan * 0.05) 
                else:
                    print("-> Kuota promo habis!")
                    continue

                # Fitur limitasi: Memastikan diskon tidak pernah melampaui harga dasarnya
                total_diskon_ongkir = min(ongkir_awal, total_diskon_ongkir + diskon_ongkir_saat_ini)
                total_diskon_makanan = min(harga_makanan, total_diskon_makanan + diskon_makanan_saat_ini)
                
                promo_terpakai_saat_ini.add(promo_id)
                print(f"-> Sukses menambahkan {promo_id}!")

                # Beri opsi jika user ingin menumpuk promo
                try:
                    if len(promo_terpakai_saat_ini) < 3:
                        tambah = input("Tambah promo lain?(maksimal 2) (y/n): ").lower()
                        if tambah != 'y': break
                    else:
                        print("Sudah mencapai batas pengunaan")
                except Exception as e:
                    print(f"Error: {e}")

            # Pastikan ongkir dan makanan tidak minus setelah diskon
            ongkir_akhir = max(0, ongkir_awal - total_diskon_ongkir)
            harga_makanan_akhir = max(0, harga_makanan - total_diskon_makanan)
            total_bayar = harga_makanan_akhir + ongkir_akhir

            # --- RINGKASAN & KONFIRMASI ---
            print(f"\n--- RINGKASAN PEMBAYARAN ---")
            print(f"Total Makanan : Rp{harga_makanan}")
            if total_diskon_makanan > 0:
                print(f"Diskon Makanan: -Rp{total_diskon_makanan}")
                print(f"Ongkir Awal   : Rp{ongkir_awal}")
                print(f"Diskon Ongkir : -Rp{total_diskon_ongkir}")
                print(f"TOTAL BAYAR   : Rp{total_bayar}")
                print(f"Saldo Anda    : Rp{self.logged_in_user.saldo}")

            konfirmasi = input("\nKonfirmasi Bayar? (y/n): ").lower()
            if konfirmasi != 'y':
                return

            # --- EKSEKUSI PEMBAYARAN ---
            if self.logged_in_user.saldo >= total_bayar:
                # Kurangi saldo
                self.logged_in_user.saldo -= total_bayar
                
                # Catat pemakaian promo agar kuotanya berkurang di pesanan berikutnya
                for p in promo_terpakai_saat_ini:
                    self.logged_in_user.promo_usage[p] += 1
            
                # --- (CIRCULAR LINKED LIST) PENUGASAN DRIVER ---
                
                # Ambil nama driver yang mendapat giliran saat ini
                driver = self.current_driver.data_driver
                
                # Geser giliran (Pointer Node) ke driver berikutnya secara melingkar
                self.current_driver = self.current_driver.next 
            
                # --- (SINGLE LINKED LIST) CATAT RIWAYAT ---
                pesanan_str = f"Order: {[i[0] for i in cart]}, Ke: {lokasi_user}, Driver: {driver}, Total: Rp{total_bayar}"
                
                # Menambahkan string riwayat ke dalam Single Linked List (SLL) milik user
                self.logged_in_user.history.add_history(pesanan_str)
                
                # Kosongkan keranjang setelah berhasil checkout
                self.logged_in_user.cart = []
            
                save_data(self)
                simpan_semua_cart(self) 
                print(f"\nBERHASIL! Driver {driver} sedang menuju lokasi.")
            else:
                print("\nSaldo tidak cukup!")
        
            input("Enter...")
        except Exception as e:
            print(f"Terjadi kesalahan sistem: {e}")
            input("Enter...")

# Blok ini akan dieksekusi jika file ini dijalankan langsung (bukan di-import sebagai module)
if __name__ == "__main__":
    app = FoodDeliveryCLI()
    app.run()