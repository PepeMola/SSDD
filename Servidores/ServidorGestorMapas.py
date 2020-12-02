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
import json
import random
import signal
import string
import logging
import os.path


class RoomHandlerI(IceGauntlet.RoomManager):
    n = 0

class Server(Ice.Application):
    '''
    Tiene que pedir un mapa y correr el juego con este mapa
    '''
    def run(self, args):
        broker = self.communicator()
        servant = RoomHandlerI(args)

        adapter = self.communicator().createObjectAdapter('RoomManagerAdapter')
        proxy = adapter.add(servant, self.communicator().stringToIdentity('default'))
    
