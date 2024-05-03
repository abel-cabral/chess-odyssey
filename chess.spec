block_cipher = None
app_icon = 'assets/chess.icns'

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/stockfish', 'assets'),
        ('assets/chess.ico', 'assets'),
        ('assets/chess.icns', 'assets'),
        ('assets/pieces/*.png', 'assets/pieces'),
        ('assets/music/*.ogg', 'assets/music')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'pandas', 'setuptools', 'pip', 'pyinstaller-hooks-contrib', 'pyinstaller', 'macholib', 'altgraph'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Chess Odyssey',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    icon=app_icon,
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
    name='Chess Odyssey.app',
    icon=app_icon,
    bundle_identifier='com.abel.chess_odyssey',
)