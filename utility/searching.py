def binary_search(arr, target):
    # Menentukan batas awal (low) dan batas akhir (high) dari array
    low, high = 0, len(arr) - 1
    
    # Perulangan akan terus berjalan selama batas bawah tidak melewati batas atas
    while low <= high:
        # Menghitung titik tengah array untuk membagi area pencarian menjadi dua
        mid = (low + high) // 2
        
        # Mengecek apakah nama menu di titik tengah sama dengan target (case-insensitive)
        if arr[mid][0].lower() == target.lower(): 
            # Jika cocok, kembalikan data menu tersebut (biasanya berupa tuple/list)
            return arr[mid]
        
        # Jika nama menu di tengah secara alfabetis lebih kecil dari target
        elif arr[mid][0].lower() < target.lower(): 
            # Geser batas bawah ke kanan (abaikan setengah bagian kiri)
            low = mid + 1
        
        # Jika nama menu di tengah lebih besar dari target secara alfabet
        else: 
            # Geser batas atas ke kiri (abaikan setengah bagian kanan)
            high = mid - 1
            
    # Jika perulangan selesai dan target tidak ditemukan, kembalikan None
    return None