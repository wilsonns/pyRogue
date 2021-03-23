import pygame as pg
import Entidade
import random

class Atacador:
     def __init__(self, forca,si):
          self.forca = forca
          self.si = si
          
     def atacar(self, alvo:Entidade):
          if alvo.destrutivel:
               dano = random.randint(0,5)+self.forca
               dano -= alvo.destrutivel.defesa
               alvo.destrutivel.tomarDano(dano)
               
               return dano
          
          
          
