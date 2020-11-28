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

class GestorMapasI(IceGauntlet.GestorMapas):
    def __init__(self, argv):
        self._users_ = {}
        self._active_tokens_ = set()
        self.autenticacion = Client()
        self.autenticacion.run(argv)
        #if os.path.exists(USERS_FILE):
        #    self.refresh()
        #else:
        #    self.__commit__()

    #def refresh(self, *args, **kwargs):
        #'''Reload user DB to RAM'''
        #logging.debug('Reloading user database')
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
        validClient = self.autenticacion.isValid(token)
        print(validClient)

    def remove(self, token, roomData, current = None):
    	print("Metodo remove")

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

class Server(Ice.Application):
    '''
    Authentication Server
    '''
    def run(self, args):
        '''
        Server loop
        '''
        logging.debug('Initializing server...')
        #servant1 = ObtenerMapaI()
        servant = GestorMapasI(args)
        adapter = self.communicator().createObjectAdapter('GestorMapasAdapter')
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
