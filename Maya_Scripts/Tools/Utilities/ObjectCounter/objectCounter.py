#===============================================================================
# By Tomas Adame Salguero
# tomas.adame@brownbagfilms.com
# Last Updated: 2016/03/10
#
# Maya - Object counter utility
# V0.3
#===============================================================================
## Importing
import pymel.core as pm
import maya.cmds  as mc

############################
# OBJECT TYPES VARIABLES
############################
oSel               = []#
selMode            = []#
counter            = []#
objectTypeListName = []#


#Run Mode
def runonSelection(selMode, searchForFilter, searchFilterCB):
    if selMode == "All":
        oSel = pm.ls(type="transform")
        oSelFiltered = searchFilter(oSel,searchForFilter,searchFilterCB)
        if not oSel:
            oSelFiltered = False
        elif len(oSelFiltered) == 0:
            oSelFiltered = "Nothing found using '%s' Keyword" % searchForFilter
        else:
            #print "%i elements found using '%s' Keyword" % (len(oSelFiltered), searchForFilter)
            pass
    else:
        oSel = pm.ls(sl = True)
        oSelFiltered = searchFilter(oSel,searchForFilter,searchFilterCB)
        if not oSel:
            oSelFiltered = False
        elif len(oSelFiltered) == 0:
            oSelFiltered = "Nothing found using '%s' Keyword" % searchForFilter
        else:
            #print "%i elements found using '%s' Keyword" % (len(oSelFiltered), searchForFilter)
            pass
    return oSelFiltered

#look for keyword
def searchFilter(oSel,searchForFilter,searchFilterCB):
    oSelFiltered = []
    if searchFilterCB == "True":
        for obj in oSel:
            if searchForFilter.lower() in str(obj).lower():
                oSelFiltered.append(obj)
            else:
                pass
    else:
        oSelFiltered = oSel
    return oSelFiltered

# GET OBJECT TYPES
def getObjectTypes(obj):
    try:
        oType = obj.getShape().type()
    except:
        oType = obj.type()
    return oType

############################
# Create OBJECT Lists
############################
def createObjetsList(oType):
    objectTypeListName = str(oType) + "_List"
    return objectTypeListName

############################
# GET OBJECT amount
############################
def getObjetsCount(oSel):
    oType              = []#
    objectTypesList    = []#
    objectCollection   = []#
    for o in oSel:
        try:
            oType              = getObjectTypes(o)
            objectTypesList    = createObjetsList(oType)
            objectCollection.append(objectTypesList)
        except:
            pass
    return objectCollection

############################
# PRINT types
############################
def printResults(selMode, searchForFilter, searchFilterCB):
    cMessageA   = []
    cMessageB   = []
    oSel        = []
    oSel        = runonSelection(selMode, searchForFilter, searchFilterCB)
    #print oSel
    if oSel == False:
        oMessage = 'Selection is Empty. Did you select any object?'
        pm.confirmDialog( title='Error message', message=oMessage, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
        sNumber = len(oMessage)
        separator = "#"*sNumber
        print separator
        print oMessage
    if isinstance(oSel, str):
        pm.confirmDialog( title='Tool Message', message=oSel, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
        sNumber = len(oSel)
        separator = "#"*sNumber
        print separator
        print oSel
    else:
        objectCollection = getObjetsCount(oSel)
        if selMode == "All":
            cInfo = "There are %s Total objects in the scene.\n\n" % (len(objectCollection))
        else:
            cInfo = "There are %s Total Selected objects in the scene.\n\n" % (len(objectCollection))
        sNumber = len(cInfo)
        separator = "#"*sNumber
        print separator
        cMessageA.append(cInfo)
        for item in set(objectCollection):
            if selMode == "All":
                cInfo = "There are %s %s objects in the scene.\n" % (objectCollection.count(item), item.split("_List")[0])
            else:
                cInfo = "There are %s %s selected objects in the scene.\n" % (objectCollection.count(item), item.split("_List")[0])
            cMessageB.append(cInfo)
        cMessageB = sorted(cMessageB, key = lambda x: x.split()[3], reverse = False)
        #print cMessageB
        cMessage = cMessageA+cMessageB
        cMessage = ("").join(cMessage)
        print cMessage
        pm.confirmDialog( title='Tool message', message=cMessage, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
