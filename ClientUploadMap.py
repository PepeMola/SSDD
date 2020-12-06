#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import IceGauntlet

class Client(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        address = broker.stringToProxy(argv[1])
        auth = IceGauntlet.RoomManagerPrx.checkedCast(address)
        if not auth:
            raise RuntimeError("Invalid proxy")
        archivo = open(argv[3], 'r')
        leer = archivo.read()
        print(leer)
        auth.publish(argv[2], leer)
        return 0

sys.exit(Client().main(sys.argv))
