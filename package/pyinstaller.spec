# -*- mode: python -*-
import os
from glob import glob

# Find PyQt5 directory
from inspect import getfile
import PyQt5
pyqt_dir = os.path.dirname(getfile(PyQt5))


# Adding all css and images as part of additional resources
data_files_glob = glob(os.path.join('mu','resources', 'css', '*.css'))
data_files_glob += glob(os.path.join('mu', 'resources', 'images', '*.*'))
data_files_glob += glob(os.path.join('mu', 'resources', 'fonts', '*.*'))
# Paths are a bit tricky: glob works on cwd (project root), pyinstaller relative
# starts on spec file location, and packed application relative starts on
# project root directory.
data_files = [(os.path.join('..', x), os.path.dirname(x)) for x in data_files_glob]
print('Spec file resources selected: %s' % data_files)


a = Analysis(['../run.py'],
             pathex=['../', pyqt_dir],
             binaries=None,
             datas=data_files,
             hiddenimports = ['sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None)

# On windows there are issues with PyInstaller not including a CRT DLL
# https://github.com/pyinstaller/pyinstaller/issues/1566
if os.name == 'nt':
    dll_path = 'C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\Common7\\IDE\\Remote Debugger\\x86\\api-ms-win-crt-runtime-l1-1-0.dll'
    if os.path.isfile(dll_path):
        binaries = [x for x in a.binaries if x[0] != 'api-ms-win-crt-runtime-l1-1-0.dll']
        a.binaries = binaries + [('api-ms-win-crt-runtime-l1-1-0.dll', dll_path, 'BINARY')]
        print(a.binaries)

pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=None)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='mu',
          strip=False,
          upx=True,
          # False hides the cli window, useful ON to debug
          console=False,
          debug=False,
          icon='package/icons/win_icon.ico')

app = BUNDLE(exe,
         name='mu.app',
         icon='package/icons/mac_icon.icns',
         bundle_identifier=None,
         info_plist={
            'NSHighResolutionCapable': 'True'})

# For debugging you can uncomment COLLECT and it will package to a folder
# instead of a single executable (also comment out the "a" arguments in EXE)
#coll = COLLECT(exe,
#               a.binaries,
#               a.zipfiles,
#               a.datas,
#               strip=None,
#               upx=True,
#               name='run')
