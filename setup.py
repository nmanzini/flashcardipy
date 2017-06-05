import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.

includefiles = ['test01.db']
includes = []
excludes = []
packages = []

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Console"

setup(  name = "FlashCardiPY",
        version = "0.1",
        description = "A flashcard application",
        options = {'build_exe': {'includes':includes,'excludes':excludes,'packages':packages,'include_files':includefiles}},
        executables = [Executable("main.py", base=base)])