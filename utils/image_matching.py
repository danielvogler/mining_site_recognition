### Daniel Vogler
###
### create csv files of image mapping between two folders

import os
import csv

### ask for folders to compare
f_a = input("First folder: ")
f_b = input("Second folder: ")
f_a_basename = os.path.basename( os.path.normpath( f_a) )
f_b_basename = os.path.basename( os.path.normpath( f_b) )

### find all items in folders
images_a = os.listdir( f_a )
images_b = os.listdir( f_b )

### make sure only pictures are checked
images_a = [x for x in images_a if x.endswith(".png") or x.endswith(".jpg") or x.endswith(".JPG")]
images_b = [x for x in images_b if x.endswith(".png") or x.endswith(".jpg") or x.endswith(".JPG")]

### check matching images
images_ab = [x for x in images_a if x in images_b]
images_only_a = [x for x in images_a if x not in images_b]
images_only_b = [x for x in images_b if x not in images_a]

### write file lists - only a
with open( str('match_only_' + f_a_basename + '.csv'), 'w') as export_a:
    for i in images_only_a:
        export_a.write('{}\n'.format(i))

### write file lists - only b
with open( str('match_only_' + f_b_basename + '.csv'), 'w') as export_b:
    for i in images_only_b:
        export_b.write('{}\n'.format(i))

### write file lists - ab
with open( str('match_both_' + f_a_basename + '_' + f_b_basename + '.csv'), 'w') as export_ab:
    for i in images_ab:
        export_ab.write('{}\n'.format(i))

print("DONE")
