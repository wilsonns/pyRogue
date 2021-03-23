import pygame as pg
from Mapa import Mapa
from Entidade import Entidade
from AI import AI, AIJogador,AIRand, AIHostil
import Cores
from Turnos import *
from Console import Console,Mensagem
from Atacador import Atacador
from Destrutivel import Destrutivel



class Engine:
     def __init__(self, largura, altura, tile_tamanho):
          pg.init()
          self.turno = NOVO_TURNO
          self.largura = largura
          self.altura = altura
          self.tile_tamanho = tile_tamanho 
          self.fonte =pg.font.SysFont("Arial",self.tile_tamanho)
          self.fontemsg =pg.font.SysFont("Arial",int(self.tile_tamanho/3))
          self.debug = False
          
          self.tela = pg.display.set_mode((640, 480))
          self.mapa = Mapa(self.largura*5, self.altura*5,self.fonte,self.tile_tamanho,self.fontemsg)
          self.console = Console(640,64,self.tile_tamanho,self.tela, self.fonte,self)
          
          self.jogador = Entidade(15,15,"Jogador","@",Cores.ROSA,self.tela,self.fonte,self.tile_tamanho)
          self.jogador.setAI(AIJogador(self.jogador,self.mapa,self.tela,self.console,self))
          
          self.jogador.setDestrutivel(Destrutivel(25010,1,"Cadaver do"+self.jogador.nome,"%",self.jogador.si))
          self.jogador.setAtacador(Atacador(3,self.jogador.si))
          
          self.monstro = Entidade(2,2,"Orc","O",Cores.transparente(Cores.VERDE,10),self.tela,self.fonte,self.tile_tamanho)
          self.monstro.setAI(AIHostil(self.monstro,self.mapa,self.console,self))
          self.monstro.setDestrutivel(Destrutivel(10,1,"Cadaver de Orc","%",self.monstro.si))
          self.monstro.setAtacador(Atacador(3,self.monstro.si))
          
          self.mapa.entidades.append(self.jogador)
          self.mapa.entidades.append(self.monstro)
          self.clock = pg.time.Clock()
          
          
     def render(self):                   
          for entidade in self.mapa.entidades:
               entidade.render(self.console.port)
          
     def atualizar(self):
          if self.turno == TURNO_JOGADOR or self.turno == NOVO_TURNO:
               if self.jogador.atualizar() == True:
                    self.turno = TURNO_INIMIGO
          if self.turno == TURNO_INIMIGO:    
               for entidade in self.mapa.entidades:
                    if entidade.AI and entidade != self.jogador:                         
                         if entidade.destrutivel.morreu() == True:
                             self.console.msgs.append(entidade.nome+ " morreu!")
                             entidade.destrutivel.morrer()
                             self.console.msgs.append(entidade.nome+ " morreu!")
                             
                         else:
                             entidade.AI.atualizar()
                             
                      
               self.turno = TURNO_JOGADOR
          
          self.clock.tick(20)
               
               