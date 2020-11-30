#!/usr/bin python3
# -*- coding: utf-8 -*-

# pylint: disable=W1203
# pylint: disable=W0613
import sys

import Ice

Ice.loadSlice('IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import getpass
import hashlib

import IceGauntlet

class ClientAuthentication (Ice.Application):

    def run(self, argv):
        broker = self.communicator()
        address = broker.stringToProxy(argv[1])
        server = IceGauntlet.AuthenticationPrx.checkedCast(address)




'''
with Ice.initialize(sys.argv) as communicator:
    base = communicator.stringToProxy(sys.argv[1])
    autenticacion = IceGauntlet.ObtenerMapaPrx.checkedCast(base)
    
    if not autenticacion:
        raise RuntimeError("Invalid proxy")
    
    
    autenticacion.getRoom()
    
    
    #print("Escriba su usuario: ")
    #user = input()
    #print(f"Escriba su contraseña: ")
    #passwordHash = getpass.getpass()
    #hashPass = hashlib.sha256(passwordHash.encode()).hexdigest()
    #print(hashPass)	
    #autenticacion.changePassword(user, "Hola123", hashPass)
    #token = autenticacion.getNewToken(user, hashPass) 
    #print(hashPass)
    #autenticacion.isValid(token)
    #print("Estás dentro.")

'''