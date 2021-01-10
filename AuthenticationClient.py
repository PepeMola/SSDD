#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=E0401
# pylint: disable=C0103
# pylint: disable=C0413
# pylint: disable=W0613
# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=W0221

import sys
from sys import argv
import hashlib
import getpass
import Ice
Ice.loadSlice('IceGauntlet.ice')

import IceGauntlet

#python3 ./AuthenticationClient.py -p pepe "default -t -e 1.1:tcp -h 10.0.2.15 -p 9091 -t 60000"
class ClienteAutenticacion(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        address = broker.stringToProxy(argv[3])
        auth = IceGauntlet.AuthenticationPrx.checkedCast(address)
        if not auth:
            raise RuntimeError("Invalid proxy")
        user = argv[2]
        actualpass = getpass.getpass('Password:')
        sha_actualpass = hashlib.sha256(actualpass.encode()).hexdigest()
        # Obtener Token
        if argv[1] == '-t':
            print(auth.getNewToken(user, sha_actualpass))
        # Setear contraseña default
        if argv[1] == '-p':
            newpass = getpass.getpass()
            sha_newpass = hashlib.sha256(newpass.encode()).hexdigest()
            auth.changePassword(user, sha_actualpass, sha_newpass)
            print("Your password has been changed successfully.\n")
        return 0
if __name__ == "__main__":
    CLIENTAUTH = ClienteAutenticacion(argv)
    sys.exit(ClienteAutenticacion().main(sys.argv))
