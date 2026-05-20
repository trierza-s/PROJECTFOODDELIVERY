class GraphPeta:
    def __init__(self):

        # Menyimpan data graph/peta dalam bentuk dictionary
        # Setiap lokasi memiliki tujuan dan jarak tertentu
        self.peta = {
            "Kampus": {"Jalan Raya": 2, "Kost": 5},
            "Jalan Raya": {"Kampus": 2, "Mall": 4, "Restoran A": 3},
            "Kost": {"Kampus": 5, "Restoran B": 2},
            "Restoran A": {"Jalan Raya": 3},
            "Restoran B": {"Kost": 2, "Mall": 6},
            "Mall": {"Jalan Raya": 4, "Restoran B": 6}
        }

    # Fungsi rekursif untuk mencari jalur dengan jarak terpendek
    def cari_jarak_rekursif(self, asal, tujuan, visited=None, path=None, current_dist=0):

        # Jika visited belum ada, buat set kosong
        if visited is None: visited = set()

        # Jika path belum ada, buat list kosong
        if path is None: path = []

        # Menandai node yang sedang dikunjungi
        visited.add(asal)

        # Menambahkan lokasi sekarang ke jalur
        new_path = path + [asal]

        # Jika lokasi asal sudah sampai tujuan
        if asal == tujuan:

            # Mengembalikan total jarak dan jalur perjalanan
            return current_dist, new_path

        # Nilai awal jarak terpendek dibuat tak hingga
        shortest_dist = float('inf')

        # Variabel untuk menyimpan jalur terbaik
        best_path = None

        # Melakukan traversal ke semua tetangga
        for tetangga, jarak in self.peta.get(asal, {}).items():

            # Hanya diproses jika belum pernah dikunjungi
            if tetangga not in visited:

                # Rekursi untuk mencari jalur berikutnya
                dist, pth = self.cari_jarak_rekursif(tetangga, tujuan, visited.copy(), new_path, current_dist + jarak)

                # Mengecek apakah jarak baru lebih pendek
                if dist < shortest_dist:

                    # Memperbarui jarak terpendek
                    shortest_dist = dist

                    # Menyimpan jalur terbaik
                    best_path = pth

        # Mengembalikan hasil akhir pencarian
        return shortest_dist, best_path