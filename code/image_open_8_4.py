from PIL import Image
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math
import sys

image1 = input('Enter image name with extension: ')
#im = Image.open('shot7.tif')
im = Image.open(image1)
#im = Image.open('GTEX-1117F-1726 (1).svs')
#im.show()

imarray = np.array(im)
imarray1 = np.array(im)
print('imarray.shape: ' + str(imarray.shape) + ', imarray.size: ' + str(imarray.size) + ', len(imarray): ' + str(len(imarray)))

"""# 4 colours
        if val_i >= 63 and val_i < 128:
            imarray[i1][i2][0] = int(85)
            imarray[i1][i2][1] = int(85)
            imarray[i1][i2][2] = int(85)
        elif val_i >= 128 and val_i < 191:
            imarray[i1][i2][0] = int(171)
            imarray[i1][i2][1] = int(171)
            imarray[i1][i2][2] = int(171)
        elif val_i < 63:
            imarray[i1][i2][0] = int(0)
            imarray[i1][i2][1] = int(0)
            imarray[i1][i2][2] = int(0)
        else:
            imarray[i1][i2][0] = int(255)
            imarray[i1][i2][1] = int(255)
            imarray[i1][i2][2] = int(255)"""

print('1) L1_4, L2_8')
print('2) L2_4')
user_choice = input('Enter your choice:')
if user_choice == '1':
    i1 = 0
    while (i1 < len(imarray1)):
        i2 = 0
        while (i2 < len(imarray1[i1])):
            val_i = int(imarray1[i1][i2][0]) 
            val_i = val_i + int(imarray1[i1][i2][1])
            val_i = val_i + int(imarray1[i1][i2][2])
            val_i = int(val_i / 3)
            # 4 colours L1
            if val_i < 63:
                imarray1[i1][i2][0] = int(0)
                imarray1[i1][i2][1] = int(0)
                imarray1[i1][i2][2] = int(0)
            i2 = i2 + 1
        i1 = i1 + 1
    
    i1 = 0
    while (i1 < len(imarray)):
        i2 = 0
        while (i2 < len(imarray[i1])):
            #print((imarray[i1][i2][0] + imarray[i1][i2][1] + imarray[i1][i2][2]) / 3)
            val_i = int(imarray[i1][i2][0]) 
            val_i = val_i + int(imarray[i1][i2][1])
            val_i = val_i + int(imarray[i1][i2][2])
            val_i = int(val_i / 3)
            # 8 colours
            val_ceil = math.ceil((val_i + 1) / 32)
            val_i = int((val_ceil * 32) - 16)
            if imarray1[i1][i2][0] == 0 and imarray1[i1][i2][1] == 0 and imarray1[i1][i2][2] == 0:
                pass
            elif val_i == 48:
                imarray1[i1][i2][0] = int(0)
                imarray1[i1][i2][1] = int(0)
                imarray1[i1][i2][2] = int(0)
            else:
                imarray1[i1][i2][0] = val_i
                imarray1[i1][i2][1] = val_i
                imarray1[i1][i2][2] = val_i
            i2 = i2 + 1
        i1 = i1 + 1
        
elif user_choice == '2':
    i1 = 0
    while (i1 < len(imarray1)):
        i2 = 0
        while (i2 < len(imarray1[i1])):
            val_i = int(imarray1[i1][i2][0]) 
            val_i = val_i + int(imarray1[i1][i2][1])
            val_i = val_i + int(imarray1[i1][i2][2])
            val_i = int(val_i / 3)
            # 4 colours L2
            if val_i >= 63 and val_i < 128:
                imarray[i1][i2][0] = int(85)
                imarray[i1][i2][1] = int(85)
                imarray[i1][i2][2] = int(85)
            i2 = i2 + 1
        i1 = i1 + 1
    
    i1 = 0
    while (i1 < len(imarray)):
        i2 = 0
        while (i2 < len(imarray[i1])):
            #print((imarray[i1][i2][0] + imarray[i1][i2][1] + imarray[i1][i2][2]) / 3)
            val_i = int(imarray[i1][i2][0]) 
            val_i = val_i + int(imarray[i1][i2][1])
            val_i = val_i + int(imarray[i1][i2][2])
            val_i = int(val_i / 3)
            # 8 colours
            val_ceil = math.ceil((val_i + 1) / 32)
            val_i = int((val_ceil * 32) - 16)
            if imarray1[i1][i2][0] == 85 and imarray1[i1][i2][1] == 85 and imarray1[i1][i2][2] == 85:
                pass
            else:
                imarray1[i1][i2][0] = val_i
                imarray1[i1][i2][1] = val_i
                imarray1[i1][i2][2] = val_i
            i2 = i2 + 1
        i1 = i1 + 1
else:
    sys.exit()
    
data = Image.fromarray(imarray1)
print('Done')
image1_name = ''
image1_exten = ''

i = len(image1) - 1
while (image1[i] != '.'):
    image1_exten = image1_exten + image1[i]
    i = i - 1
image1_exten = image1_exten[::-1]

i = len(image1) - len(image1_exten) - 1 # (-1 for '.')
i = i - 1 # since range = 0 -> length - 1
while (i >= 0):
    image1_name = image1_name + image1[i]
    i = i - 1
image1_name = image1_name[::-1]
if user_choice == '1':
    image1_name = image1_name + '_8_L2_4_L1.' + image1_exten
else:
    image1_name = image1_name + '_8_4_L2.' + image1_exten
#image1_name = image1_name + '_8_4_L2.' + image1_exten
data.save(image1_name)
#data.save('shot7_bi2.tif')