#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W1203
# pylint: disable=W0613

import sys
from sys import argv
import Ice
Ice.loadSlice('../IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413

import IceGauntlet
import hashlib
import getpass

class ClienteAutenticacion(Ice.Application):
    
    def run(self, argv):
       
        broker = self.communicator()
        address = broker.stringToProxy(argv[1])
        server = IceGauntlet.AuthenticationPrx.checkedCast(address) #Interface Authentication --> IceGauntlet.ice

        if not server:
            raise RuntimeError("Invalid proxy")

        user = input("Write your User name:")
        print("Introduce your actual password.\n")
        actualPass = getpass.getpass()

        while True:

            self.menu()

            try:

                opcion = int(input("Seleccione una de las opciones usando el teclado numérico...\n"))

                if opcion in range(2):
                    if opcion == 1:
                        self.changePass(server, user, actualPass)
                        break
                    if opcion == 2:
                        self.getToken(server, user, actualPass)
                        break
                else:

                    print("Error en la opcion elegida.\nSolo se aceptan los numeros 1 y 2.\n")

            except ValueError:

                print("Error, por favor ingrese solo números.\n") 

        return 0
    
    def changePass(self, server, user, actualPass):
        print("Please, type your new password:\n")
        newPass = getpass.getpass()

        server.changePassword(user, actualPass, newPass)
        print("Password succesfully changed.\n")

    def getToken(self, server, user, actualPass):
        token = server.getNewToken(user, actualPass)
        print(token)

    def menu(self):
        print("-------- ¿Qué desea hacer? --------\n")
        print("\t 1.- Cambiar contraseña.\n")
        print("\t 2.- Obtener un nuevo token.\n")


if __name__ == "__main__":
    clienteAutenticacion = ClienteAutenticacion(argv)
    sys.exit(ClienteAutenticacion().main(sys.argv))   