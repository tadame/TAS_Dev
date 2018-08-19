import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os
from xml.dom.minidom import parse


menu_label   = ''
menu_name    = 'TAS_Tools'

def get_root_path():
    dir_path = os.path.abspath(os.path.join(__file__,"../.."))
    root = os.path.join(dir_path,"Tools")
    return root

def load_info(filename):
    dom = parse(filename)
    tool_info = {}
    try:
        rootTree = dom.getElementsByTagName('ToolInfo')

        # Get the name
        for node in rootTree[0].getElementsByTagName("Name"):
            appname = node.firstChild.data

        # Get the departments
        for node in rootTree[0].getElementsByTagName("Department"):
            dept = node.firstChild.data

        # Get the ToolHelp
        for node in rootTree[0].getElementsByTagName("ToolHelp"):
            tool = node.firstChild.data

        # Get the description
        for node in rootTree[0].getElementsByTagName("Description"):
            desc = node.firstChild.data

        # Get the application path
        basepath = os.path.dirname(filename)
        for filename in os.listdir(basepath):
            if filename.endswith("command.py"):
                script_path = os.path.join(basepath,filename)

        #collection = appname, tool, desc
        #tool_info [dept] = collection
        tool_info = dept, appname, script_path
        
    except:
        pass

    return tool_info
    
def buildMenu(parent):
        """ Searches the root folder for tools and folders. These are added
        to the parent menu and sorted.

        Args:
            parent: parent menu item to add items to
            root: find tools starting in this folder
        """
        root = get_root_path()
        if not os.path.exists(root):
            return
        
        menu_tool = []
        menu_items = []
        
        # Generate the list of menu items.
        for root, dirs, files in os.walk(root):
            for file in files:
                if file.endswith("tool_info.xml"):
                    tool_file = os.path.join(root, file)
                    tool_info = load_info(tool_file)
                    menu_tool.append(tool_info)
                if file.endswith("sub_menu.xml"):
                    menu_item = os.path.basename(root)
                    menu_items.append(menu_item)
        
        # Create the sorted menu.
        tool_dict = dict()
        print menu_tool

        for tool in menu_tool:
            if tool[0] in tool_dict:
                # append the new number to the existing array at this slot
                tool_dict[tool[0]].append((tool[1], tool[2]))
            else:
                # create a new array in this slot
                tool_dict[tool[0]] = [(tool[1], tool[2])]
        
        # print tool_dict, "KK"
        ''' [(u'Animation', u'GPU Cache Switch', 'C:\\Users\\t_adame\\Documents\\Git\\TAS_Dev\\Maya_Scripts\\Tools\\Animation\\GPU_Cache\\command.py'),
             (u'Utilities', u'Object Counter ', 'C:\\Users\\t_adame\\Documents\\Git\\TAS_Dev\\Maya_Scripts\\Tools\\Utilities\\ObjectCounter\\command.py'),
             (u'Utilities', u'Smooth Toogle', 'C:\\Users\\t_adame\\Documents\\Git\\TAS_Dev\\Maya_Scripts\\Tools\\Utilities\\SmoothToogle\\command.py')]
        '''

        for menu_name, menu_data in tool_dict.iteritems() :
            if menu_name in menu_items:
                sub_menu = pm.menuItem(label=menu_name, subMenu=True, p=parent, tearOff=True, postMenuCommandOnce=True)
                #sub_menu = pm.subMenuItem(label=menu_name, subMenu=True, p=parent, tearOff=True, postMenuCommandOnce=True)
                for app, cmd in menu_data:
                    script_cmd='execfile(r"{}");'.format(cmd)
                    pm.menuItem(label=app, command=script_cmd, parent=sub_menu)


def createMenus():
    """ setup menu creation for tools in a folder and its subfolders

    Args:
        rootFolder: path to the start of a folder structure with tool infos in them
    """
    # Get gMainWindow from mel command
    main_window = mel.eval("$temp=$gMainWindow")

    # search and delete old menuName
    unload_menus()

    # Add userMenu to Maya Menu
    tools_menu = pm.menu(menu_name, parent=main_window)
    print ('Building Menu : ' + menu_name)
    
    # Add recursive menus
    buildMenu(tools_menu)
    
def unload_menus( ):
    # Get gMainWindow from mel command
    main_window = mel.eval("$temp=$gMainWindow")
    # search and delete old menuName
    menu_list = pm.window(main_window, query=True, menuArray=True)
    
    for menu in menu_list:
        if menu == menu_name:
            pm.menu(menu, edit=True, deleteAllItems=True)
            pm.deleteUI(menu)
            print ('Unloading Menu : ' + menu_name)
            break
