import pygame as pg
import Cores

class Destrutivel:
     def __init__(self,maxHp, defesa, nomeCadaver,simbCadaver, si):
          self.maxHp = maxHp
          self.hp = maxHp
          self.defesa = defesa
          self.nomeCadaver = nomeCadaver
          self.simbCadaver = simbCadaver
          self.si = si
     
     def tomarDano(self, valor):
          self.hp -= valor
          
     def morrer(self):
          if self.hp <= 0:
               self.si.nome = self.nomeCadaver
               self.si.simb = self.simbCadaver
               self.si.denso = False
               self.si.cor_fg = Cores.VERMELHO_ESCURO
               self.si.AI = None
     
     def morreu(self):
          if self.hp <= 0:
               return True
          else:
               return False