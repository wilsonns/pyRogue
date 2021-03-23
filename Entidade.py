import pygame as pg
import Cores
from AI import *
from Atacador import Atacador
from Destrutivel import Destrutivel

class Entidade:
     def __init__(self, x,y,nome, simb, cor_fg,tela,fonte,tile_tamanho,denso = True):
          self.x = x
          self.y = y
          self.nome =nome
          self.simb = simb
          self.cor_fg = cor_fg
          self.cor_bg = Cores.PRETO
          self.tela = tela
          self.fonte = fonte
          self.tile_tamanho = tile_tamanho
          self.AI = None
          self.denso = denso
          self.si = self
      
     def setAI(self, AI):
          self.AI = AI
          
     def setDestrutivel(self, destrutivel):
          self.destrutivel = destrutivel
          
     def setAtacador(self, atacador):
          self.atacador = atacador
          
     def render(self,port):
          x1 = port.x
          x2 = port.x+port.largura
          y1 = port.y
          y2 = port.y+port.altura
          if self.x > x1 and self.x < x2 and self.y > y1 and self.y < y2:
               
    
               rectext= pg.Rect((0,0),(self.tile_tamanho,self.tile_tamanho))
               rectext.move_ip(((self.x-port.x)*self.tile_tamanho, (self.y-port.y)*self.tile_tamanho))
               pg.draw.rect(self.tela,Cores.BRANCO,rectext)
               rectint= pg.Rect((0,0),(self.tile_tamanho-2,self.tile_tamanho-2))
               rectint.move_ip((((self.x-port.x)*self.tile_tamanho)+1, ((self.y-port.y)*self.tile_tamanho)-1))
               pg.draw.rect(self.tela,self.cor_bg,rectint)
               rend = self.fonte.render(self.simb,1,self.cor_fg)
               self.tela.blit(rend,((self.x-port.x)*self.tile_tamanho,(self.y-port.y)*self.tile_tamanho))#Render Entidadr
          
     def atualizar(self):
          if self.AI:
               if self.AI.atualizar() == True:
                         return True
               
          
     def mover(self, dx: int, dy: int):
          self.x = dx
          self.y = dy

