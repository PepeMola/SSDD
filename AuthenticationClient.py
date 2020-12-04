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

        return 0
    
    def isValid(self, token):
        return self.proxy.isValid(token)

    


sys.exit(Client().main(sys.argv))
