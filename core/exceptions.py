#!/usr/bin/env python
# -*- coding: utf-8 -*-


class NotAddingNonPlayerBotException(Exception):
    """ It is raised when a bot adds another bot which is not of the type GenericBotNonPlayer """
    def __init__(self):
        super().__init__('Only a GenericBotNonPlayer type can be added')
