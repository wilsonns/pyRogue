import pygame as pg
import Cores

class Mensagem:
     def __init__(self,msg, fonte,tela):
          self.msg = msg
          self.fonte = fonte
          self.tela = tela
     
     def render(self, y):     
          self.tela.blit(self.fonte.render(self.msg,1,Cores.BRANCO),(500,y))
     
class Viewport:
     def __init__(self,largura,altura,tela, engine,tile_tamanho,fonte):
          self.largura = largura
          self.altura = 20
          self.tela = tela
          self.engine = engine
          self.x = 0
          self.y = 0
          self.tile_tamanho = tile_tamanho
          self.fonte = pg.font.SysFont("Arial",int(self.tile_tamanho))
          
     def render(self,jogador,mapa):
          self.x = jogador.x-int(self.largura/2)
          self.y = jogador.y-int(self.altura/2)-1
          if self.x < 0:
          	self.x = 0
          if self.y < -1:
          	self.y = -1
          
          for i in range(0,self.largura):
               for j in range(1,self.altura):
                    tile = mapa.tiles[i+self.x][j+self.y]
                    rectext= pg.Rect((0,0),(self.tile_tamanho,self.tile_tamanho))
                    rectext.move_ip((i*self.tile_tamanho, j*self.tile_tamanho))
                    pg.draw.rect(self.tela,Cores.BRANCO,rectext)
                    rectint= pg.Rect((0,0),(self.tile_tamanho-2,self.tile_tamanho-2))
                    rectint.move_ip(((i*self.tile_tamanho)+1, (j*self.tile_tamanho)-1))
                    pg.draw.rect(self.tela,tile.cor_bg,rectint)
                    if tile.parede == True:  
                         pared = self.fonte.render("#",1,tile.cor_fg)
                         self.tela.blit(pared,(i*self.tile_tamanho,j*self.tile_tamanho))

class Console:
     def __init__(self, largura, altura, tile_tamanho, tela, fonte,engine):
          self.largura = largura
          self.altura = altura
          self.tela = tela
          self.tile_tamanho = tile_tamanho
          self.fonte = pg.font.SysFont("Arial",int(self.tile_tamanho/5))
          self.msgs = []
          self.engine = engine
          self.port = Viewport(engine.largura,altura-engine.altura,self.tela,self.engine,self.tile_tamanho,self.fonte)          
          self.px = 0
          self.py = 0
          
     def render(self,jogador):
          
          self.port.render(jogador,self.engine.mapa)
          self.engine.render()
          
          ###GUI###
          rectext= pg.Rect((0,0),(self.tile_tamanho*self.largura,self.tile_tamanho*3))
          rectext.move_ip((0*self.tile_tamanho, 20*self.tile_tamanho))
          pg.draw.rect(self.tela,Cores.BRANCO,rectext)
          
          con = pg.Rect((0,0),((self.tile_tamanho*self.largura)-4,(self.tile_tamanho*3)-4))
          con.move_ip(((0*self.tile_tamanho)+2, (20*self.tile_tamanho)+2))
          pg.draw.rect(self.tela,Cores.PRETO,con)
          
          barrabx = pg.Rect((0,0),(self.tile_tamanho*5,self.tile_tamanho/2))
          barrabx.move_ip((2,(20*self.tile_tamanho)))
          pg.draw.rect(self.tela, Cores.VERMELHO_ESCURO,barrabx)
          
          
          barracm = pg.Rect((0,0),(int(self.tile_tamanho*5)*(jogador.destrutivel.hp/jogador.destrutivel.maxHp),self.tile_tamanho/2))
          barracm.move_ip((2,(20*self.tile_tamanho)))
          pg.draw.rect(self.tela, Cores.VERMELHO,barracm)
          
          self.tela.blit(self.fonte.render(jogador.nome,1,Cores.BRANCO),(5,20*self.tile_tamanho))
          self.tela.blit(self.fonte.render(str(jogador.destrutivel.hp)+"/"+str(jogador.destrutivel.maxHp),1,Cores.BRANCO),(int((2+(self.tile_tamanho*5)/2)),int(20*self.tile_tamanho)+int(self.tile_tamanho/4)))
          
          self.tela.blit(self.fonte.render("X:"+str(jogador.x)+"Y:"+str(jogador.y),1,Cores.BRANCO),(5,21*self.tile_tamanho))
          self.tela.blit(self.fonte.render("pX:"+str(self.px)+"pY:"+str(self.py),1,Cores.BRANCO),(5,21.5*self.tile_tamanho))
          self.tela.blit(self.fonte.render("pXf:"+str(self.px+self.port.x)+"pYf:"+str(self.py+self.port.y),1,Cores.BRANCO),(5,22*self.tile_tamanho))
          
          i = 0
          if len(self.msgs) < 11:
               for msg in self.msgs:
                    msg.render(i+(20*self.tile_tamanho))
                    i += int(self.tile_tamanho/4)
          else:
               self.msgs.pop(0)
               for msg in self.msgs:
                    msg.render(i+(20*self.tile_tamanho))
                    i += int(self.tile_tamanho/4)
                    
          pg.display.flip()
                    
               