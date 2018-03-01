from cx_Freeze import setup, Executable
import os
import sys
import distutils
import opcode

base = None

#TODO generic...
pythonPath = r'C:/Users/MyUser/Anaconda3/'

os.environ['TCL_LIBRARY'] = pythonPath + r'tcl/tcl8.6'
os.environ['TK_LIBRARY'] = pythonPath + r'tcl/tk8.6'
executables = [Executable("mainWindow.py", base=base)]

options = {
    'build_exe': {

        'packages':['pandas', 'scipy', 'numpy', 'idna', 'seaborn', 'os'],
		'excludes':['scipy.spatial.cKDTree'],
		'includes':['scipy'],
		'include_files':[pythonPath + 'DLLs/sqlite3.dll']
    },
}

setup(
    name = "BioTrackerAnalysis",
    options = options,
    version = "1.0",
    description = 'BioTrackerAnalysis',
    executables = executables
)

lst = os.listdir('build');
if (len(lst) == 1):
	os.rename('build/'+lst[0], '../BioTrackerAnalysis')
	os.rmdir('build')
	from distutils.dir_util import copy_tree
	copy_tree("settings", "../BioTrackerAnalysis/settings")
	copy_tree("data_processing", "../BioTrackerAnalysis/data_processing")
	copy_tree("stats", "../BioTrackerAnalysis/stats")