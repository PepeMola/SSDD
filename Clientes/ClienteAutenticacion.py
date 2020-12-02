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
import hashlib
import getpass

class ClienteAutenticacion(Ice.Application):
    
    def run(self, argv):
       
        broker = self.communicator()
        address = broker.stringToProxy(argv[1])
        server = IceGauntlet.AuthenticationPrx.checkedCast(address) #Interface Authentication --> IceGauntlet.ice

        if not server:
            raise RuntimeError("Invalid proxy")

        user = input("Write your User name:")
        print("Introduce your actual password.\n")
        actualPass = getpass.getpass()

        '''
        Hacer aqui un menu con las 2 opciones
        '''
        self.getToken(server, user, actualPass)
        self.changePass(server, user, actualPass)
        
        return 0
    
    def changePass(self, server, user, actualPass):
        print("Please, type your new password:\n")
        newPass = getpass.getpass()

        server.changePassword(user, actualPass, newPass)
        print("Password succesfully changed.\n")

    def getToken(self, server, user, actualPass):
        token = server.getNewToken(user, actualPass)
        print(token)

if __name__ == "__main__":
    clienteAutenticacion = ClienteAutenticacion(argv)
    sys.exit(ClienteAutenticacion().main(sys.argv))   