### Philipp Schaedle
###
### restructure the database and dissect the global identifiers into columns

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
    print(cur.execute('PRAGMA table_info(globalID)').fetchall())
    cur.execute('ALTER TABLE globalID ADD COLUMN mine integer')
    cur.execute('ALTER TABLE globalID ADD COLUMN band integer')
    cur.execute('ALTER TABLE globalID ADD COLUMN edge_l integer')
    cur.execute('ALTER TABLE globalID ADD COLUMN region text')
    cur.execute('ALTER TABLE globalID ADD COLUMN id_nb integer')
except:
    pass



allID = cur.execute('SELECT ID FROM globalID').fetchall()
for row in allID:
    row_mine = row[0][0]
    row_band = row[0][1]
    row_edge_l = row[0][2]
    row_region = row[0][3]
    row_id_nb = row[0][4:7]
    cur.execute('''UPDATE globalID
                SET mine=?, band=?, edge_l=?, region=?, id_nb=?
                WHERE ID=?''', (row_mine, row_band, row_edge_l, row_region, row_id_nb, row[0]))

for i in cur.execute('SELECT * FROM globalID').fetchall():
    print(i)

# commit changes to database
GID_database.commit()
# close database
GID_database.close()
