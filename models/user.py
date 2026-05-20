from structures.singlelinked_list import SLLHistory

class User:
    def __init__(self, username, password, saldo=0):
        self.username = username
        self.password = password
        self.saldo = saldo
        # Riwayat Pemesanan
        self.history = SLLHistory()
        # Tempat menyimpan pemesanan
        self.cart = []
        # Promo
        self.promo_usage = {"HEMAT10": 0, "MAKANPUAS": 0, "MakanEnak": 0}