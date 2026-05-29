# Class untuk membuat node pada Circular Linked List
class CLLNode:
    def __init__(self, data_driver):

        # Menyimpan data driver ke dalam node
        self.data_driver = data_driver
        
        # Pointer next digunakan untuk menunjuk node selanjutnya
        # Awalnya bernilai None karena belum terhubung ke node lain
        self.next = None


# Class utama Circular Linked List
class CircularLinkedList:
    def __init__(self):

        # self.data_driver berfungsi sebagai head
        # yaitu node pertama dalam Circular Linked List
        self.data_driver = None 

    # Method untuk menambahkan node di bagian akhir linked list
    def insert_tail(self, data_driver):
        
        # Membuat object/node baru
        new_node = CLLNode(data_driver)

        # Mengecek apakah linked list masih kosong
        if self.data_driver is None:
            
            # Jika kosong, node baru langsung menjadi head
            self.data_driver = new_node
            
            # Karena Circular Linked List bersifat melingkar,
            # maka node pertama harus menunjuk kembali ke dirinya sendiri
            new_node.next = self.data_driver

        else:
            # Variabel sementara untuk membantu traversal
            temp = self.data_driver

            # Melakukan perulangan sampai menemukan node terakhir
            # Node terakhir ditandai dengan next yang kembali ke head
            while temp.next != self.data_driver:
                temp = temp.next

            # Menghubungkan node terakhir ke node baru
            temp.next = new_node

            # Node baru diarahkan kembali ke head
            # agar struktur tetap berbentuk lingkaran
            new_node.next = self.data_driver