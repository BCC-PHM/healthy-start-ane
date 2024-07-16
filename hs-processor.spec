# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['python/hs-processor.py'],
    pathex=['.'],
    binaries=[],
    datas=[('data/birmingham-imds.csv', 'data')],
    hiddenimports=['pandas', 'numpy', 'ctypes', 'sys', 'easygui', 'os'],
    hookspath=[],
    runtime_hooks=[],
    excludes = ['asttokens', 'cloudpickle', 'colorama', 'comm', 'debugpy', 'decorator', 'executing', 'ipykernel', 'python', 'jedi', 
               'jupyter_client', 'jupyter_core', 'libsodium', 'matplotlib-inline', 'nest-asyncio', 'parso', 'platformdirs', 
               'rompt-toolkit', 'prompt_toolkit', 'psutil', 'pure_eval', 'pygments', 'pyzmq', 'spyder-kernels', 'stack_data', 
               'tornado', 'traitlets', 'wcwidth', 'zeromq', 'matplotlib', 'scipy', 'sklearn', 'seaborn', 'bokeh', 'pillow', 'PyQt5', 
        	'PySide2', 'pytest', 'jupyter', 'IPython', 'pygments', 'notebook', 'qtpy', 'qtconsole', 'pyqtgraph', 'PyQt6', 'PySide6', 
                'PIL', 'pyarrow', 'fastparquet'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='hs-processor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='hs-processor',
)


