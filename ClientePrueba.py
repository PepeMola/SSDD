
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413

import IceGauntlet
 
class ClientePrueba(Ice.Application):
    def run(self,argv): 
        archivo= open("icegauntlet-master/dungeonFile.txt","r")
        proxy = archivo.read()
        archivo.close()
        print(proxy)
        base = self.communicator().stringToProxy(proxy)
        auth = IceGauntlet.DungeonPrx.checkedCast(base)
    
        if not auth:
            raise RuntimeError("Invalid proxy")

        mapData = auth.getRoom()
        print(mapData)

        return 0

sys.exit(ClientePrueba().main(sys.argv))