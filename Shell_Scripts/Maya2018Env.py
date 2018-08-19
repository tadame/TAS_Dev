import os
import subprocess

# Local file
dir_path = os.path.abspath(os.path.join(__file__,"../.."))

# Append TAS Repo
my_env = os.environ.copy()
common = os.path.join(dir_path,"Common")
scripts = ';' + os.path.join(dir_path,"Maya_Scripts")
lib = ';' + os.path.join(dir_path,"Maya_Scripts\Lib")
startup = ';' + os.path.join(dir_path,"Maya_Scripts\StartUp")
tools = ';' + os.path.join(dir_path,"Maya_Scripts\Tools")
shell_tools = ';' + os.path.join(dir_path,"Shell_Scripts")

my_env["PYTHONPATH"] = common
my_env["PYTHONPATH"] += scripts
my_env["PYTHONPATH"] += lib
my_env["PYTHONPATH"] += startup
my_env["PYTHONPATH"] += tools
my_env["PYTHONPATH"] += shell_tools

# exec Files
__M2018=r"C:\Program Files\Autodesk\Maya2018\bin\maya.exe"
__M2019=r"C:\Program Files\Autodesk_Beta\Maya2019\bin\maya.exe"

#Maya = subprocess.call(__M2018)
Maya = subprocess.Popen(__M2018, env=my_env)
print "Starting Maya 2018.3 TAS Dev Environment"

