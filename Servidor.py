#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import random
import logging
import os.path
import Ice
Ice.loadSlice('IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413

import IceGauntlet


MAPS_FILE = 'maps.json'
TOKEN_SIZE = 40
CURRENT_TOKEN = 'current_token'

EXIT_OK = 0
EXIT_ERROR = 1
class RoomManagerI(IceGauntlet.RoomManager):
    def __init__(self, argv):
        self._users_ = {}
        self._vecMaps_ = {}
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
            self._vecMaps_ = json.load(contents)
        self._active_tokens_ = set([
            map.get(CURRENT_TOKEN, None) for map in self._vecMaps_.values()])

    def __commit__(self):
        with open(MAPS_FILE, 'w') as contents:
            json.dump(self._vecMaps_, contents, indent=4, sort_keys=True)

    def publish(self, token, roomData, current=None):
        validClient = self.auth.isValid(token)
        logging.debug(validClient)
        if not validClient:
            raise IceGauntlet.Unauthorized()
        try:
            map = json.loads(roomData)
            nameMap = map["room"]
        except:
            raise ValueError("Invalid name")
        if nameMap in self._vecMaps_:
            raise IceGauntlet.RoomAlreadyExists()
        self._vecMaps_[nameMap] = {}
        self._vecMaps_[nameMap]["token"] = token
        self._vecMaps_[nameMap]["roomData"] = roomData
        self.__commit__()

    def remove(self, token, roomName, current=None):
        validClient = self.auth.isValid(token)
        logging.debug(validClient)
        if not validClient:
            raise IceGauntlet.Unauthorized()
        if roomName not in self._vecMaps_:
            raise IceGauntlet.RoomNotExists()
        del self._vecMaps_[roomName]
        self.__commit__()
    def getVecMaps(self):
        return self._vecMaps_
class DungeonI(IceGauntlet.Dungeon):
    def __init__(self, argv):
        self.servant = argv
    def getRoom(self, current=None):
        vectorMapas = self.servant.getVecMaps()
        randomMap = random.sample(list(vectorMapas.values()), 1)
        jsonMap = json.dumps(randomMap[0])
        return jsonMap

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
        servantDungeon = DungeonI(servant)
        adapter = self.communicator().createObjectAdapter('RoomManagerAdapter')
        proxy = adapter.add(servant, self.communicator().stringToIdentity('RoomManager'))
        proxyDungeon = adapter.add(servantDungeon, self.communicator().stringToIdentity('Dungeon'))
        adapter.addDefaultServant(servant, '')
        adapter.activate()
        print('"{}"'.format(proxy), flush=True)
        file = open("icegauntlet-master/dungeonFile.txt", "w")
        file.write('{}'.format(proxyDungeon))
        file.close()

        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
