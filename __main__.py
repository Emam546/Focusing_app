from __init__ import *
def main():
    root=APP()
    root.title("Foucsing")
    root.iconbitmap(default="app_icon.ico")
    root.mainloop()
if __name__=="__main__":
    main()
# [--add-data <SRC;DEST or SRC:DEST>]
# [--add-binary <SRC;DEST or SRC:DEST>] [-p DIR]
# [--hidden-import MODULENAME]
# [--additional-hooks-dir HOOKSPATH]
# [--runtime-hook RUNTIME_HOOKS] [--exclude-module EXCLUDES]
# [--key KEY] [-d {all,imports,bootloader,noarchive}] [-s]
# [--noupx] [--upx-exclude FILE] [-c] [-w]
# [-i <FILE.ico or FILE.exe,ID or FILE.icns or "NONE">]
# [--version-file FILE] [-m <FILE or XML>] [-r RESOURCE]
# [--uac-admin] [--uac-uiaccess] [--win-private-assemblies]
# [--win-no-prefer-redirects]
# [--osx-bundle-identifier BUNDLE_IDENTIFIER]
# [--runtime-tmpdir PATH] [--bootloader-ignore-signals]
# [--distpath DIR] [--workpath WORKPATH] [-y]
# [--upx-dir UPX_DIR] [-a] [--clean] [--log-level LEVEL]