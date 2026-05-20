class SLLNode:
    def __init__(self, data):

        # Menyimpan data pada node
        self.data = data

        # Pointer menuju node berikutnya
        self.next = None

class SLLHistory:
    def __init__(self):

        # Head sebagai node pertama pada linked list
        self.head = None

    # Method untuk menambahkan riwayat pesanan
    def add_history(self, data):

        # Membuat node baru
        new_node = SLLNode(data)

        # Jika linked list masih kosong
        if not self.head:

            # Node baru dijadikan head
            self.head = new_node

        else:
            # Variabel bantu untuk traversal
            current = self.head

            # Bergerak sampai node terakhir
            while current.next:
                current = current.next

            # Menyambungkan node terakhir ke node baru
            current.next = new_node

    # Method untuk menampilkan seluruh riwayat
    def display(self):

        # Mulai traversal dari head
        current = self.head

        # Mengecek apakah linked list kosong
        if not current:
            print("Belum ada riwayat pesanan.")
            return

        # Menampilkan data satu per satu
        while current:
            print(f"- {current.data}")

            # Berpindah ke node selanjutnya
            current = current.next