def merge_sort(arr):
    # Jika panjang array 1 atau kurang, data sudah dianggap terurut
    if len(arr) > 1:
        # Menentukan titik tengah array
        mid = len(arr) // 2
        
        # Membelah array menjadi dua bagian: Kiri (L) dan Kanan (R)
        L, R = arr[:mid], arr[mid:]

        # Rekursif: Pecah terus bagian kiri sampai tersisa 1 elemen
        merge_sort(L)
        # Rekursif: Pecah terus bagian kanan sampai tersisa 1 elemen
        merge_sort(R)

        # Proses Penggabungan (Merging)
        i = j = k = 0

        # Bandingkan elemen dari list L dan R, lalu masukkan yang terkecil ke arr
        while i < len(L) and j < len(R):
            # Membandingkan L[i][0] karena data berupa tuple (nama, harga)
            if L[i][0] < R[j][0]:
                arr[k] = L[i]
                i += 1
            else: 
                arr[k] = R[j]
                j += 1
            k += 1

        # Jika ada elemen yang tersisa di bagian L (Kiri)
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        # Jika ada elemen yang tersisa di bagian R (Kanan)
        while j < len(R): 
            arr[k] = R[j]
            j += 1
            k += 1