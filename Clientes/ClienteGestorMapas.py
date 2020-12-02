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

'''
Este cliente es el encargado de ejecutar el publish() y remove()
'''
class ClienteGestorMapas(Ice.Application):
    
    def run(self, argv): 
        broker = self.communicator().stringToProxy(argv[1])
        server = IceGauntlet.RoomManagerPrx.checkedCast(broker)

        if not server:
            raise RuntimeError("Invalid proxy")
      
        while True:

            self.menu()

            try:
                opcion = int(input("Seleccione una de las opciones usando el teclado numérico...\n"))

                if opcion in range(2):

                    if opcion == 1:
                        self.publish(server, argv)
                        break
                    if opcion == 2:
                        self.remove(server, argv)
                        break

                else:
                    print("Error en la opcion elegida.\nSolo se aceptan los numeros 1 y 2.\n")

            except ValueError:
                print("Error, por favor ingrese solo números.\n")   

        return 0

    def publish(self, server, argv):
        archivo = open(argv[3], 'r') 
        leer = archivo.read() 
        print(leer)
        server.publish(argv[2], leer)

    def remove(self, server, argv):
        server.remove(argv[2], argv[3]) 

    def menu(self):
        print("-------- ¿Qué desea hacer? --------\n")
        print("\t 1.- Publicar un nuevo mapa.\n")
        print("\t 2.- Eliminar un mapa existente.\n")

if __name__ == "__main__":
    clienteMapas = ClienteGestorMapas(argv)
    sys.exit(ClienteGestorMapas().main(sys.argv))   