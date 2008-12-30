#PySh tutorial
#(C)2008 Robin Wellner (gvx)
#License: GPLv3
#Level: 3 (Advanced)

#TODO: put comments everywhere to explain functions
"""pysh 3.2.0
(C) 2008 Robin Wellner (gvx)
Licence: GPLv3

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""
#I advise you to read the Python Documentation on these modules:
from os import walk
from os.path import join, isdir
from ctypes import windll #Need Windows API
import _winreg
import gc
import re

#DataTuple is here a list, and not a tuple!
#But that is changed at the end of LoadData()
DataTuple = []

def LoadData():
#We're setting DataTuple here, so we must make clear to use
#the global name called DataTuple:
    global DataTuple
#Clear the data:
    DataTuple = []
#Force a garbage collect, to clear the old cache:
    gc.collect()
#You don't need a PyFox.txt, but if you do,
#it allows you to add a few links yourself.
    try:
        f = open('PyFox.txt')
        Data = f.read()
        f.close()
    except:
        Data = '#PyFox data file -- V0.0'
#If the first line isn't the PyFox data header ...
    if Data.split('\n')[0] != '#PyFox data file -- V0.0': #Wrong format! Possibly an old version.
#Don't complain, but don't process it either.
        pass
    else:
        DataTuple = [tuple(Line.split(' :: ', 1)) for Line in Data.split('\n')[1:]]
#To know what this does, I recommend you to read up on the documentation
#of both Windows Registry and the _winreg Python module.
    thekey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
#Make a local function AddDir:
    def AddDir(thedir, thedirname, anyfile=False):
        gotdir = _winreg.QueryValueEx(thekey, thedir)[0]
        for triple in walk(gotdir):
            for file in triple[2]:
                if file[-4:].lower() == '.lnk':
                    title = file[:-4]
                    DataTuple.append((title.replace('(', '\t'),join(triple[0], file)))
                elif anyfile:
                    title = file
                    DataTuple.append((title.replace('(', '\t'),join(triple[0], file)))
    AddDir('Programs', 'Menu Start')
    AddDir('Desktop', 'Desktop')
    AddDir('Personal', 'My Documents', anyfile=True)
    _winreg.CloseKey(thekey)
    thekey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    AddDir('Common Programs', 'Menu Start')
    AddDir('Common Desktop', 'Desktop')
    AddDir('Common Documents', 'Shared Documents', anyfile=True)
    _winreg.CloseKey(thekey)
    DataTuple = tuple(DataTuple)

LoadData()

print __doc__

help = """pysh: PyFox 3 PyShell Edition
(C)2008 Robin Wellner (gvx)

Some things to type:
reload      reload directory listings
exit        what do you THINK it does?
run         run the first hit from previous search
run 30      run the 30th hit
run 0       run the last hit
cd [DIR]    show current directory, or, if given, go to directory DIRNAME

You can also type some text. Then, PyFox will look for it. If it finds one
thing, it launches that, if it finds multiple things, it will list those.
For example:
fire        probably finds firefox, and maybe some other things, like
            "fire.jpg" and "you_are_fired.txt"
fire you    finds things like "fire.jpg", "you_are_fired.txt" and youtube.com
fire_you    finds "I'll fire you.txt", but not youtube.com or "fire.jpg"
firefox*    instead of starting firefox, just list it
fire?       verbose listing (just try it)
fire#40     show first 40 hits, normally shows first 10 hits.
!foo        search for "foo" in current directory, rules are the same as with
            normal search, only ? (verbose) is not supported"""

foundList = []
CUR_DIR = '.'

while True:
    try:
        inp = raw_input('?').lower()
    except:
        break
    INPL = inp.split('#')
    inp = INPL[0]
    try:
        N = int(INPL[1])
    except:
        N = 10
    del INPL
    if not inp:
        continue
    elif inp == 'help':
        print help
        continue
    elif inp == 'reload':
        LoadData()
        continue
    elif inp == 'exit':
        break
    elif inp.split()[0] == 'cd':
        if len(inp.split()) > 1:
            CUR_DIR = ' '.join(inp.split()[1:])
        else:
            print CUR_DIR
        continue
    elif inp.split()[0] == 'run':
        try:
            n = int(inp.split()[1])-1
        except:
            n = 0
        if n >= len(foundList):
            print "Didn't found that much!"
        else:
            print "Starting", foundList[n][0], '...'
            s = str(foundList[n][1]).split(' :: ') + ['','','']
            windll.shell32.ShellExecuteA(None, s[2] ,s[0], s[3], s[1], 1)
        continue
    elif inp[0] == '!':
        foundList = []
        valL = inp[1:].replace('*', '').split()
        i = 0
        for triple in walk(CUR_DIR):
            i += 1
            if i > N: break
            for file in triple[2]:
                if file[-4:].lower() == '.lnk':
                    title = file[:-4]
                else:
                    title = file
                lo = title.lower().replace(' ', '_')
                if any(val in lo for val in valL):
                    foundList.append((title.replace('(', '\t'),join(triple[0], file)))
        if len(foundList) == 1 and '*' not in inp:
            print "Starting", foundList[0][0], '...'
            s = str(foundList[0][1]).split(' :: ') + ['','','']
            windll.shell32.ShellExecuteA(None, s[2] ,s[0], s[3], s[1], 1)
        elif len(foundList) == 0:
            print "Could not find that."
        else:
            for item in foundList[:N]:
                try:
                    print item[0]
                except:
                    pass
        continue
    foundList = []
    valL = inp.replace('*', '').replace('?', '').split()
    for Item, Other in DataTuple:
        lo = Item.lower().replace(' ', '_')
        if any(val in lo for val in valL):
             foundList.append((Item.split('(')[0].replace('\t', '('), Other))
    if len(foundList) == 1 and '*' not in inp:
        print "Starting", foundList[0][0], '...'
        s = str(foundList[0][1]).split(' :: ') + ['','','']
        windll.shell32.ShellExecuteA(None, s[2] ,s[0], s[3], s[1], 1)
    elif len(foundList) == 0:
        print "Could not find that."
    elif '?' in inp:
        for item in foundList[:N]:
            try:
                print item[0]
                print ' ', item[1]
            except:
                pass
    else:
        for item in foundList[:N]:
            try:
                print item[0]
            except:
                pass
