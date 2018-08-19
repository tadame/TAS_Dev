import os
import sys
import datetime
import thread
import re
import __main__

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import pymel.core.nodetypes as nt
import pymel.core.datatypes as dt
import maya.OpenMaya as om
from pprint import pprint
import logging
log = logging.getLogger(__name__)



# Setup Menus using evalDeffered so that the UI exists
def addMenus():
    '''
	Loading Custom Tools menu
	'''
    import tasMenu
    tasMenu.createMenus()
	

pm.evalDeferred(addMenus)

print "Hello Tom"