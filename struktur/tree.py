class TreeNode:
    def __init__(self, nama_menu, harga=0):

        # Menyimpan nama menu atau kategori
        self.nama_menu = nama_menu

        # Menyimpan harga menu
        # Default bernilai 0 jika hanya sebagai kategori
        self.harga = harga

        # List untuk menampung child/node turunan
        self.children = []

    # Method untuk menambahkan child ke dalam node
    def add_child(self, child_node):

        # Menambahkan node anak ke list children
        self.children.append(child_node)

    # Method untuk mengambil seluruh item menu
    def get_all_items(self):

        # List kosong untuk menyimpan hasil item
        items = []

        # Jika node tidak memiliki child
        # dan memiliki harga lebih dari 0
        if not self.children and self.harga > 0:

            # Mengembalikan nama menu dan harga
            return [(self.nama_menu, self.harga)]

        # Melakukan traversal ke seluruh child
        for child in self.children:

            # Menggabungkan hasil item dari child
            items.extend(child.get_all_items())

        # Mengembalikan seluruh item menu
        return items