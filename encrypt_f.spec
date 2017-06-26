# -*- mode: python -*-

block_cipher = None


a = Analysis(['encrypt_f.py'],
             pathex=['/home/mayanksingh2298/Desktop/projects/steganography/final_mix'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='encrypt_f',
          debug=False,
          strip=False,
          upx=True,
          console=True )
