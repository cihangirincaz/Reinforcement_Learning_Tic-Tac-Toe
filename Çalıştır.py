from TicTacToe import TicTacToe
from Agent import Ajan

oyun = TicTacToe()

## EĞİTİM PARAMETRE ÖNERİSİ ##
# X oyuncusu için --> öneri = indirim_faktoru = 0.6
# O oyuncusu için --> öneri = indirim_faktoru = 0.5
ajan = Ajan(oyun, 'X', indirim_faktoru = 0.6, bolum = 60000)

ajan.insanla_oyna()
