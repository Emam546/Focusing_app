# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('public', 'public')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
    
)
pyz = PYZ(a.pure)


exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='focusing',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,  # Windows-safe
    upx=True,
    console=False,  # hide console for GUI app
    disable_windowed_traceback=True,
    icon='build/icon.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name='focusing',
)
