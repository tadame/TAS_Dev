# -*- coding: utf-8 -*-
"""
.. module:: BBF
   :synopsis:

copyright 2015 Brown Bag Films
"""
from __future__ import print_function

import os
import re
import sys
import __builtin__

__base_dir    = os.path.abspath(os.path.dirname(__file__))
__env_pypaths = os.environ.get('PYTHONPATH', '').split(os.pathsep)
__env_paths   = os.environ.get('PATH', '').split(os.pathsep)

__env_store_name = "BBF_PIPELINE_BASE_PATH_LIST"


# For __store and __clean to function properly, we need to the module by path (using imp.load_source("name", <path.py>)
def __store(base_dir):
    """
    Stores the base BBF path to an environment variable called BBF_PIPELINE_BASE_PATH_LIST

    Args:
        base_dir: str
    """
    base_dir = os.path.normpath(base_dir)

    paths = os.environ.get(__env_store_name, "")
    path_list = paths.split(os.pathsep)
    if base_dir not in path_list:
        path_list.append(base_dir)
    os.environ[__env_store_name] = os.pathsep.join(path_list)


def __clean(base_dir):
    """
    Removes any previously stored sys.path and os.environ["PYTHONPATH"]
    
    Args:
        base_dir: str - e.g. S:/BBF_PIPELINE

    """
    paths = os.environ.get(__env_store_name, "")
    store_path_list = paths.split(os.pathsep)
    _clean_paths = set()
    base_dir = os.path.normpath(base_dir)

    for _path in store_path_list:
        _path = os.path.normpath(_path)
        if not _path or base_dir == _path:
            continue

        for sys_path in sys.path:
            _sys_path = os.path.normpath(sys_path)
            if _sys_path.startswith(_path):
                _clean_paths.add(sys_path)

        for py_path in __env_pypaths:
            _py_path = os.path.normpath(py_path)
            if _py_path.startswith(_path):
                _clean_paths.add(py_path)

        for env_path in __env_paths:
            _env_path = os.path.normpath(env_path)
            if _env_path.startswith(_path):
                _clean_paths.add(env_path)

    for _path in _clean_paths:
        if _path in sys.path:
            sys.path.remove(_path)
        if _path in __env_pypaths:
            __env_pypaths.remove(_path)
        if _path in __env_paths:
            __env_paths.remove(_path)

    if __env_pypaths:
        os.environ["PYTHONPATH"] = os.pathsep.join(__env_pypaths)

    if __env_paths:
        os.environ["PATH"] = os.pathsep.join(__env_paths)


__store(os.path.dirname(__base_dir))
__clean(os.path.dirname(__base_dir))


for path in ['Common/Lib',
             'Common/Tools',
             'Common/ThirdParty/Lib']:
    pypath = os.path.join(__base_dir, path)
    if pypath not in sys.path:
        sys.path.append(pypath)
    if pypath not in __env_paths:
        __env_pypaths.append(pypath)

for path in ['Common/Bin']:
    bin_path = os.path.join(__base_dir, path)
    __env_paths.append(bin_path)
    os.environ['PATH'] = os.pathsep.join(__env_paths)

# Setting this will override where Maya finds its PySide later on
# os.environ['PYTHONPATH'] = os.pathsep.join(__env_pypaths)

import BBF.Common.Lib.bbfContext as bbfContext

if not hasattr(__builtin__, 'bbf_context'):
    __builtin__.bbf_context = bbfContext.context.ContextStack()
    bbfContext.context.Context('<root>')

    # fill in some information about the code repository
    cwd = os.getcwdu()
    os.chdir(__base_dir)

    bbf_context['repo'] = {'revision': None,
                           'root': None}

    try:
        pipe = os.popen('git rev-parse HEAD') # subprocess.Popen fails in Maya
        bbf_context['repo.revision'] = pipe.read().strip()
        pipe.close()
        pipe = os.popen('git rev-parse --show-toplevel')
        bbf_context['repo.root'] = pipe.read().strip()
        pipe.close()
    except: # if git isn't available, or we're not running from a proper git cloned repo, that's currently not a problem
        pass

    os.chdir(cwd)

    # fill in information from the environment
    if 'PROJECTNAME' in os.environ:
        bbf_context['project.name'] = os.environ['PROJECTNAME']
    for key in os.environ.keys():
        m = re.match('BBF_(?P<key>.+)', key)
        if m is not None:
            ctx_key = 'bbf.{key}'.format(key=m.group('key').lower())
            bbf_context[ctx_key] = os.environ[key]
