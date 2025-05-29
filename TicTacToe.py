import numpy as np

class TicTacToe:
    """
    current_state: [0 X 0 0 0 0 0 0 0] gibi mevcut oyun durumunu tutar
    """
    
    def __init__(self):
        self.guncel_durum = np.zeros(9, dtype=np.int8)
        self.kazanan = None
        self.oyuncu = 1
    
    def guncel_oyunu_ciz(self):
        guncel_durum = ['X' if x == 1 else 'O' if x == -1 else '--' for x in self.guncel_durum]
        print(f'{guncel_durum[0]:^5} {guncel_durum[1]:^5} {guncel_durum[2]:^5}')
        print(f'{guncel_durum[3]:^5} {guncel_durum[4]:^5} {guncel_durum[5]:^5}')
        print(f'{guncel_durum[6]:^5} {guncel_durum[7]:^5} {guncel_durum[8]:^5}')
        print('_' * 15)

    def guncel_oyunu_al(self):
        return self.guncel_durum
    
    def guncel_oyun_tupu_al(self):
        return tuple(self.guncel_durum)

    def musait_pozisyonlari_al(self):
        return np.argwhere(self.guncel_durum == 0).ravel()  # argwhere 2D array döner, array'i düzleştirmemiz gerekir

    def oyunu_sifirla(self):
        self.guncel_durum = np.zeros(9, dtype=np.int8)
        self.oyuncu = 1

    def oyuncuyu_al(self):
        return self.oyuncu

    """
    Gerçek hareketi gerçekleştirir.
    """
    def hareket_yap(self, hareket):  # oyuncu 1 ise X, oyuncu -1 ise O
        if hareket in self.musait_pozisyonlari_al():
            self.guncel_durum[hareket] = self.oyuncu
            self.oyuncu *= -1
        else:
            print('Bu pozisyon uygun değil')

    """
    Hareket yapılırsa oluşacak durumu döner.
    """
    def _hareket_yap(self, _guncel_durum, hareket):  # Kullanıcıdan giriş almak için uygun değil, make_move fonksiyonu tercih edilmeli
        _guncel_durum[hareket] = self.oyuncu
        return _guncel_durum

    """
    Olası hareketler yapılırsa oluşacak durumları döner.
    """
    def sonraki_durumlari_al(self):
        durumlar = []
        _guncel_durum = self.guncel_durum
        _musait_hareketler = self.musait_pozisyonlari_al()
        for hareket in _musait_hareketler:
            durumlar.append(self._hareket_yap(_guncel_durum=_guncel_durum, hareket=hareket))
        return durumlar
        
    def kazanan_var_mi(self, oyun_devam=False):
        kazanan_koordinatlari = np.array([[0,1,2], [3, 4, 5], [6, 7, 8],
                                          [0, 3, 6], [1, 4, 7], [2, 5, 8],
                                          [0, 4, 8], [2, 4, 6]])
        for koordinat in kazanan_koordinatlari:
            toplam = sum(self.guncel_durum[koordinat])
            if toplam == 3:  # X kazandı
                if oyun_devam:
                    print('X Kazandı!')
                self.kazanan = 1
                self.oyunu_sifirla()
                return 1
            elif toplam == -3:  # O kazandı
                if oyun_devam:
                    print('O Kazandı!')
                self.kazanan = -1
                self.oyunu_sifirla()
                return -1
            elif sum(self.guncel_durum == 1) == 5:  # Beraberlik
                if oyun_devam:
                    print('Beraberlik')
                self.kazanan = -2
                self.oyunu_sifirla()
                return -2
        return False
