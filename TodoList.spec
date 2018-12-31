# -*- mode: python -*-

block_cipher = None


a = Analysis(['bin/TodoList.py'],
             pathex=['/Users/coskunyerli/PycharmProjects/TextEditor'],
             binaries=[],
             datas=[('/Users/coskunyerli/PycharmProjects/TextEditor/icons/*', 'icons'),
             ('/Users/coskunyerli/PycharmProjects/TextEditor/editor.conf', '.'),
             ('/Users/coskunyerli/PycharmProjects/TextEditor/style.qss', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='TodoList',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='TodoList')
app = BUNDLE(coll,
             name='TodoList.app',
             icon=None,
             bundle_identifier=None)
