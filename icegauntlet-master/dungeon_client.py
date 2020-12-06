#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=E0401
# pylint: disable=C0413
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=W0221

import sys
import atexit
import Ice
import game
import game.common
import game.screens
import game.pyxeltools
import game.orchestration

Ice.loadSlice('../IceGauntlet.ice')

import IceGauntlet

EXIT_OK = 0
BAD_COMMAND_LINE = 1

DEFAULT_HERO = game.common.HEROES[0]

class RemoteDungeonMap(Ice.Application, IceGauntlet.Dungeon):
    def __init__(self, argv):
        self.mapproxy = None

    @property
    def next_room(self):
        print('GETTING ROOM!!')
        archivo = open("./dungeonFile.txt", "r")
        proxy = archivo.read()
        archivo.close()

        broker = self.communicator()
        address = broker.stringToProxy(proxy)
        self.mapproxy = IceGauntlet.DungeonPrx.checkedCast(address)
        if not self.mapproxy:
            raise RuntimeError("Invalid proxy")

        mapdata = self.mapproxy.getRoom()
        return mapdata

    @property
    def finished(self):
        return False

class Client(Ice.Application):
    def run(self, address):
        dungeon = RemoteDungeonMap(address)
        game.pyxeltools.initialize()
        gauntlet = game.Game(self, dungeon)
        gauntlet.add_state(game.screens.TileScreen, game.common.INITIAL_SCREEN)
        gauntlet.add_state(game.screens.StatsScreen, game.common.STATUS_SCREEN)
        gauntlet.add_state(game.screens.GameScreen, game.common.GAME_SCREEN)
        gauntlet.add_state(game.screens.GameOverScreen, game.common.GAME_OVER_SCREEN)
        gauntlet.add_state(game.screens.GoodEndScreen, game.common.GOOD_END_SCREEN)
        gauntlet.start()

        return EXIT_OK


@atexit.register
# pylint: disable=W0613
def bye(*args, **kwargs):
    '''Exit callback, use for shoutdown'''
    print('Thanks for playing!')
# pylint: enable=W0613

if __name__ == '__main__':
    sys.exit(Client().main(sys.argv))
