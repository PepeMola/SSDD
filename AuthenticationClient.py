#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('IceGauntlet.ice')

import IceGauntlet
import hashlib
import getpass

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


sys.exit(Client().main(sys.argv))
    