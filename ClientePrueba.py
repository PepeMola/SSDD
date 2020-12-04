#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413

import IceGauntlet
 
class ClientePrueba(Ice.Application):
    def run(self, argv): 
        base = self.communicator().stringToProxy(argv[1])
        autenticacion = IceGauntlet.DungeonPrx.checkedCast(base)
    
        if not autenticacion:
            raise RuntimeError("Invalid proxy")

        autenticacion.getRoom()
        

        return 0

sys.exit(ClientePrueba().main(sys.argv))
