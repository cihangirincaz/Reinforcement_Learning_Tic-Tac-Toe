import numpy as np
import random
import pickle

class Ajan:
    def __init__(self, oyun, oyuncu='X', bolum=100000, epsilon=0.9, indirim_faktoru=0.6, epsilon_azaltma_faktoru=0.01):
        """
        oyun: Ajanın eğitileceği TicTacToe oyunu
        oyuncu: Ajanın oynayacağı oyuncu ('X' veya 'O')
        beyin: Oyundaki farklı durumların q değerlerini tutar
        bolum: Eğitim sonunda kaç oyun oynanacağını belirtir
        epsilon: Ajanın rastgele mi yoksa q tablosuna göre mi hareket edeceğini belirleyen değer
        indirim_faktoru: Geri yayılım katsayısı
        """
        self.oyun = oyun
        self.oyuncu = oyuncu
        self.beyin = dict()
        self.bolum = bolum
        self.epsilon = epsilon
        self.indirim_faktoru = indirim_faktoru
        self.sonuclar = {'X': 0, 'O': 0, 'B': 0}
        self.epsilon_azaltma_faktoru = epsilon_azaltma_faktoru

    def beyin_kaydet(self, oyuncu):
        with open('beyin' + oyuncu, 'wb') as beyin_dosyasi:
            pickle.dump(self.beyin, beyin_dosyasi)

    def beyin_yukle(self, oyuncu):
        try:
            with open('beyin' + oyuncu, 'rb') as beyin_dosyasi:
                self.beyin = pickle.load(beyin_dosyasi)
        except:
            print('Henüz bir beyin yok. Önce ajanı eğitmelisiniz. Bu nedenle bu oyun ajanı rastgele oynayacak')

    def odullendir(self, oyuncu, hareket_gecmisi, sonuc):
        _odul = 0
        if oyuncu == 1:
            if sonuc == 1:
                _odul = 1
                self.sonuclar['X'] += 1
            elif sonuc == -1:
                _odul = -1
                self.sonuclar['O'] += 1
        elif oyuncu == -1:
            if sonuc == 1:
                _odul = -1
                self.sonuclar['X'] += 1
            elif sonuc == -1:
                _odul = 1
                self.sonuclar['O'] += 1
        if sonuc == -2:
            self.sonuclar['B'] += 1
        hareket_gecmisi.reverse()
        for durum, hareket in hareket_gecmisi:
            self.beyin[durum, hareket] = self.beyin.get((durum, hareket), 0.0) + _odul
            _odul *= self.indirim_faktoru

    def beyin_kullan(self):
        olasi_hareketler = self.oyun.musait_pozisyonlari_al()
        max_qdegeri = -1000
        en_iyi_hareket = olasi_hareketler[0]
        for hareket in olasi_hareketler:
            qdegeri = self.beyin.get((self.oyun.guncel_oyun_tupu_al(), hareket), 0.0)
            if qdegeri > max_qdegeri:
                en_iyi_hareket = hareket
                max_qdegeri = qdegeri
            elif qdegeri == max_qdegeri and random.random() < 0.5:
                en_iyi_hareket = hareket
                max_qdegeri = qdegeri
            elif len(olasi_hareketler) == 9:
                en_iyi_hareket = random.choice(olasi_hareketler)
                break
        return en_iyi_hareket

    def beyin_egit_x_rastgele(self):
        for _ in range(self.bolum):
            if _ % 1000 == 0:
                print('Bölüm: ' + str(_))
                self.epsilon -= self.epsilon_azaltma_faktoru
            hareket_gecmisi = []
            while True:
                if sum(self.oyun.guncel_oyunu_al() == 1) == 0 or random.random() < self.epsilon:
                    musait_hareketler = self.oyun.musait_pozisyonlari_al()
                    hareket_x = random.choice(musait_hareketler)
                    hareket_gecmisi.append([self.oyun.guncel_oyun_tupu_al(), hareket_x])
                    self.oyun.hareket_yap(hareket_x)
                else:
                    hareket_x = self.beyin_kullan()
                    hareket_gecmisi.append([self.oyun.guncel_oyun_tupu_al(), hareket_x])
                    self.oyun.hareket_yap(hareket_x)
                if self.oyun.kazanan_var_mi():
                    self.odullendir(1, hareket_gecmisi, self.oyun.kazanan)
                    break
                musait_hareketler = self.oyun.musait_pozisyonlari_al()
                hareket_o = random.choice(musait_hareketler)
                self.oyun.hareket_yap(hareket_o)
                if self.oyun.kazanan_var_mi():
                    self.odullendir(1, hareket_gecmisi, self.oyun.kazanan)
                    break
        self.beyin_kaydet('X')
        print('EĞİTİM TAMAMLANDI!')
        print('SONUÇLAR:')
        print(self.sonuclar)

    def beyin_egit_o_rastgele(self):
        for _ in range(self.bolum):
            if _ % 1000 == 0:
                print('Bölüm: ' + str(_))
                self.epsilon -= self.epsilon_azaltma_faktoru
            hareket_gecmisi = []
            while True:
                musait_hareketler = self.oyun.musait_pozisyonlari_al()
                hareket_x = random.choice(musait_hareketler)
                self.oyun.hareket_yap(hareket_x)
                if self.oyun.kazanan_var_mi():
                    self.odullendir(-1, hareket_gecmisi, self.oyun.kazanan)
                    break
                if random.random() < self.epsilon:
                    musait_hareketler = self.oyun.musait_pozisyonlari_al()
                    hareket_o = random.choice(musait_hareketler)
                    hareket_gecmisi.append([self.oyun.guncel_oyun_tupu_al(), hareket_o])
                    self.oyun.hareket_yap(hareket_o)
                else:
                    hareket_o = self.beyin_kullan()
                    hareket_gecmisi.append([self.oyun.guncel_oyun_tupu_al(), hareket_o])
                    self.oyun.hareket_yap(hareket_o)
                if self.oyun.kazanan_var_mi():
                    self.odullendir(-1, hareket_gecmisi, self.oyun.kazanan)
                    break
        self.beyin_kaydet('O')
        print('EĞİTİM TAMAMLANDI!')
        print('SONUÇLAR:')
        print(self.sonuclar)
    
    def insanla_oyna(self):
        self.beyin_yukle(self.oyuncu)
        sirasi = 1 if self.oyuncu == 'X' else -1
        while True:
            if sirasi == 1:
                self.oyun.hareket_yap(self.beyin_kullan())
                self.oyun.guncel_oyunu_ciz()
                sirasi *= -1
                if self.oyun.kazanan_var_mi(oyun_devam=True):
                    break
            else:
                hareket_o = int(input('Hangi kare?'))
                self.oyun.hareket_yap(hareket_o - 1)
                self.oyun.guncel_oyunu_ciz()
                sirasi *= -1
                if self.oyun.kazanan_var_mi(oyun_devam=True):
                    break
