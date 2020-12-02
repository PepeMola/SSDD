#!/usr/bin python3
# -*- coding: utf-8 -*-

# pylint: disable=W1203
# pylint: disable=W0613

import sys
import Ice
Ice.loadSlice('../IceGauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413

import IceGauntlet

class GestorMapas(IceGauntlet.RoomManager):
    '''
    Tiene que pedir un mapa y correr el juego con este mapa
    '''
    
    
