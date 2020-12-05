#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W1203
# pylint: disable=W0613

import sys
from sys import argv
import Ice
Ice.loadSlice('IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413

import IceGauntlet
import hashlib
import getpass

class ClienteAutenticacion(Ice.Application):
    
    def run(self, argv):
        broker = self.communicator()
        address = broker.stringToProxy(argv[3])
        auth = IceGauntlet.AuthenticationPrx.checkedCast(address) 

        if not auth:
            raise RuntimeError("Invalid proxy")
        
        user = argv[2]
        print(user)

        if argv[1] == '-t': # Obtener Token
            actualPass = getpass.getpass()
            sha_actualPass = hashlib.sha256(actualPass.encode()).hexdigest()
            print(auth.getNewToken(user, sha_actualPass))

        if argv[1] == '-p': # Setear contraseña default 
            newPass = getpass.getpass()
            sha_newPass = hashlib.sha256(newPass.encode()).hexdigest()
            auth.changePassword(user, None, sha_newPass)
        return 0
    
if __name__ == "__main__":
    clienteAutenticacion = ClienteAutenticacion(argv)
    sys.exit(ClienteAutenticacion().main(sys.argv)) 