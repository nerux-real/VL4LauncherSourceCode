# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['launcher_gui.pyw'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\NERUX\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\pyfiglet\\fonts', 'pyfiglet/fonts')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='launcher_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['v4l_smp_logo.ico'],
)
