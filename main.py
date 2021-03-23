import pygame as pg
from Entidade import Entidade
from Engine import Engine
import Cores
import Console

engine = Engine(11,26,96)

tile_tamanho = engine.tile_tamanho

'''
engine.mapa.cavar(1,3,1,7)
engine.mapa.cavar(2,2,7,14)
engine.mapa.cavar(1,3,14,18)
engine.mapa.cavar(7,10,1,7)
engine.mapa.cavar(1,8,3,3)
engine.mapa.cavar(6,6,3,18)
engine.mapa.cavar(1,3,14,18)
engine.mapa.cavar(4,4,10,10)
engine.mapa.cavar(6,9,12,18)
engine.mapa.cavar(2,8,17,17)
'''
engine.mapa.cavar(1,engine.mapa.largura-2, 1, engine.mapa.altura-2)
while True:
     engine.console.render(engine.jogador)
     engine.atualizar()
     #Framelimiter