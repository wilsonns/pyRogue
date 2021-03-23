import pygame as pg
import Entidade
import Mapa
import math
import random
import Cores
from Console import Console, Mensagem

class AI:
     def __init__(self,
     si: Entidade,
     mapa:Mapa, console, engine,euclideana = True):
          self.si = si
          self.mapa = mapa
          self.mapa_path = Mapa.MapaPath(mapa.largura, mapa.altura, mapa.tile_tamanho, euclideana)
          self.fonte = pg.font.SysFont("Arial",int(self.mapa.tile_tamanho/5))
         
          self.console = console
          self.engine = engine
          self.tela = self.console.tela
     
     def mover(self, 
     dx:int,
     dy:int, 
     entidade:Entidade ):
          if self.mapa.eParede(self.mapa.tiles[dx][dy]) == False and self.mapa.temEntidade(self.mapa.tiles[dx][dy]) == None:
               entidade.mover(dx,dy)
          else:
               entidade = self.mapa.temEntidade(self.mapa.tiles[dx][dy]) 
               if entidade != None:
                    if entidade.destrutivel.morreu() == False:
                         dano = self.si.atacador.atacar(entidade)
                         self.console.msgs.append(Mensagem(self.si.nome + " ataca "+entidade.nome + " causando " +str(dano) + " dano!", self.fonte, self.tela))
                         if entidade.destrutivel.morreu():
                              self.console.msgs.append(Mensagem(entidade.nome + " Morreu!",self.fonte, self.tela))
                              entidade.destrutivel.morrer()
                              
     def acharCaminho(self,
          inicio:Mapa.Nodo, 
          objetivo:Mapa.Nodo):
               aberta = []
               aberta.append(inicio)
               fechada = []
               atual = inicio
               clock = pg.time.Clock()
               if self.engine.debug == True:
                    rectint= pg.Rect((0,0),(self.mapa.tile_tamanho-2,self.mapa.tile_tamanho-2))
                    rectint.move_ip(((objetivo.x*self.mapa.tile_tamanho)+1, (objetivo.y*self.mapa.tile_tamanho)-1))
                    pg.draw.rect(self.tela,Cores.VERMELHO,rectint)
               
               while len(aberta) > 0:
                    atual = aberta[0]
                    if self.engine.debug == True:
                         rectint= pg.Rect((0,0),(self.mapa.tile_tamanho-2,self.mapa.tile_tamanho-2))
                         rectint.move_ip(((atual.x*self.mapa.tile_tamanho)+1, (atual.y*self.mapa.tile_tamanho)-1))
                         pg.draw.rect(self.tela,Cores.VERDE_ESCURO,rectint)
                         desc = self.fonte.render("G:"+str(atual.g),1,Cores.PRETO)
                         self.tela.blit(desc,((atual.x*self.mapa.tile_tamanho)+5,(atual.y*self.mapa.tile_tamanho)+45))
                         desc = self.fonte.render("H:"+str(atual.h),1,Cores.PRETO)
                         self.tela.blit(desc,((atual.x*self.mapa.tile_tamanho)+45,(atual.y*self.mapa.tile_tamanho)+45))
                         desc = self.fonte.render("F:"+str(atual.f),1,Cores.PRETO)
                         self.tela.blit(desc,((atual.x*self.mapa.tile_tamanho)+5,(atual.y*self.mapa.tile_tamanho)+5))
                         pg.display.flip()
                         clock.tick(50)
                    
                    fechada.append(atual)
                    aberta.remove(atual)
               
                    if atual == objetivo:
                         caminho = []
                         nodo_atual = atual
                         while nodo_atual != inicio:
                              caminho.append(nodo_atual)
                              nodo_atual = nodo_atual.pai
                              
                              if self.engine.debug == True:
                                   rectint= pg.Rect((0,0),(self.tile_tamanho-2,self.tile_tamanho-2))
                                   rectint.move_ip(((nodo_atual.x*self.tile_tamanho)+1, (nodo_atual.y*self.tile_tamanho)-1))
                                   pg.draw.rect(self.tela,Cores.AZUL,rectint)
                                   pg.display.flip()
                                   clock.tick(70)
                         caminho.append(atual)
                         caminho.reverse()
                         caminho.pop(0)
                         self.caminho = caminho
                         for x in range(self.mapa_path.largura):
                              for y in range(self.mapa_path.altura):
                                    tile = self.mapa_path.tiles[x][y]
                                    tile.g = 0
                                    tile.h = 0
                                    tile.f = 0
                                    tile.pai = None
                         return True
                                   
                    for vizinho in atual.vizinhos:
                         if self.mapa.eParede(self.mapa.tiles[vizinho.x][vizinho.y]) == False and vizinho not in fechada and vizinho in aberta:
                              if vizinho.pai != None and vizinho.pai.g > self.calcularG(atual):
                                   vizinho.pai = atual
                                   vizinho.g = self.calcularG(vizinho)
                                   vizinho.h = self.calcularH(vizinho, objetivo)
                                   vizinho.f = self.calcularF(vizinho)
                         elif self.mapa.eParede(self.mapa.tiles[vizinho.x][vizinho.y]) == False and vizinho not in fechada and vizinho not in aberta:
                              vizinho.pai = atual
                              vizinho.g = self.calcularG(vizinho)
                              vizinho.h = self.calcularH(vizinho, objetivo)
                              vizinho.f = self.calcularF(vizinho)
                              aberta.append(vizinho)
                              if self.engine.debug == True:
                                   rectint= pg.Rect((0,0),(self.mapa.tile_tamanho-2,self.mapa.tile_tamanho-2))
                                   rectint.move_ip(((vizinho.x*self.mapa.tile_tamanho)+1, (vizinho.y*self.mapa.tile_tamanho)-1))
                                   pg.draw.rect(self.tela,Cores.VERDE,rectint)
                                   desc = self.fonte.render("G:"+str(vizinho.g),1,Cores.PRETO)
                                   self.tela.blit(desc,((vizinho.x*self.mapa.tile_tamanho)+5,(vizinho.y*self.mapa.tile_tamanho)+45))
                                   desc = self.fonte.render("H:"+str(vizinho.h),1,Cores.PRETO)
                                   self.tela.blit(desc,((vizinho.x*self.mapa.tile_tamanho)+45,(vizinho.y*self.mapa.tile_tamanho)+45))
                                   desc = self.fonte.render("F:"+str(vizinho.f),1,Cores.PRETO)
                                   self.tela.blit(desc,((vizinho.x*self.mapa.tile_tamanho)+5,(vizinho.y*self.mapa.tile_tamanho)+5))
                                   pg.display.flip()
                                   clock.tick(50)
                              
                    aberta.sort(key=lambda x:x.f) 
               for x in range(self.mapa_path.largura):
                     for y in range(self.mapa_path.altura):
                          tile = self.mapa_path.tiles[x][y]
                          tile.g = 0
                          tile.h = 0
                          tile.f = 0
                          tile.pai = None
               return False               
               
     def calcularG(self,nodo:Mapa.Nodo):
          if nodo.x != nodo.pai.x and nodo.y != nodo.pai.y:
               return nodo.pai.g+14
          else:
               return nodo.pai.g +10
          
     def calcularH(self, atual:Mapa.Nodo,objetivo:Mapa.Nodo):
          dx = atual.x - objetivo.x
          dy = atual.y - objetivo.y
          distancia = int(math.sqrt((dx*dx)+(dy*dy)))
          return distancia*10
     
     def calcularF(self, nodo:Mapa.Nodo):
          return nodo.g+nodo.h
                                               
