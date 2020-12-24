#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=E0401
# pylint: disable=C0413
# pylint: disable=C0103
# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=W0221

import sys
import Ice
Ice.loadSlice('IceGauntlet.ice')

import IceGauntlet

class Client(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        address = broker.stringToProxy(argv[1])
        auth = IceGauntlet.RoomManagerPrx.checkedCast(address)
        if not auth:
            raise RuntimeError("Invalid proxy")

        auth.remove(argv[2], argv[3])

        return 0

sys.exit(Client().main(sys.argv))
