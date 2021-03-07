### Philipp Schaedle
###
### rename tifs and assign global identifier

### naming convention
# global identifier --> gidABCDEFG_lat...
# A: nonMine/mine : 0/1
# B: band: normal (0), infrared (1)
# C: edge length in km (1, 2, 3 ...)
# D: region identifier: operating_mines (a), NT (b), QLD (c), WA (d), S_WA (z)
# EFG: 3 digit file id
###
# provide A, B, C, D in command line
###

import os, sys
import sqlite3

### basic information
# execute this script in a folder containing raw images
dataDir = os.getcwd()
baseDir = os.path.dirname(os.path.realpath(__file__))

globalID_basefile = os.path.join(baseDir, 'assigned_GID.db')
# initialize database file
GID_database = sqlite3.connect(globalID_basefile)
# create database cursor
cur = GID_database.cursor()
try:
    # Create table if not yet existing
    cur.execute('''CREATE TABLE globalID
                    (ID text, file text, lat real, lon real)''')
except:
    pass

# read command line input with GID options
A, B, C, D = sys.argv[1:]

def getBaseGID(A, B, C, D, EFG):
    return ''.join([str(i) for i in [A, B, C, D, str(EFG).zfill(3)]])

# loop though files and rename
filenames = [i for i in os.listdir(dataDir) if i.startswith('ima')]
EFG = 0
for filename in filenames:
    baseGID = getBaseGID(A, B, C, D, EFG)
    # check if GID already exists
    while len(cur.execute("SELECT ID FROM globalID WHERE ID=?", (baseGID,)).fetchall())>0:
        EFG += 1
        baseGID = getBaseGID(A, B, C, D, EFG)
    coords = filename.split('_')[-4:]
    # hack to get the coordinates
    lat = float(coords[1])
    lon = float('.'.join(coords[3].split('.')[:-1]))
    newname = '_'.join([baseGID] + coords)
    newentry = (baseGID, newname, lat, lon)
    cur.execute("INSERT INTO globalID VALUES (?,?,?,?)", newentry)
    print('rename: ', filename, 'by: ', newname)
    os.rename(filename, newname)

    # hack to rewrite ir images with corresponding to respective image
    baseGID = getBaseGID(A, 1, C, D, EFG)
    newname = '_'.join([baseGID] + coords)
    newentry = (baseGID, newname, lat, lon)
    cur.execute("INSERT INTO globalID VALUES (?,?,?,?)", newentry)
    print('rename: ', 'ir'+filename, 'by: ', newname)
    os.rename('ir'+filename, newname)
    EFG += 1
    if EFG > 999.:
        print("###### WARNING number of images exceeded ######")



for row in cur.execute('SELECT * FROM globalID'):
    print(row)

# commit changes to database
GID_database.commit()
# close database
GID_database.close()
