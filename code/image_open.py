from PIL import Image
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math

image1 = input('Enter image name with extension: ')
#im = Image.open('shot7.tif')
im = Image.open(image1)
#im = Image.open('GTEX-1117F-1726 (1).svs')
#im.show()

imarray = np.array(im)
print('imarray.shape: ' + str(imarray.shape) + ', imarray.size: ' + str(imarray.size) + ', len(imarray): ' + str(len(imarray)))

#threshold1 = input('Enter threshold value: ')
#threshold1 = int(threshold1)

#for i in range(1, 10):
#    print(len(imarray[i]), imarray[i][0], imarray[i][1], imarray[i][2])

"""i1 = 0
while (i1 < len(imarray)):
    i2 = 0
    while (i2 < len(imarray[i1])):
        imarray[i1][i2][0] = int(imarray[i1][i2][0] / 2)
        imarray[i1][i2][1] = int(imarray[i1][i2][1] / 2)
        imarray[i1][i2][2] = int(imarray[i1][i2][2] / 2)
        i2 = i2 + 1
    i1 = i1 + 1
"""

"""i1 = 0
while (i1 < len(imarray)):
    i2 = 0
    while (i2 < len(imarray[i1])):
        #print((imarray[i1][i2][0] + imarray[i1][i2][1] + imarray[i1][i2][2]) / 3)
        val_i = int(imarray[i1][i2][0]) 
        val_i = val_i + int(imarray[i1][i2][1])
        val_i = val_i + int(imarray[i1][i2][2])
        val_i = int(val_i / 3)
        if val_i > 128:
            imarray[i1][i2][0] = int(255)
            imarray[i1][i2][1] = int(255)
            imarray[i1][i2][2] = int(255)
        else:
            imarray[i1][i2][0] = int(0)
            imarray[i1][i2][1] = int(0)
            imarray[i1][i2][2] = int(0)
        i2 = i2 + 1
    i1 = i1 + 1"""

i1 = 0
while (i1 < len(imarray)):
    i2 = 0
    while (i2 < len(imarray[i1])):
        #print((imarray[i1][i2][0] + imarray[i1][i2][1] + imarray[i1][i2][2]) / 3)
        val_i = int(imarray[i1][i2][0]) 
        val_i = val_i + int(imarray[i1][i2][1])
        val_i = val_i + int(imarray[i1][i2][2])
        val_i = int(val_i / 3)
        # standard binary colours
        #if val_i < 228:
        #if val_i < 230:
        #if val_i < 234:
        #if val_i < 232:
        """if val_i < threshold1:
            imarray[i1][i2][0] = int(0)
            imarray[i1][i2][1] = int(0)
            imarray[i1][i2][2] = int(0)
        else:
            imarray[i1][i2][0] = int(255)
            imarray[i1][i2][1] = int(255)
            imarray[i1][i2][2] = int(255)"""
        """# 16 colours
        val_ceil = math.ceil((val_i + 1) / 16)
        val_i = int((val_ceil * 32) - 8)
        imarray[i1][i2][0] = val_i
        imarray[i1][i2][1] = val_i
        imarray[i1][i2][2] = val_i"""
        """# 16 colours binary class
        if val_i < 248:
            imarray[i1][i2][0] = int(0)
            imarray[i1][i2][1] = int(0)
            imarray[i1][i2][2] = int(0)
        else:
            imarray[i1][i2][0] = int(255)
            imarray[i1][i2][1] = int(255)
            imarray[i1][i2][2] = int(255)"""
        # 8 colours
        val_ceil = math.ceil((val_i + 1) / 32)
        val_i = int((val_ceil * 32) - 16)
        imarray[i1][i2][0] = val_i
        imarray[i1][i2][1] = val_i
        imarray[i1][i2][2] = val_i
        """# 8 colours binary class
        if val_i < 240:
            imarray[i1][i2][0] = int(0)
            imarray[i1][i2][1] = int(0)
            imarray[i1][i2][2] = int(0)
        else:
            imarray[i1][i2][0] = int(255)
            imarray[i1][i2][1] = int(255)
            imarray[i1][i2][2] = int(255)"""
        # 6 colours
        #val_ceil = math.ceil((val_i + 1) / 43)
        #val_i = int((val_ceil * 43) - 21)
        # 5 colours
        #val_ceil = math.ceil((val_i + 1) / 51)
        #val_i = int((val_ceil * 51) - 26)
        # 5 colours ternary class
        """#if val_i < 154:
        if val_i < 127:
        #if val_i < 95:    
            imarray[i1][i2][0] = int(0)
            imarray[i1][i2][1] = int(0)
            imarray[i1][i2][2] = int(0)
        elif val_i < 205:
            imarray[i1][i2][0] = int(191)
            imarray[i1][i2][1] = int(191)
            imarray[i1][i2][2] = int(191)
        else:
            imarray[i1][i2][0] = int(255)
            imarray[i1][i2][1] = int(255)
            imarray[i1][i2][2] = int(255)"""
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
        """# 4 colours binary class
        if val_i < 191:
            imarray[i1][i2][0] = int(0)
            imarray[i1][i2][1] = int(0)
            imarray[i1][i2][2] = int(0)
        else:
            imarray[i1][i2][0] = int(255)
            imarray[i1][i2][1] = int(255)
            imarray[i1][i2][2] = int(255)"""
        """# 3 colours
        if val_i > 85 and val_i < 171:
            imarray[i1][i2][0] = int(128)
            imarray[i1][i2][1] = int(128)
            imarray[i1][i2][2] = int(128)
        elif val_i < 85:
            imarray[i1][i2][0] = int(0)
            imarray[i1][i2][1] = int(0)
            imarray[i1][i2][2] = int(0)
        else:
            imarray[i1][i2][0] = int(255)
            imarray[i1][i2][1] = int(255)
            imarray[i1][i2][2] = int(255)"""
        i2 = i2 + 1
    i1 = i1 + 1

data = Image.fromarray(imarray)
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
image1_name = image1_name + '_8.' + image1_exten
data.save(image1_name)
#data.save('shot7_bi2.tif')