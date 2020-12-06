#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from sys import argv
import hashlib
import getpass
import Ice
Ice.loadSlice('IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413
# pylint: disable=W0613

import IceGauntlet

class ClienteAutenticacion(Ice.Application):
    def run(self, argv):
        broker=self.communicator()
        address=broker.stringToProxy(argv[3])
        auth=IceGauntlet.AuthenticationPrx.checkedCast(address)
        if not auth:
            raise RuntimeError("Invalid proxy")
        user=argv[2]
        #print(user)
        actualPass=getpass.getpass('Password:')
        sha_actualPass=hashlib.sha256(actualPass.encode()).hexdigest()
        # Obtener Token
        if argv[1]=='-t':
            print(auth.getNewToken(user,sha_actualPass))
        # Setear contraseña default
        if argv[1]=='-p':
            newPass=getpass.getpass()
            sha_newPass=hashlib.sha256(newPass.encode()).hexdigest()
            auth.changePassword(user,sha_actualPass,sha_newPass)
            print("Your password has been changed successfully.\n")
        return 0
        
if __name__ == "__main__":
    clienteAutenticacion = ClienteAutenticacion(argv)
    sys.exit(ClienteAutenticacion().main(sys.argv))
