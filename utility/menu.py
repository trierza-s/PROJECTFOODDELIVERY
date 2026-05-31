from structures.tree import TreeNode
"""Method untuk Membangun struktur Tree hierarki menu.
     Root (Console) -> Node Anak (Restoran) -> Node Cucu (Kategori) -> Node Cicit (Item Menu)
"""
def init_menu_tree():
    # Titik paling atas (Root)
    root = TreeNode("Daftar Restoran") 

    # --- 1. RESTORAN A ---
    resto_a = TreeNode("Restoran A")
        
    # Kategori Makanan Resto A
    makanan_a = TreeNode("Makanan") 
    makanan_a.add_child(TreeNode("Ayam Geprek", 15000))
    makanan_a.add_child(TreeNode("Mie Setan", 12000))
    makanan_a.add_child(TreeNode("Kwetiau Goreng", 16000))
    makanan_a.add_child(TreeNode("Nila Bakar", 20000))
    makanan_a.add_child(TreeNode("Lele Goreng", 15000))
        
    # Kategori Minuman Resto A
    minuman_a = TreeNode("Minuman") 
    minuman_a.add_child(TreeNode("Es Teh Manis", 5000))
    minuman_a.add_child(TreeNode("Es Jeruk", 6000))
    minuman_a.add_child(TreeNode("Es Timun", 4000))
    minuman_a.add_child(TreeNode("Teh Hangat", 3000))
    minuman_a.add_child(TreeNode("Jus Mangga", 7000))
        
    # Menggabungkan kategori ke dalam Restoran A
    resto_a.add_child(makanan_a)
    resto_a.add_child(minuman_a)

    # --- 2. RESTORAN B ---
    resto_b = TreeNode("Restoran B")
        
    cemilan_b = TreeNode("Cemilan")
    cemilan_b.add_child(TreeNode("Brownies", 25000))
    cemilan_b.add_child(TreeNode("Kentang Goreng", 15000))
    cemilan_b.add_child(TreeNode("Nugget Goreng", 15000))
    cemilan_b.add_child(TreeNode("Burger", 8000))
    cemilan_b.add_child(TreeNode("Sosis Goreng", 10000))
        
    minuman_b = TreeNode("Minuman")
    minuman_b.add_child(TreeNode("Kopi Susu", 10000))
    minuman_b.add_child(TreeNode("Air Mineral", 4000))
    minuman_b.add_child(TreeNode("Kopi Gula Aren", 15000))
    minuman_b.add_child(TreeNode("Jahe Hangat", 12000))
    minuman_b.add_child(TreeNode("Teh Tarik", 8000))

    resto_b.add_child(cemilan_b)
    resto_b.add_child(minuman_b)

    # --- MENGGABUNGKAN SEMUA RESTORAN KE ROOT ---
    root.add_child(resto_a)
    root.add_child(resto_b)

    # Kembalikan struktur Tree utuh
    return root 