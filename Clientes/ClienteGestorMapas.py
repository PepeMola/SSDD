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

'''
Este cliente es el encargado de ejecutar el publish() y remove()
'''
class Client(Ice.Application):
    
    def run(self, argv): 
        broker = self.communicator().stringToProxy(argv[1])
        server = IceGauntlet.RoomManagerPrx.checkedCast(broker)
    
        if not server:
            raise RuntimeError("Invalid proxy")

        '''
        Otro menu para ver que quiere hacer el usuario
        '''

        self.publish(server, argv)
        self.remove(server, argv)

        return 0

    def publish(self, server, argv):
        archivo = open(argv[3], 'r') 
        leer = archivo.read() 
        print(leer)
        server.publish(argv[2], leer)

    def remove(self, server, argv):
        server.remove(argv[2], argv[3])    