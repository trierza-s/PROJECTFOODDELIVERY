# Class node untuk Double Linked List
class DLLNode:
    def __init__(self, promo):
        
        # Menyimpan data promo pada node
        self.promo = promo
        
        # Pointer prev digunakan untuk menunjuk node sebelumnya
        # Awalnya bernilai None karena node belum terhubung
        self.prev = None
        
        # Pointer next digunakan untuk menunjuk node selanjutnya
        # Awalnya juga bernilai None
        self.next = None


# Class utama Double Linked List
class DoubleLinkedList:
    def __init__(self):
        
        # self.head berfungsi sebagai node pertama
        # pada Double Linked List
        self.head = None 

    # Method untuk menambahkan node di bagian akhir linked list
    def insert_tail(self, promo):
        
        # Membuat node baru berdasarkan data promo
        new_node = DLLNode(promo)

        # Mengecek apakah linked list masih kosong
        if self.head is None:
            
            # Jika kosong, node baru langsung menjadi head
            self.head = new_node

        else:
            # Variabel sementara untuk membantu traversal
            temp = self.head

            # Perulangan berjalan sampai menemukan node terakhir
            # Node terakhir ditandai dengan next bernilai None
            while temp.next:
                temp = temp.next

            # Menghubungkan node terakhir dengan node baru
            temp.next = new_node

            # Menghubungkan node baru ke node sebelumnya
            # menggunakan pointer prev
            new_node.prev = temp