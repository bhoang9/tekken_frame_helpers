#rename files for each move with their place in the movelist
import os
import sys

src = os.getcwd()
targetDir = src + "/" + sys.argv[1] + "_gif_raw"
list = os.listdir(targetDir)

#convert 2nd argument into string array of indexes to insert
insertIndexes = sys.argv[2].split(",")
insertIndexes = [int(i) for i in insertIndexes] #convert string array into array of ints

#sort files by date modified
list.sort(key=lambda x: os.stat(os.path.join(targetDir, x)).st_mtime)
os.chdir(targetDir)
j = 0
for index,oldFile in enumerate(list):
    #move_num = str(index)
#    if(index + 1 >= insertIndexes[j]):
#        move_num = index + (j+2)
#    else:
#        move_num = index+1

#    if(j != (len(insertIndexes) - 1)):
#        if(index+1 == insertIndexes[j+1]):
#            j += 1
#    if(index+1 == insertIndexes[j] and j+1 < len(insertIndexes)):
#        j += 1


    while(j != len(insertIndexes) and index + (j+1) == insertIndexes[j]):
        j += 1

    move_num = index + 1 + j

    newFile = sys.argv[1] + "_move_{}.mp4".format(move_num)
    os.rename(oldFile, newFile)
