#!/usr/bin python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Handler.ice')

import IceGauntlet
import hashlib
import getpass
 
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

