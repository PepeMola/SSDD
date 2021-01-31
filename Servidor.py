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
from os import remove
from os import path
import Ice
Ice.loadSlice('IceGauntlet.ice')

import IceGauntlet
import uuid
import fnmatch
import IceStorm
import tempfile
import psutil
import shutil

MAPS_FILE = 'maps.json'
TOKEN_SIZE = 40
CURRENT_TOKEN = 'current_token'
PATH_ROOMS = "./icegauntlet-master/assets"

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
        self._maps_path_ = PATH_ROOMS 
        self._mapList_ = self.llenarMapas(self._maps_path_) #Lista de mapas al iniciar RoomManager
        self.manager_sync = None

    def llenarMapas(self, path, current = None): #Metodo para llenar la lista _mapList_
        listaMapas = []
        for mapa in os.listdir(path):
            if fnmatch.fnmatch(mapa, '*.json'):
                listaMapas.append(mapa) 
        return listaMapas

    def publish(self, token, roomData, current=None):
        validclient = self.auth.getOwner(token)
        logging.debug(validclient)
        if not validclient:
            raise IceGauntlet.Unauthorized()
        map = {}
        try:
            map = json.loads(roomData)
            namemap = map["room"]
            map["user"] = validclient
            map["token"] = token #Habria que eliminarlo
        except:
            raise ValueError("Invalid name")
        if namemap in self._mapList_:
            raise IceGauntlet.RoomAlreadyExists()
        
        archivo = str(PATH_ROOMS + '/' + namemap + '.json')
        with open(archivo, 'w') as data:
            json.dump(map, data, indent=4, sort_keys=True)
        data.close()

        self._mapList_.append(namemap+".json")
       
        self.manager_sync.newRoom(namemap, self._id_)

    def remove(self, token, roomName, current=None):
        validclient = self.auth.getOwner(token)
        logging.debug(validclient)
        roomName = roomName + '.json'
        
        if not validclient:
            raise IceGauntlet.Unauthorized()
        
        if roomName not in self._mapList_:
            raise IceGauntlet.RoomNotExists()

        
        if path.exists(PATH_ROOMS + '/' + roomName):
            remove(PATH_ROOMS + '/' + roomName)
        self._mapList_.remove(roomName)
       
        self.manager_sync.removedRoom(roomName, self._id_)

    def getRoom(self, roomName, current=None):
        if roomName.find(".json") == -1:
            roomName = roomName + ".json"
        vectorMapas = self._mapList_
        if roomName in vectorMapas:
            archivo = str(self._maps_path_ + '/' + roomName)
            with open(archivo, 'r') as data:
                roomData = data.read()
            return roomData

    def availableRooms(self, current = None):
        availableMaps = self._mapList_
        return availableMaps

    def publishSync(self, token, roomData, RoomManagerId, Current=None):
        print('PUBLISHING!')
        validclient = self.auth.getOwner(token)
        logging.debug(validclient)
        if not validclient:
            raise IceGauntlet.Unauthorized()
        map = {}
        try:
            map = json.loads(roomData)
            namemap = map["room"]
            map["user"] = validclient
        except:
            raise ValueError("Invalid name")
        if namemap in self._mapList_:
            raise IceGauntlet.RoomAlreadyExists()
        
        print('New Room published: ', namemap, 
                '\nPublished by: ', RoomManagerId)

        archivo = str(PATH_ROOMS + '/' + namemap + '.json')
        with open(archivo, 'w') as data:
            json.dump(map, data, indent=4, sort_keys=True)
        data.close()

    def removeSync(self, roomName, RoomManagerId, current=None):
        print('PUBLISHING REMOVE')
        deleteRoom = roomName
        if path.exists(PATH_ROOMS + '/' + deleteRoom):
            remove(PATH_ROOMS + '/' + deleteRoom)
        print('Room removed: ', roomName, 
                '\nRemoved by: ', RoomManagerId)

