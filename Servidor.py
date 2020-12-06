#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=E0401
# pylint: disable=C0413
# pylint: disable=C0103
# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=W0221

import sys
import json
import random
import logging
import os.path
import Ice
Ice.loadSlice('IceGauntlet.ice')

import IceGauntlet


MAPS_FILE = 'maps.json'
TOKEN_SIZE = 40
CURRENT_TOKEN = 'current_token'

EXIT_OK = 0
EXIT_ERROR = 1
class RoomManagerI(IceGauntlet.RoomManager):
    def __init__(self, argv):
        self._users_ = {}
        self._vecmaps_ = {}
        self._active_tokens_ = set()
        self.auth = Client()
        self.auth.run(argv)
        self._maps_ = {}
        if os.path.exists(MAPS_FILE):
            self.refresh()
        else:
            self.__commit__()

    def refresh(self):
        '''Reload user DB to RAM'''
        with open(MAPS_FILE, 'r') as contents:
            self._vecmaps_ = json.load(contents)
        self._active_tokens_ = set([
            map.get(CURRENT_TOKEN, None) for map in self._vecmaps_.values()])

    def __commit__(self):
        with open(MAPS_FILE, 'w') as contents:
            json.dump(self._vecmaps_, contents, indent=4, sort_keys=True)

    def publish(self, token, roomData, current=None):
        validclient = self.auth.isValid(token)
        logging.debug(validclient)
        if not validclient:
            raise IceGauntlet.Unauthorized()
        try:
            map = json.loads(roomData)
            namemap = map["room"]
        except:
            raise ValueError("Invalid name")
        if namemap in self._vecmaps_:
            raise IceGauntlet.RoomAlreadyExists()
        self._vecmaps_[namemap] = {}
        self._vecmaps_[namemap]["token"] = token
        self._vecmaps_[namemap]["roomData"] = roomData
        self.__commit__()

    def remove(self, token, roomName, current=None):
        validclient = self.auth.isValid(token)
        logging.debug(validclient)
        if not validclient:
            raise IceGauntlet.Unauthorized()
        if roomName not in self._vecmaps_:
            raise IceGauntlet.RoomNotExists()
        del self._vecmaps_[roomName]
        self.__commit__()
    def getvecmaps(self):
        return self._vecmaps_
class DungeonI(IceGauntlet.Dungeon):
    def __init__(self, argv):
        self.servant = argv
    def getRoom(self, current=None):
        vectormapas = self.servant.getvecmaps()
        randommap = random.sample(list(vectormapas.values()), 1)
        jsonmap = json.dumps(randommap[0])
        return jsonmap

class Client(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        address = broker.stringToProxy(argv[1])
        auth = IceGauntlet.AuthenticationPrx.checkedCast(address)
        if not auth:
            raise RuntimeError("Invalid proxy")
        self.proxy = auth
        return 0
    def isValid(self, token):
        return self.proxy.isValid(token)
class Server(Ice.Application):
    def run(self, args):
        servant = RoomManagerI(args)
        servantdungeon = DungeonI(servant)
        adapter = self.communicator().createObjectAdapter('RoomManagerAdapter')
        proxy = adapter.add(servant, self.communicator().stringToIdentity('RoomManager'))
        proxydungeon = adapter.add(servantdungeon, self.communicator().stringToIdentity('Dungeon'))
        adapter.addDefaultServant(servant, '')
        adapter.activate()
        print('"{}"'.format(proxy), flush=True)
        file = open("icegauntlet-master/dungeonFile.txt", "w")
        file.write('{}'.format(proxydungeon))
        file.close()

        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


if __name__ == '__main__':
    APP = Server()
    sys.exit(APP.main(sys.argv))
