import pygame as pg
import Cores

class Tile:
     def __init__(self, x, y, parede):
          self.x = x
          self.y = y
          self.parede = parede
          self.cor_fg = Cores.BRANCO
          self.cor_bg = Cores.PRETO
          
 
class Nodo(Tile):
     def __init__(self, x,y):
          self.x = x
          self.y = y
          self.f = 0
          self.g = 0
          self.h = 0
          self.vizinhos = []
          self.pai = None
          
     def __eq__(self, outro):
          if outro != None and self.x == outro.x and self.y == outro.y:
               return True
          else:
               return False
          
     def definirVizinhos(self, mapa):
          for x in range(self.x-1,self.x+2):
               for y in range(self.y-1,self.y+2):
                    tile = mapa.tiles[x][y]
                    if mapa.podeAndar(tile) and tile.x != self.x and tile.y != self.y:
                         self.vizinhos.append(tile)
                         
          
          
      
class Mapa:
     def __init__(self,largura,altura, fonte, tile_tamanho,fontemsg):
          self.largura = largura
          self.altura = altura
          
          self.fonte = fonte
          self.tile_tamanho = tile_tamanho 
          self.entidades = []
          self.tiles = []
          
          self.fontemsg = fontemsg
          
          for i in range(largura):
               self.tiles.append([])
               for j in range(altura):
                    self.tiles[i].append(None)
          for i in range(largura):
               for j in range(altura):
                    self.tiles[i][j] = Tile(i,j,True)
           
     def render(self,tela):
               '''for x in range(self.largura):
                    for y in range(self.altura):
                         tile = self.tiles[x][y]
                         rectext= pg.Rect((0,0),(self.tile_tamanho,self.tile_tamanho))
                         rectext.move_ip((tile.x*self.tile_tamanho, tile.y*self.tile_tamanho))
                         pg.draw.rect(tela,Cores.BRANCO,rectext)
                         rectint= pg.Rect((0,0),(self.tile_tamanho-2,self.tile_tamanho-2))
                         rectint.move_ip(((tile.x*self.tile_tamanho)+1, (tile.y*self.tile_tamanho)-1))
                         pg.draw.rect(tela,tile.cor_bg,rectint)
                         if tile.parede == True:  
                              pared = self.fonte.render("#",1,tile.cor_fg)
                              tela.blit(pared,(tile.x*self.tile_tamanho,tile.y*self.tile_tamanho))'''
                         
                         
     def cavar(self, x1,x2,y1,y2):
           for y in range(y1,y2+1):
                for x in range(x1,x2+1):
                     self.tiles[x][y].parede = False
                     
     def eParede(self, tile:Tile):
          if tile.parede == True:
               return True
          else:
               return False

     def temEntidade(self,tile:Tile):
          for entidade in self.entidades:
               if entidade.x == tile.x and entidade.y == tile.y and entidade.denso == True:
                    return entidade
               else:
                    continue
          return None
                    
     def podeAndar(self, tile:Tile):
          if self.eParede(tile) == False and self.temEntidade(tile)==False:
               return True
          else:
               return False
               
               
class MapaPath(Mapa):
     def __init__(self,largura,altura,tile_tamanho, euclideana = True):
          self.largura = largura
          self.altura = altura
          self.tile_tamanho = tile_tamanho
          self.tiles = []
          self.euclideana = euclideana
          for i in range(largura):
               self.tiles.append([])
               for j in range(altura):
                    self.tiles[i].append(None)
          for i in range(largura):
               for j in range(altura):
                    self.tiles[i][j] = Nodo(i,j)
          for i in range(largura):
               for j in range(altura):
                    tile = self.tiles[i][j]
                    if j > 0:
                         tile.vizinhos.append(self.tiles[i][j-1])
                    
                    if j < self.altura-1:
                         tile.vizinhos.append(self.tiles[i][j+1])
                    
                    if i > 0:
                         tile.vizinhos.append(self.tiles[i-1][j])
                    
                    if i < self.largura-1:
                         tile.vizinhos.append(self.tiles[i+1][j])
                    
                    if euclideana == True:
                         if j>0 and i > 0:
                              tile.vizinhos.append(self.tiles[i-1][j-1])
                         
                         if j < self.altura-1 and i>0:
                              tile.vizinhos.append(self.tiles[i-1][j+1])
                         
                         if i < self.largura-1 and j > 0:
                              tile.vizinhos.append(self.tiles[i+1][j-1])
                         
                         if i < self.largura-1 and j < self.altura-1:
                              tile.vizinhos.append(self.tiles[i+1][j+1])                   