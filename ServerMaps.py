#!/usr/bin python3
# -*- coding: utf-8 -*-

# pylint: disable=W1203
# pylint: disable=W0613

import sys
import Ice
Ice.loadSlice('IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413

import IceGauntlet
import json
import random
import signal
import string
import logging
import os.path

class ObtenerMapaI(IceGauntlet.ObtenerMapa):
    def __init__(self):
        self._users_ = {}
        self._active_tokens_ = set()
        #if os.path.exists(USERS_FILE):
        #    self.refresh()
        #else:
        #    self.__commit__()

    #def refresh(self, *args, **kwargs):
        '''Reload user DB to RAM'''
        logging.debug('Reloading user database')
        #with open(USERS_FILE, 'r') as contents:
        #    self._users_ = json.load(contents)
        #self._active_tokens_ = set([
        #    user.get(CURRENT_TOKEN, None) for user in self._users_.values()
        #])

    #def __commit__(self):
        #logging.debug('User database updated!')
        #with open(USERS_FILE, 'w') as contents:
        #    json.dump(self._users_, contents, indent=4, sort_keys=True)

    def getRoom(self, current=None):
        print("Metodo getRoom")


class GestorMapasI(IceGauntlet.GestorMapas):
    def __init__(self):
        self._users_ = {}
        self._active_tokens_ = set()
        #if os.path.exists(USERS_FILE):
        #    self.refresh()
        #else:
        #    self.__commit__()

    #def refresh(self, *args, **kwargs):
        '''Reload user DB to RAM'''
        logging.debug('Reloading user database')
        #with open(USERS_FILE, 'r') as contents:
        #    self._users_ = json.load(contents)
        #self._active_tokens_ = set([
        #    user.get(CURRENT_TOKEN, None) for user in self._users_.values()
        #])

    #def __commit__(self):
        #logging.debug('User database updated!')
        #with open(USERS_FILE, 'w') as contents:
        #    json.dump(self._users_, contents, indent=4, sort_keys=True)

    def publish(self, token, roomData, current = None):
    	print("Metodo publish")

    def remove(self, token, roomData, current = None):
    	print("Metodo remove")

class Server(Ice.Application):
    '''
    Authentication Server
    '''
    def run(self, args):
        '''
        Server loop
        '''
        logging.debug('Initializing server...')
        servant = ObtenerMapaI()
        servant1 = GestorMapasI()
        adapter = self.communicator().createObjectAdapter('ObtenerMapaAdapter')
        proxy = adapter.add(servant, self.communicator().stringToIdentity('default'))
        adapter.addDefaultServant(servant, '')
        adapter.activate()
        logging.debug('Adapter ready, servant proxy: {}'.format(proxy))
        print('"{}"'.format(proxy), flush=True)

        logging.debug('Entering server loop...')        
        logging.debug('Entering server loop...')
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
