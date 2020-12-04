#!/usr/bin python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('IceGauntlet.ice')

import IceGauntlet
import json
import random
import signal
import string
import logging
import os.path
import logging

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
        validClient = self.autenticacion.isValid(token)
        logging.debug(validClient)
        if not validClient:
            raise IceGauntlet.Unauthorized()
        
        if roomName not in self._vecMaps_:
            raise IceGauntlet.RoomNotExists()
        
        del self._vecMaps_[roomName]
        self.__commit__()

<<<<<<< HEAD:Servidor.py
class DungeonI(IceGauntlet.Dungeon):
    def __init__(self, argv):
        self.servant = argv
        
    def getRoom(self, current = None):
        vectorMapas = self.servant._vecMaps_
        valores = vectorMapas.values()
        print(valores)

    def isEmpty(self, vectorMapas):
        for element in vectorMapas:
            if element:
                randomMap = random.choice(vectorMapas.keys())
                print(randomMap)
                return randomMap
            else:
                raise IceGauntlet.RoomNotExists()
    
        return None  


=======
>>>>>>> 70121a26f785d1c3f19866493083dca170f2abbd:Servidores/Servidor.py
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
    
<<<<<<< HEAD:Servidor.py
=======
def publish():
    '''
    Do the stuff
    '''
    
>>>>>>> 70121a26f785d1c3f19866493083dca170f2abbd:Servidores/Servidor.py

class Server(Ice.Application):
    def run(self, args):
        '''
        Server loop
        '''
        a_logger = logging.getLogger()
        a_logger.setLevel(logging.DEBUG)
<<<<<<< HEAD:Servidor.py
        output_file_handler = logging.FileHandler("Servidor.log")
=======
        output_file_handler = logging.FileHandler("Servidor.py")
>>>>>>> 70121a26f785d1c3f19866493083dca170f2abbd:Servidores/Servidor.py
        stdout_handler = logging.StreamHandler(sys.stdout)
        a_logger.addHandler(output_file_handler)
        a_logger.addHandler(stdout_handler)

        a_logger.debug('Initializing server...')
        servant = RoomManagerI(args)
<<<<<<< HEAD:Servidor.py
        servantDungeon = DungeonI(servant)
        adapter = self.communicator().createObjectAdapter('RoomManagerAdapter')
        proxy = adapter.add(servant, self.communicator().stringToIdentity('RoomManager'))
        proxyDungeon = adapter.add(servantDungeon, self.communicator().stringToIdentity('Dungeon'))
=======
        adapter = self.communicator().createObjectAdapter('RoomManagerAdapter')
        proxy = adapter.add(servant, self.communicator().stringToIdentity('default'))
>>>>>>> 70121a26f785d1c3f19866493083dca170f2abbd:Servidores/Servidor.py
        adapter.addDefaultServant(servant, '')
        adapter.activate()
        logging.debug('Adapter ready, servant proxy: {}'.format(proxy))
        print('"{}"'.format(proxy), flush=True)
<<<<<<< HEAD:Servidor.py
        print('"{}"'.format(proxyDungeon), flush=True)
=======
>>>>>>> 70121a26f785d1c3f19866493083dca170f2abbd:Servidores/Servidor.py

        logging.debug('Entering server loop...') 
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
<<<<<<< HEAD:Servidor.py
=======
Initializing server...
Reloading user database
Adapter ready, servant proxy: default -t -e 1.1:tcp -h 192.168.1.66 -p 40365 -t 60000
Entering server loop...
>>>>>>> 70121a26f785d1c3f19866493083dca170f2abbd:Servidores/Servidor.py
