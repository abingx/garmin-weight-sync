# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('src', 'src')]
binaries = []
hiddenimports = ['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'garmin', 'xiaomi', 'core', 'core.models', 'core.config_manager', 'core.sync_service', 'jaraco', 'jaraco.collections', 'jaraco.context', 'jaraco.functools', 'jaraco.classes', 'jaraco.text', 'jaraco.compat', 'importlib_metadata', 'pkg_resources', 'pkg_resources.extern', 'packaging', 'packaging.version', 'packaging.requirements', 'packaging.specifiers', 'packaging.markers', 'appdirs', 'more_itertools', 'zipp', 'typing_extensions']
tmp_ret = collect_all('fit_tool')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('garth')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('logfire')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['src/gui/main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['pyi_rth_pyqt6.py'],
    excludes=['tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy', 'PIL', 'logfire.integrations.pydantic'],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GarminWeightSync',
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
)
app = BUNDLE(
    exe,
    name='GarminWeightSync.app',
    icon=None,
    bundle_identifier=None,
)