class DungeonI(IceGauntlet.Dungeon):
    def __init__(self, argv):
        self.servant = argv
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
        global PATH_ROOMS

        if self.serverFinder() == True:
            PATH_ROOMS = tempfile.mkdtemp()
            

        servant = RoomManagerI(args)
        servantdungeon = DungeonI(servant)
        servantEvents = RoomManagerSyncI(servant) #Pasamos id del RoomManager para distinguirlo
        
        adapter = self.communicator().createObjectAdapter('RoomManagerAdapter')
        
        proxy = adapter.addWithUUID(servant)
        proxydungeon = adapter.addWithUUID(servantdungeon)
        proxyEvents = adapter.addWithUUID(servantEvents)

        adapter.addDefaultServant(servant, '')
        adapter.activate()
        print('"{}"'.format(proxy), flush=True)
        file = open("icegauntlet-master/dungeonFile.txt", "w")
        file.write('{}'.format(proxydungeon))
        room_manager = IceGauntlet.RoomManagerPrx.uncheckedCast(proxy) #Instanciamos el manager
        
        servantEvents.room_manager = room_manager
        servantEvents._topic_channel_.subscribeAndGetPublisher(qos, proxyEvents)
        servantEvents._publisher_.hello(room_manager, servant._id_)
        servant.manager_sync = servantEvents
        
        print("Esperando eventos...")

        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        if PATH_ROOMS != "./icegauntlet-master/assets":
            shutil.rmtree(PATH_ROOMS)

        return 0
    
    def serverFinder(self):
        cont = 0

        for proc in psutil.process_iter():
            if proc.name().startswith('python3'):
                for arg in proc.cmdline():
                    if arg.startswith('./'):
                        arg = arg[2:]
                    if arg == 'Servidor.py':
                        cont = cont + 1
        print(cont)
        if cont == 1:
            return False
        else:
            return True

class RoomManagerSyncI(Ice.Application, IceGauntlet.RoomManagerSync):
    def __init__(self, servant):
        self.room_manager = servant
        self._id_ = servant._id_
        self.room_manager = None
        self._topic_name_ = "RoomManagerSyncChannel"
        self._topic_manager_ = self.get_topic_manager()
        self._topic_channel_ = self.get_topic()
        self._publisher_ = self.get_publisher()
        self._pool_servers_ = {}
        self._room_storage_ = servant._mapList_ 

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
            self._publisher_.announce(self.room_manager, self._id_)
             
    def announce(self, RoomManager, RoomManagerId, current=None):
        if RoomManagerId not in self._pool_servers_:
            self._pool_servers_[RoomManagerId] = RoomManager
            print("Hi my pana, my id is: ", RoomManagerId)
            availableMaps = RoomManager.availableRooms()

            for map in availableMaps:
                if map not in self._room_storage_:
                    new = self._pool_servers_[RoomManagerId].getRoom(map)
                    path = str(PATH_ROOMS + '/' + map)
                    with open(path, 'x') as f:
                        f.write(new)
                    f.close()

    def newRoom(self, roomName, RoomManagerId, current=None):
        print("New Room Event from: ",RoomManagerId)
        room = self._pool_servers_[RoomManagerId].getRoom(roomName + ".json")
        for i in self._pool_servers_:
            print("Propagating to: ", i)
            room_json = json.loads(room)
            token = room_json["token"]
            self._pool_servers_[i].publishSync(token, room, RoomManagerId)

    def removedRoom(self, roomName, RoomManagerId, current=None):
        print("Removed Room: ", roomName)
        room = self._pool_servers_[RoomManagerId].getRoom(roomName)
        for i in self._pool_servers_:
            print("Propagating to: ", i)
            self._pool_servers_[i].removeSync(roomName, i)
        

if __name__ == '__main__':
    APP = Server()
    sys.exit(APP.main(sys.argv))
