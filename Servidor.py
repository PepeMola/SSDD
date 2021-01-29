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
import uuid
import fnmatch
import IceStorm

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
        self._id_ = str(uuid.uuid4()) #Identificador unico para nuestro servicio de gestion de mapas
        self._maps_path_ = "./icegauntlet-master/assets" 
        self._mapList_ = self.llenarMapas(self._maps_path_) #Lista de mapas al iniciar RoomManager
        if os.path.exists(MAPS_FILE):
            self.refresh()
        else:
            self.__commit__()

    def llenarMapas(self, path, current = None): #Metodo para llenar la lista _mapList_
        listaMapas = []
        for mapa in os.listdir(path):
            if fnmatch.fnmatch(mapa, '*.json'):
                listaMapas.append(mapa)
        return listaMapas

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
        validclient = self.auth.getOwner(token)
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
        self._vecmaps_[namemap]["user"] = validclient
        self._vecmaps_[namemap]["roomData"] = roomData
        self.__commit__()

        '''
        Aqui debemos crear una instancia del RoomManagerSync para propagar newRoom()
        la propagacion debe contener: 
            1. Nombre del mapa
            2. Id de la instancia uuid
        '''

    def remove(self, token, roomName, current=None):
        validclient = self.auth.getOwner(token)
        logging.debug(validclient)

        if not validclient:
            raise IceGauntlet.Unauthorized()
        
        if roomName not in self._vecmaps_:
            raise IceGauntlet.RoomNotExists()
        del self._vecmaps_[roomName]
        self.__commit__()
        '''
        Aqui debemos crear una instancia del RoomManagerSync para propagar removedRoom()
        la propagacion debe contener: 
            1. Nombre del mapa
        '''
    def getvecmaps(self, current = None):
        return self._vecmaps_

    def getRoom(self, roomName, current=None):
        vectorMapas = self._mapList_
        if roomName in vectorMapas:
            jsonMap = json.dumps(roomName)
            return str(jsonMap)

    def availableRooms(self, current = None):
        availableMaps = self._mapList_
        return availableMaps
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

    def getOwner(self, token):
        return self.proxy.getOwner(token)
class Server(Ice.Application):
    def run(self, args):
        qos = {}
        servant = RoomManagerI(args)
        servantdungeon = DungeonI(servant)
        servantEvents = RoomManagerSyncI(servant._id_) #Pasamos id del RoomManager para distinguirlo
        adapter = self.communicator().createObjectAdapter('RoomManagerAdapter')
        #proxy = adapter.add(servant, self.communicator().stringToIdentity('RoomManager'))
        proxy = adapter.addWithUUID(servant)
        #proxydungeon = adapter.add(servantdungeon, self.communicator().stringToIdentity('Dungeon'))
        proxydungeon = adapter.addWithUUID(servantdungeon)
        #Proxy de canal de eventos
        proxyEvents = adapter.addWithUUID(servantEvents)
        adapter.addDefaultServant(servant, '')
        adapter.activate()
        print('"{}"'.format(proxy), flush=True)
        file = open("icegauntlet-master/dungeonFile.txt", "w")
        file.write('{}'.format(proxydungeon))
        file.close()

        room_manager = IceGauntlet.RoomManagerPrx.uncheckedCast(proxy) #Instanciamos el manager
        servantEvents._room_manager_ = room_manager
        servantEvents._topic_channel_.subscribeAndGetPublisher(qos, proxyEvents)
        servantEvents._publisher_.hello(room_manager, servant._id_)
        
        print("Esperando eventos...")

        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0

class RoomManagerSyncI(Ice.Application, IceGauntlet.RoomManagerSync):
    def __init__(self, identity):
        self._id_ = identity
        self.room_manager = None
        self._topic_name_ = "RoomManagerSyncChannel"
        self._topic_manager_ = self.get_topic_manager()
        self._topic_channel_ = self.get_topic()
        self._publisher_ = self.get_publisher()
        self._pool_servers_ = {}

    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property {} not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def get_topic(self):
        if not self._topic_manager_:
            print('Invalid proxy')
            return 2
        try:
            topic = self._topic_manager_.retrieve(self._topic_name_)
        except IceStorm.NoSuchTopic:
            print("no such topic found, creating")
            topic = self._topic_manager_.create(self._topic_name_)
        return topic

    def get_publisher(self):
        publisher = self.get_topic().getPublisher()
        RoomManagerSync = IceGauntlet.RoomManagerSyncPrx.uncheckedCast(publisher)
        return RoomManagerSync

    def hello(self, RoomManager, RoomManagerId, current=None):
        if RoomManagerId not in self._pool_servers_:
            self._pool_servers_[RoomManagerId] = RoomManager
            print("Hello ", RoomManagerId)
            self._publisher_.announce(self._room_manager_, self._id_)
             
    def announce(self, RoomManager, RoomManagerId, current=None):
        if RoomManagerId not in self._pool_servers_:
            self._pool_servers_[RoomManagerId] = RoomManager
            print("Hi my pana, my id is: ", RoomManagerId)
            room_storage = RoomManager.availableRooms()

            for map in room_storage:
                if map not in self._pool_servers_[RoomManagerId]._mapList_:
                    self._pool_servers_[RoomManagerId].getRoom(map)
                    print(map)

    def newRoom(self, roomName, RoomManagerId, current=None):
        if RoomManagerId in self._pool_servers_:
            room = self._pool_servers_[RoomManagerId].getRoom(roomName)
            #Añadir el mapa al almacen de mapas
            print("newRoom")
    
    def removedRoom(self, roomName, current=None):
        room = self._pool_servers_[RoomManagerId].getRoom(roomName)
        #Borrar el mapa del almacen
        print("removedRoom")


if __name__ == '__main__':
    APP = Server()
    sys.exit(APP.main(sys.argv))
