#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413

import IceGauntlet
import hashlib
import getpass

class Client(Ice.Application):
    def run(self, argv): 
        broker = self.communicator()
        address = broker.stringToProxy(argv[1])
        auth = IceGauntlet.AuthenticationPrx.checkedCast(address)
    
        if not auth:
            raise RuntimeError("Invalid proxy")
        
        self.proxy = auth
        print("Escriba su usuario: ")
        user = input()
        print(f"Escriba su contraseña: ")
        passwordHash = getpass.getpass()
        hashPass = hashlib.sha256(passwordHash.encode()).hexdigest()
        print(hashPass)	
        auth.changePassword(user, "Hola", hashPass)
        token = auth.getNewToken(user, hashPass) 
        print(hashPass)
        auth.isValid(token)
        return 0
    
    def isValid(self, token):
        return self.proxy.isValid(token)

    '''
    def changePass(self, server, user, actualPass):
        print("Please, type your new password:\n")
        newPass = getpass.getpass()

        server.changePassword(user, actualPass, newPass)
        print("Password succesfully changed.\n")

    def getToken(self, server, user, actualPass):
        token = server.getNewToken(user, actualPass)
        print(token)
    '''


sys.exit(Client().main(sys.argv))
