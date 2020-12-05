
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
        auth = IceGauntlet.DungeonPrx.checkedCast(base)
    
        if not auth:
            raise RuntimeError("Invalid proxy")

        auth.getRoom()
        

        return 0

sys.exit(ClientePrueba().main(sys.argv))