class AIJogador(AI):
     def __init__(self,
     si: Entidade,
     mapa:Mapa, tela, console, engine):
          self.si = si
          self.mapa = mapa
          self.mapa_path = Mapa.MapaPath(mapa.largura, mapa.altura, mapa.tile_tamanho)
          self.tela = tela
          self.tile_tamanho = mapa.tile_tamanho
          self.fonte = pg.font.SysFont("Arial",int(self.mapa.tile_tamanho/5))
          self.caminho = []
          self.px = None
          self.py = None
          self.console = console
          self.engine = engine
 
     
                    
     def atualizar(self):
          for ev in pg.event.get():
               if ev.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    self.px = int(pos[0]/self.tile_tamanho)
                    self.console.px = self.px
                    self.px += self.console.port.x
                    self.py = int(pos[1]/self.tile_tamanho)
                    self.console.py = self.py
                    self.py += self.console.port.y
         
          if self.px == self.si.x and self.py == self.si.y:
               return False
               
          if len(self.caminho) >0:
               self.mover(self.caminho[0].x,self.caminho[0].y,self.si) 
               self.caminho.pop(0)
               return True
               
          elif len(self.caminho) >= 0 and self.px != None and self.py != None:
               if self.acharCaminho(self.mapa_path.tiles[self.si.x][self.si.y],self.mapa_path.tiles[self.px][self.py]) == True:
                    self.mover(self.caminho[0].x,self.caminho[0].y,self.si) 
                    self.caminho.pop(0)
                    self.px = None
                    self.py = None
                    return True
               else:
                    self.px = None
                    self.py = None
                    return True
               return False                                   

class AIHostil(AI):
     def acharAlvo(self):
          for entidade in self.mapa.entidades:
               if entidade != self.si:
                    self.alvo = entidade
                    
                    
     def atualizar(self):
          self.acharAlvo()
          self.acharCaminho(self.mapa_path.tiles[self.si.x][self.si.y],self.mapa_path.tiles[self.alvo.x][self.alvo.y])
          self.mover(self.caminho[0].x,self.caminho[0].y,self.si)
     
class AIRand(AI):
     def __init__(self, si:Entidade, mapa:Mapa):
          self.si = si
          self.mapa = mapa
     def atualizar(self):
          dx = random.randint(-1,1)
          dy = random.randint(-1,1)
          
          self.mover(self.si.x+dx,self.si.y+dy,self.si)
     