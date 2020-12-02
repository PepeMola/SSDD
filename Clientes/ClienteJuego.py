#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W1203
# pylint: disable=W0613

import sys
from sys import argv
import Ice
Ice.loadSlice('../IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413

import IceGauntlet

#Estos import son los de dungeon_local
import atexit
import logging
import argparse

import game
import game.common
import game.screens
import game.pyxeltools
import game.orchestration


DEFAULT_HERO = game.common.HEROES[0]

class ClienteMapas(Ice.Application):
    '''
    Este cliente va a ser el que pida un mapa o lista de mapas y luego arranque el juego
    '''
    def run(self, argv):
        
        broker = self.communicator()
        address = broker.stringToProxy(argv[1])
        server_gestorMapas = IceGauntlet.DungeonPrx.checkedCast(address) #Interface Dungeon --> IceGauntlet.ice

        if not server_gestorMapas:
            raise RuntimeError("Invalid proxy")

        room = server_gestorMapas.getRoom()

        with open("../icegauntlet-master/assets/room.json", "w") as fd:
            fd.write(room)
        fd.close()

        print("Mapa guardado en /assests/.\n") 

        roomList = []
        roomList.append("room.json")

        game.pyxeltools.initialize()
        dungeon = game.DungeonMap(roomList) #Tiene que recibir una lista con al menos 1 mapa, maquina, palabra de Pillete
        gauntlet = game.Game(DEFAULT_HERO, dungeon)
        gauntlet.add_state(game.screens.TileScreen, game.common.INITIAL_SCREEN)
        gauntlet.add_state(game.screens.StatsScreen, game.common.STATUS_SCREEN)
        gauntlet.add_state(game.screens.GameScreen, game.common.GAME_SCREEN)
        gauntlet.add_state(game.screens.GameOverScreen, game.common.GAME_OVER_SCREEN)
        gauntlet.add_state(game.screens.GoodEndScreen, game.common.GOOD_END_SCREEN)
        gauntlet.start()

if __name__ == "__main__":
    clienteMapas = ClienteMapas()
    sys.exit(ClienteMapas().main(sys.argv))   