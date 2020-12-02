#!/usr/bin python3
# -*- coding: utf-8 -*-

# pylint: disable=W1203
# pylint: disable=W0613

import sys
import Ice
Ice.loadSlice('../IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import IceGauntlet
import json
import random
import signal
import string
import logging
import os.path

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
        self.autenticacion = Client()
        self.autenticacion.run(argv)
        self._maps_ = {}
        if os.path.exists(MAPS_FILE):
            self.refresh()
        else:
            self.__commit__()

    def refresh(self, *args, **kwargs):
        '''Reload user DB to RAM'''
        
        ##Poner para que se impriman los comentarios
        logging.debug('Reloading user database')
        with open(MAPS_FILE, 'r') as contents:
            self._maps_ = json.load(contents)
        self._active_tokens_ = set([
            map.get(CURRENT_TOKEN, None) for map in self._vecMaps_.values()
        ])

    def __commit__(self):
        logging.debug('Map database updated!')
        with open(MAPS_FILE, 'w') as contents:
            json.dump(self._vecMaps_, contents, indent=4, sort_keys=True)

    def publish(self, token, roomData, current=None):
        validClient = self.autenticacion.isValid(token)
        print(validClient)
        if not validClient:
            raise IceGauntlet.Unauthorized()
        #print(roomData)
        try:
            map = json.loads(roomData)
            nameMap = map["room"]
        except:
            raise ValueError("Invalid name")
        
        #print(nameMap)
        if nameMap in self._vecMaps_:
            raise IceGauntlet.RoomAlreadyExists()

        self._vecMaps_[nameMap] = {}
        self._vecMaps_[nameMap]["token"] = token
        self._vecMaps_[nameMap]["roomData"] = roomData
        self.__commit__()
        #print(self._vecMaps_)

    def remove(self, token, roomName, current=None):
        validClient = self.autenticacion.isValid(token)
        print(validClient)
        if not validClient:
            raise IceGauntlet.Unauthorized()
        
        if roomName not in self._vecMaps_:
            raise IceGauntlet.RoomNotExists()
        
        del self._vecMaps_[roomName]
        self.__commit__()

##Modificar el juego de Tobias para que haga de cliente y cuando le des a ejecutar
##Conecte con este servidor y le de un mapa aleatorio o que pueda elegirlo

#class DungeonI(IceGauntlet.Dungeon):
 #   def getRoom(self, current=none):
        #llamar al vector de mapas del RoomManagerI
        #convertir el diccionario en una lista y sacar un elemento al azar

class Client(Ice.Application):
    def run(self, argv): 
        base = self.communicator().stringToProxy(argv[1])
        autenticacion = IceGauntlet.AuthenticationPrx.checkedCast(base)
    
        if not autenticacion:
            raise RuntimeError("Invalid proxy")
        
        self.proxy = autenticacion

        return 0
    
    def isValid(self, token):
        return self.proxy.isValid(token)

#Implementar otro sirviente para hacer el Dungeon
class Server(Ice.Application):
    '''
    Authentication Server
    '''
    def run(self, args):
        '''
        Server loop
        '''
        logging.debug('Initializing server...')
        servant = RoomManagerI(args)
        #servant1 = DungeonI(args)
        adapter = self.communicator().createObjectAdapter('RoomManagerAdapter')
        proxy = adapter.add(servant, self.communicator().stringToIdentity('default'))
        #proxyDungeon = adapter.add(servant1, self.communicator().stringToIdentity('juego'))
        adapter.addDefaultServant(servant, '')
        adapter.activate()
        logging.debug('Adapter ready, servant proxy: {}'.format(proxy))
        print('"{}"'.format(proxy), flush=True)
        #print('"{}"'.format(proxyDungeon), flush=True)
        logging.debug('Entering server loop...')        
        #logging.debug('Entering server loop...')
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))