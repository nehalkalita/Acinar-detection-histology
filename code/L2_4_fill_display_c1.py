from PIL import Image
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math
import cv2 as cv
import csv
import skimage
#import skimage.viewer
import sys
import random

image_original = input('Enter image name with extension: ')
image_exten = ''
i = len(image_original) - 1
while (image_original[i] != '.'):
    image_exten = image_exten + image_original[i]
    i = i - 1
image_exten = image_exten[::-1]

image_o_name = ''
i = 0
while (i < (len(image_original) - (len(image_exten) + 1))):
    image_o_name = image_o_name + image_original[i]
    i = i + 1
    
image_8_name = image_o_name + '_8' + '.' + image_exten
    
path_in = (image_original)
#img=cv.imread(path_in)
img = Image.open(path_in)
imarray0 = np.array(img)


path_in = (image_8_name)
img=cv.imread(path_in)
imarray1 = np.array(img)
print(imarray1.shape, imarray1.size, len(imarray1)) # Y,X
y_axis = imarray1.shape[0] # 680 # size of each section
x_axis = imarray1.shape[1]

s_size = 100 # size of each section
y_total = math.ceil(y_axis / s_size)
x_total = math.ceil(x_axis / s_size)
yx_total = y_total * x_total
#print(x_total, y_total, yx_total)

min_acinar_area = input('Enter minimum area of acinar: ')
min_acinar_area = int(min_acinar_area)

max_gap_area = input('Enter maximum area of gap: ')
max_gap_area = int(max_gap_area)

combined_file = open('L2_4_combined.csv', 'r', newline='')
csv_reader1 = csv.reader(combined_file)
segmented_file = open('L2_4_segmented.csv', 'r', newline='')
csv_reader2 = csv.reader(segmented_file)

combined_file = open('L1_4_combined.csv', 'r', newline='')
csv_reader3 = csv.reader(combined_file)
segmented_file = open('L1_4_segmented.csv', 'r', newline='')
csv_reader4 = csv.reader(segmented_file)

acinar_c_indices = [] # index, total L1_4 gaps
acinar_s_indices = [] # index, total L1_4 gaps
combined_dataset = [[[]]]
segmented_dataset = []

combined_dataset_L1 = [[[]]]
segmented_dataset_L1 = []

# store data in combined and segmented datasets
i = 0
i1 = -1
for line in csv_reader1:
    if len(line) == 0:
        combined_dataset.append([])
        i = i + 1
        i1 = -1
    else:
        if len(line) == 3:
            combined_dataset[i][i1].append([int(line[0]), int(line[1]), int(line[2])])
        elif len(line) == 2:
            combined_dataset[i].append([])
            i1 = i1 + 1
            combined_dataset[i][i1].append([int(line[0]), int(line[1])])
i = 0 # remove null lists
while (i < len(combined_dataset)):
    if len(combined_dataset[i]) == 0:
        del combined_dataset[i]
    else:
        i1 = 0
        while (i1 < len(combined_dataset[i])):
            if combined_dataset[i][i1] == []:
                del combined_dataset[i][i1]
            else:
                i1 = i1 + 1
        i = i + 1

i = 0
i1 = -1
i2 = -1
i3 = 0
for line in csv_reader2:
    if len(line) == 0:
        i = i + 1
    elif len(line) == 1:
        if i1 != i:
            i1 = i
            segmented_dataset.append([i1])
            i2 = i2 + 1
            segmented_dataset[i2].append([])
            i3 = 1
        else:
            segmented_dataset[i2].append([])
            i3 = i3 + 1
    elif len(line) == 3:
        #print(i,i1,i2)
        segmented_dataset[i2][i3].append([int(line[0]), int(line[1]), int(line[2])])

i = 0
i1 = -1
for line in csv_reader3:
    if len(line) == 0:
        combined_dataset_L1.append([])
        i = i + 1
        i1 = -1
    else:
        if len(line) == 3:
            combined_dataset_L1[i][i1].append([int(line[0]), int(line[1]), int(line[2])])
        elif len(line) == 2:
            combined_dataset_L1[i].append([])
            i1 = i1 + 1
            combined_dataset_L1[i][i1].append([int(line[0]), int(line[1])])
i = 0 # remove null lists
while (i < len(combined_dataset_L1)):
    if len(combined_dataset_L1[i]) == 0:
        del combined_dataset_L1[i]
    else:
        i1 = 0
        while (i1 < len(combined_dataset_L1[i])):
            if combined_dataset_L1[i][i1] == []:
                del combined_dataset_L1[i][i1]
            else:
                i1 = i1 + 1
        i = i + 1

i = 0
i1 = -1
i2 = -1
i3 = 0
for line in csv_reader4:
    if len(line) == 0:
        i = i + 1
    elif len(line) == 1:
        if i1 != i:
            i1 = i
            segmented_dataset_L1.append([i1])
            i2 = i2 + 1
            segmented_dataset_L1[i2].append([])
            i3 = 1
        else:
            segmented_dataset_L1[i2].append([])
            i3 = i3 + 1
    elif len(line) == 3:
        #print(i,i1,i2)
        segmented_dataset_L1[i2][i3].append([int(line[0]), int(line[1]), int(line[2])])
                        
#print('combined dataset')
#for i in combined_dataset[1]:
#    print(i)

#print()
#print('segmented dataset')
#for i in segmented_dataset[1]:
#    print(i)

L_1_2_grid = [] # grid to store all L2_4 values [y, x, 1 or 2, index]
i1 = 0
while (i1 < y_axis):
    L_1_2_grid.append([])
    i2 = 0
    while (i2 < x_axis):
        L_1_2_grid[i1].append([])
        i2 = i2 + 1
    i1 = i1 + 1
    
final_dataset = []
# delete combined_dataset[j] after aceessing it
i1 = 0
i = -1
while (i1 < len(combined_dataset)):
    final_dataset.append([])
    i = i + 1
    for i2 in combined_dataset[i1]:
        i2_y_val = int(i2[0][0] / x_total) # x_axis
        i2_x_val = i2[0][0] - (x_total * i2_y_val)
        i2_x_val = i2_x_val * 100
        i2_y_val = i2_y_val * 100
        #if i == 1:
        #    print(i2[0], i2_x_val, i2_y_val, i2[0][0] / x_total, int(i2[0][0] / x_total), math.ceil(i2[0][0] / x_total))
        for i3 in range(1, len(i2)):
            for i4 in range(i2[i3][1], i2[i3][2] + 1):
                final_dataset[i].append([i2_y_val + i2[i3][0], i2_x_val + i4])
    del combined_dataset[i1]

final_dataset_2 = []
# delete segmented_dataset[j] after aceessing it
i1 = 0
i = -1
temp1 = -1
while (i1 < len(segmented_dataset)):    
    i = i + 1
    temp2 = segmented_dataset[i1][0]
    i1_y_val = int(temp2 / x_total)
    i1_x_val = temp2 - (x_total * i1_y_val)
    i1_y_val = i1_y_val * 100
    i1_x_val = i1_x_val * 100
    for i2 in range(1, len(segmented_dataset[i1])):
        final_dataset_2.append([])
        temp1 = temp1 + 1
        for i3 in segmented_dataset[i1][i2]:
            for i4 in range(i3[1], i3[2] + 1):
                final_dataset_2[temp1].append([i1_y_val + i3[0], i1_x_val + i4])
    del segmented_dataset[i1]

final_dataset_L1 = []
# delete combined_dataset_L1[j] after aceessing it
i1 = 0
i = -1
while (i1 < len(combined_dataset_L1)):
    final_dataset_L1.append([])
    i = i + 1
    for i2 in combined_dataset_L1[i1]:
        i2_y_val = int(i2[0][0] / x_total) # x_axis
        i2_x_val = i2[0][0] - (x_total * i2_y_val)
        i2_x_val = i2_x_val * 100
        i2_y_val = i2_y_val * 100
        #if i == 1:
        #    print(i2[0], i2_x_val, i2_y_val, i2[0][0] / x_total, int(i2[0][0] / x_total), math.ceil(i2[0][0] / x_total))
        for i3 in range(1, len(i2)):
            for i4 in range(i2[i3][1], i2[i3][2] + 1):
                final_dataset_L1[i].append([i2_y_val + i2[i3][0], i2_x_val + i4])
    del combined_dataset_L1[i1]

final_dataset_2_L1 = []
# delete segmented_dataset_L1[j] after aceessing it
i1 = 0
i = -1
temp1 = -1
while (i1 < len(segmented_dataset_L1)):    
    i = i + 1
    temp2 = segmented_dataset_L1[i1][0]
    i1_y_val = int(temp2 / x_total)
    i1_x_val = temp2 - (x_total * i1_y_val)
    i1_y_val = i1_y_val * 100
    i1_x_val = i1_x_val * 100
    for i2 in range(1, len(segmented_dataset_L1[i1])):
        final_dataset_2_L1.append([])
        temp1 = temp1 + 1
        for i3 in segmented_dataset_L1[i1][i2]:
            for i4 in range(i3[1], i3[2] + 1):
                final_dataset_2_L1[temp1].append([i1_y_val + i3[0], i1_x_val + i4])
    del segmented_dataset_L1[i1]
        
#for i in range(4):
#    print(final_dataset_2[i])
#    print()
    
def elem_0(val_final):
    return val_final[0]

def elem_1(val_final):
    return val_final[1]

for i in final_dataset:
    #i.sort(key = elem_0)
    i.sort() # 2nd, 3rd numbers are sorted after the 1st number

for i in final_dataset_2:
    #i.sort(key = elem_0)
    i.sort()
    
for i in final_dataset_L1:
    #i.sort(key = elem_0)
    i.sort()

for i in final_dataset_2_L1:
    #i.sort(key = elem_0)
    i.sort()
         
final_dataset_acinar_1_2 = [] # L2 indices list, L1 indices list, total L1

for i in final_dataset:
    print(len(i))
#print(final_dataset[0][0], final_dataset[0][5], final_dataset[0][10], final_dataset[0][5000])
print()
# arrange pixels in rows of lists
if len(final_dataset) == 1 and final_dataset[0] == []:
    pass
else:
    i1 = 0
    while (i1 < len(final_dataset)):
        final_dataset[i1].append([final_dataset[i1][0]])
        del final_dataset[i1][0]
        
        temp1 = len(final_dataset[i1]) - 1
        i = 0
        while (len(final_dataset[i1][i]) == 2):
            if isinstance(final_dataset[i1][i][0], int):
                #i2 = i + 1
                i2 = temp1
                flag1 = 0
                while (i2 < len(final_dataset[i1])):
                    if isinstance(final_dataset[i1][i2][0], list):
                        # if equal then add to this nested list
                        if final_dataset[i1][i][0] == final_dataset[i1][i2][0][0]: 
                            final_dataset[i1][i2].append(final_dataset[i1][i])
                            #del final_dataset[i1][i2]
                            flag1 = 1
                            break
                    i2 = i2 + 1
                #print('i2: ', i2, i1, len(final_dataset[i1]) - 1)
                if i2 == len(final_dataset[i1]):
                    final_dataset[i1].append([final_dataset[i1][i]])
                    del final_dataset[i1][i]
                if flag1 == 1:
                    del final_dataset[i1][i]
                    temp1 = temp1 - 1
            else:
                break
        #print(i1)
        i1 = i1 + 1
    
    #for i in final_dataset[0]:
    #    print(i)

i1 = 0
while (i1 < len(final_dataset_2)):
    final_dataset_2[i1].append([final_dataset_2[i1][0]])
    del final_dataset_2[i1][0]
    
    temp1 = len(final_dataset_2[i1]) - 1
    i = 0
    while (len(final_dataset_2[i1][i]) == 2):
        if isinstance(final_dataset_2[i1][i][0], int):
            #i2 = i + 1
            i2 = temp1
            flag1 = 0
            while (i2 < len(final_dataset_2[i1])):
                if isinstance(final_dataset_2[i1][i2][0], list):
                    # if equal then add to this nested list
                    if final_dataset_2[i1][i][0] == final_dataset_2[i1][i2][0][0]: 
                        final_dataset_2[i1][i2].append(final_dataset_2[i1][i])
                        #del final_dataset[i1][i2]
                        flag1 = 1
                        break
                i2 = i2 + 1
            if i2 == len(final_dataset_2[i1]):
                final_dataset_2[i1].append([final_dataset_2[i1][i]])
                del final_dataset_2[i1][i]
            if flag1 == 1:
                del final_dataset_2[i1][i]
                temp1 = temp1 - 1
        else:
            break
    #print(i1)
    i1 = i1 + 1
       
print()

if len(final_dataset_L1) == 1 and final_dataset_L1[0] == []:
    pass
else:
    i1 = 0
    while (i1 < len(final_dataset_L1)):
        final_dataset_L1[i1].append([final_dataset_L1[i1][0]])
        del final_dataset_L1[i1][0]
        
        temp1 = len(final_dataset_L1[i1]) - 1
        i = 0
        while (len(final_dataset_L1[i1][i]) == 2):
            if isinstance(final_dataset_L1[i1][i][0], int):
                #i2 = i + 1
                i2 = temp1
                flag1 = 0
                while (i2 < len(final_dataset_L1[i1])):
                    if isinstance(final_dataset_L1[i1][i2][0], list):
                        # if equal then add to this nested list
                        if final_dataset_L1[i1][i][0] == final_dataset_L1[i1][i2][0][0]: 
                            final_dataset_L1[i1][i2].append(final_dataset_L1[i1][i])
                            #del final_dataset_L1[i1][i2]
                            flag1 = 1
                            break
                    i2 = i2 + 1
                if i2 == len(final_dataset_L1[i1]):
                    final_dataset_L1[i1].append([final_dataset_L1[i1][i]])
                    del final_dataset_L1[i1][i]
                if flag1 == 1:
                    del final_dataset_L1[i1][i]
                    temp1 = temp1 - 1
            else:
                break
        #print(i1)
        i1 = i1 + 1

i1 = 0
while (i1 < len(final_dataset_2_L1)):
    final_dataset_2_L1[i1].append([final_dataset_2_L1[i1][0]])
    del final_dataset_2_L1[i1][0]
    
    temp1 = len(final_dataset_2_L1[i1]) - 1
    i = 0
    while (len(final_dataset_2_L1[i1][i]) == 2):
        if isinstance(final_dataset_2_L1[i1][i][0], int):
            #i2 = i + 1
            i2 = temp1
            flag1 = 0
            while (i2 < len(final_dataset_2_L1[i1])):
                if isinstance(final_dataset_2_L1[i1][i2][0], list):
                    # if equal then add to this nested list
                    if final_dataset_2_L1[i1][i][0] == final_dataset_2_L1[i1][i2][0][0]: 
                        final_dataset_2_L1[i1][i2].append(final_dataset_2_L1[i1][i])
                        #del final_dataset_2_L1[i1][i2]
                        flag1 = 1
                        break
                i2 = i2 + 1
            if i2 == len(final_dataset_2_L1[i1]):
                final_dataset_2_L1[i1].append([final_dataset_2_L1[i1][i]])
                del final_dataset_2_L1[i1][i]
            if flag1 == 1:
                del final_dataset_2_L1[i1][i]
                temp1 = temp1 - 1
        else:
            break
    #print(i1)
    i1 = i1 + 1
                    
#for i in final_dataset_2_L1[0]:
#    print(i)

x_total_list = []
y_total_list = []
x_min_list = []
x_max_list = []
y_min_list = []
y_max_list = []
x_total_2_list = []
y_total_2_list = []
x_min_2_list = []
x_max_2_list = []
y_min_2_list = []
y_max_2_list = []
x_total_L1_list = []
y_total_L1_list = []
x_min_L1_list = []
x_max_L1_list = []
y_min_L1_list = []
y_max_L1_list = []
x_total_2_L1_list = []
y_total_2_L1_list = []
x_min_2_L1_list = []
x_max_2_L1_list = []
y_min_2_L1_list = []
y_max_2_L1_list = []

def dataset_xy_limits(input_dataset, x_total, y_total, x_min, y_min, x_max, y_max):
    i1 = 0
    while (i1 < len(input_dataset)):
        # find x_total and y_total
        x_total.append(0)
        y_total.append(len(input_dataset[i1]))
        x_min.append(0)
        y_min.append(0)
        x_max.append(0)
        y_max.append(0)
        
        i = 0
        while (i < len(input_dataset[i1])):
            j1 = 0
            while (j1 < len(input_dataset[i1][i])):
                if x_max[i1] < input_dataset[i1][i][j1][1]:
                    x_max[i1] = input_dataset[i1][i][j1][1]
                j1 = j1 + 1
            i = i + 1
        x_min[i1] = x_max[i1]
        i = 0
        while (i < len(input_dataset[i1])):
            j1 = 0
            while (j1 < len(input_dataset[i1][i])):
                if x_min[i1] > input_dataset[i1][i][j1][1]:
                    x_min[i1] = input_dataset[i1][i][j1][1]
                j1 = j1 + 1
            i = i + 1
        
        x_total[i1] = x_max[i1] - x_min[i1] + 1
        #print()
        #print(x_min,x_max,x_total)
        
        y_min[i1] = input_dataset[i1][0][0][0]
        y_max[i1] = input_dataset[i1][-1][0][0]
        #print(y_min,y_max,y_total)
        #print('1 i1:', i1)
            
        i1 = i1 + 1
   
# add L2 values to L_1_2_grid
i1 = 0
while (i1 < len(final_dataset)):
    i2 = 0
    while (i2 < len(final_dataset[i1])):
        i3 = 0
        while (i3 < len(final_dataset[i1][i2])):
            L_1_2_grid[final_dataset[i1][i2][i3][0]][final_dataset[i1][i2][i3][1]].append(1)
            L_1_2_grid[final_dataset[i1][i2][i3][0]][final_dataset[i1][i2][i3][1]].append(i1)
            i3 = i3 + 1
        i2 = i2 + 1
    i1 = i1 + 1
i1 = 0
while (i1 < len(final_dataset_2)):
    i2 = 0
    while (i2 < len(final_dataset_2[i1])):
        i3 = 0
        while (i3 < len(final_dataset_2[i1][i2])):
            L_1_2_grid[final_dataset_2[i1][i2][i3][0]][final_dataset_2[i1][i2][i3][1]].append(2)
            L_1_2_grid[final_dataset_2[i1][i2][i3][0]][final_dataset_2[i1][i2][i3][1]].append(i1)
            i3 = i3 + 1
        i2 = i2 + 1
    i1 = i1 + 1
    
# identify XY limits of dataset
if len(final_dataset) == 1 and final_dataset[0] == []:
    pass
else:
    dataset_xy_limits(final_dataset, x_total_list, y_total_list, x_min_list, y_min_list, x_max_list, y_max_list)
dataset_xy_limits(final_dataset_2, x_total_2_list, y_total_2_list, x_min_2_list, y_min_2_list, x_max_2_list, y_max_2_list)
if len(final_dataset_L1) == 1 and final_dataset_L1[0] == []:
    pass
else:
    dataset_xy_limits(final_dataset_L1, x_total_L1_list, y_total_L1_list, x_min_L1_list, y_min_L1_list, x_max_L1_list, y_max_L1_list)
dataset_xy_limits(final_dataset_2_L1, x_total_2_L1_list, y_total_2_L1_list, x_min_2_L1_list, y_min_2_L1_list, x_max_2_L1_list, y_max_2_L1_list)

# detect adjacency between black and gray areas

if len(final_dataset_L1) == 1 and final_dataset_L1[0] == []:
    pass
else:
    i1 = 0
    while (i1 < len(final_dataset_L1)):
        grid_values = []
        final_dataset_acinar_1_2.append([[],[[1, i1]],0])
        temp2 = len(final_dataset_acinar_1_2) - 1 # index where values are to be added
        j1 = 0
        while (j1 < y_total_L1_list[i1]):
            grid_values.append([])
            j2 = 0
            while (j2 < x_total_L1_list[i1]):
                grid_values[j1].append([])
                j2 = j2 + 1
            j1 = j1 + 1
        
        i2 = 0
        while (i2 < len(final_dataset_L1[i1])):
            i3 = 0
            while (i3 < len(final_dataset_L1[i1][i2])):
                #grid_values[i2][i3].append(final_dataset_L1[i1][i2][i3][0])
                #grid_values[i2][i3].append(final_dataset_L1[i1][i2][i3][1])
                grid_values[final_dataset_L1[i1][i2][i3][0] - y_min_L1_list[i1]][final_dataset_L1[i1][i2][i3][1] - x_min_L1_list[i1]].append(final_dataset_L1[i1][i2][i3][0])
                grid_values[final_dataset_L1[i1][i2][i3][0] - y_min_L1_list[i1]][final_dataset_L1[i1][i2][i3][1] - x_min_L1_list[i1]].append(final_dataset_L1[i1][i2][i3][1])
                i3 = i3 + 1
            i2 = i2 + 1
        
        i = 0
        while (i < len(grid_values)):
            i3 = 0
            while (i3 < len(grid_values[i])):
                temp1 = []
                flag2 = -1
                if grid_values[i][i3] != []:
                    if grid_values[i][i3][0] == 0:
                        flag2 = 1
                    elif grid_values[i][i3][0] == y_axis - 1:
                        flag2 = 2
                    else:
                        flag2 = 0
                
                if flag2 == 0:
                    if i3 == 0:
                        if ((grid_values[i][i3][1] - 1) < 0): # if x - 1 < 0
                            # checking left side is not possible
                            if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                                if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            else:
                                if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                                #if L_1_2_grid[grid_values[i + 1][i3][0]][grid_values[i + 1][i3][1]] != []:
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                            else:
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                            if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                        else:
                            #if (grid_values[i][i3 - 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                            if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                                if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            else:
                                if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                            else:
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                            if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                    elif i3 == len(grid_values[i]) - 1:
                        if (grid_values[i][i3][1] + 1) == x_axis: # if x + 1 == x_axis
                            if (grid_values[i][i3 - 1] == []):
                                if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                            if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                            else:
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                            if ((i + 1) < len(grid_values)) and grid_values[i + 1][i3] != [] and L_1_2_grid[grid_values[i + 1][i3][0] - 1][grid_values[i + 1][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i + 1][i3][0] - 1][grid_values[i + 1][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i + 1][i3][0] - 1][grid_values[i + 1][i3][1]])
                        else:
                            if (grid_values[i][i3 - 1] == []):
                                if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                            #elif (grid_values[i][i3 + 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                            else:
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                            if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                    else:
                        if (grid_values[i][i3 - 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                        if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        else:
                            if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        else:
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                
                elif flag2 == 1:
                    if i3 == 0:
                        if ((grid_values[i][i3][1] - 1) < 0): # if x - 1 < 0
                            # checking left side is not possible
                            if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                                if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            else:
                                if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                            else:
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        else:
                            #if (grid_values[i][i3 - 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                            if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                                if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            else:
                                if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                            else:
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                    elif i3 == len(grid_values[i]) - 1:
                        if (grid_values[i][i3][1] + 1) == x_axis: # if x + 1 == x_axis
                            if (grid_values[i][i3 - 1] == []):
                                if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                            if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                            else:
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        else:
                            if (grid_values[i][i3 - 1] == []):
                                if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                            #elif (grid_values[i][i3 + 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                            else:
                                if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                    else:
                        if (grid_values[i][i3 - 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                        if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        else:
                            if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        else:
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                elif flag2 == 2:
                    if i3 == 0:
                        if ((grid_values[i][i3][1] - 1) < 0): # if x - 1 < 0
                            # checking left side is not possible
                            if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                                if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            else:
                                if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                        else:
                            #if (grid_values[i][i3 - 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                            if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                                if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            else:
                                if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                    if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                        temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                    elif i3 == len(grid_values[i]) - 1:
                        if (grid_values[i][i3][1] + 1) == x_axis: # if x + 1 == x_axis
                            if (grid_values[i][i3 - 1] == []):
                                if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                            if ((i + 1) < len(grid_values)) and grid_values[i + 1][i3] != [] and L_1_2_grid[grid_values[i + 1][i3][0] - 1][grid_values[i + 1][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i + 1][i3][0] - 1][grid_values[i + 1][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i + 1][i3][0] - 1][grid_values[i + 1][i3][1]])
                        else:
                            if (grid_values[i][i3 - 1] == []):
                                if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                            #elif (grid_values[i][i3 + 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                            if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                    else:
                        if (grid_values[i][i3 - 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                        if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        else:
                            if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                
                if temp1 != []:                        
                    j1 = len(final_dataset_acinar_1_2) - 1 # doubtful
                    flag1 = 0
                    while (j1 >= 0):
                        if j1 != temp2:
                            for k_1 in temp1:
                                j2 = len(final_dataset_acinar_1_2[j1][0]) - 1
                                while (j2 >= 0):
                                    if final_dataset_acinar_1_2[j1][0][j2] == k_1: #temp1
                                        # add elements from last list to this list
                                        j3 = 0
                                        while (j3 < len(final_dataset_acinar_1_2[temp2][0])):
                                            j4 = len(final_dataset_acinar_1_2[j1][0]) - 1
                                            flag3 = 0
                                            while (j4 >= 0):
                                                if final_dataset_acinar_1_2[j1][0][j4] == final_dataset_acinar_1_2[temp2][0][j3]:
                                                    flag3 = 1
                                                    break
                                                j4 = j4 - 1
                                            if flag3 == 0: #j4 == -1:
                                                final_dataset_acinar_1_2[j1][0].append(final_dataset_acinar_1_2[temp2][0][j3])
                                            #if final_dataset_acinar_1_2[j1][0].__contains__(final_dataset_acinar_1_2[temp2][0][j3]) == False:
                                            #    final_dataset_acinar_1_2[j1][0].append(final_dataset_acinar_1_2[temp2][0][j3])
                                            j3 = j3 + 1
                                        j3 = 0
                                        while (j3 < len(final_dataset_acinar_1_2[temp2][1])):
                                            j4 = len(final_dataset_acinar_1_2[j1][1]) - 1
                                            flag3 = 0
                                            while (j4 >= 0):
                                                if final_dataset_acinar_1_2[j1][1][j4] == final_dataset_acinar_1_2[temp2][1][j3]:
                                                    flag3 = 1
                                                    break
                                                j4 = j4 - 1
                                            if flag3 == 0: #j4 == -1:
                                                final_dataset_acinar_1_2[j1][1].append(final_dataset_acinar_1_2[temp2][1][j3])
                                            j3 = j3 + 1
                                        final_dataset_acinar_1_2[j1][2] = len(final_dataset_acinar_1_2[j1][1])
                                        del final_dataset_acinar_1_2[temp2]
                                        if temp2 > j1:
                                            temp2 = j1
                                        else:
                                            temp2 = j1 - 1
                                        
                                        flag1 = 1
                                        break
                                    j2 = j2 - 1
                                if j2 >= 0:
                                    break
                        j1 = j1 - 1
                    if flag1 == 0:
                        if len(final_dataset_acinar_1_2[temp2][0]) == 0:
                            for k_1 in temp1:
                                final_dataset_acinar_1_2[temp2][0].append(k_1)
                        else:
                            for k_1 in temp1:
                                j2 = len(final_dataset_acinar_1_2[temp2][0]) - 1
                                while (j2 >= 0):
                                    if final_dataset_acinar_1_2[temp2][0][j2] == k_1:
                                        break
                                    j2 = j2 - 1
                                if j2 == -1:
                                    final_dataset_acinar_1_2[temp2][0].append(k_1)
                        final_dataset_acinar_1_2[temp2][2] = len(final_dataset_acinar_1_2[temp2][1])
                i3 = i3 + 1
            i = i + 1
            
        i1 = i1 + 1

i1 = 0
while (i1 < len(final_dataset_2_L1)):
    grid_values = []
    final_dataset_acinar_1_2.append([[],[[2, i1]],0])
    temp2 = len(final_dataset_acinar_1_2) - 1 # index where values are to be added
    j1 = 0
    while (j1 < y_total_2_L1_list[i1]):
        grid_values.append([])
        j2 = 0
        while (j2 < x_total_2_L1_list[i1]):
            grid_values[j1].append([])
            j2 = j2 + 1
        j1 = j1 + 1
    
    i2 = 0
    while (i2 < len(final_dataset_2_L1[i1])):
        i3 = 0
        while (i3 < len(final_dataset_2_L1[i1][i2])):
            #grid_values[i2][i3].append(final_dataset_2_L1[i1][i2][i3][0])
            #grid_values[i2][i3].append(final_dataset_2_L1[i1][i2][i3][1])
            grid_values[final_dataset_2_L1[i1][i2][i3][0] - y_min_2_L1_list[i1]][final_dataset_2_L1[i1][i2][i3][1] - x_min_2_L1_list[i1]].append(final_dataset_2_L1[i1][i2][i3][0])
            grid_values[final_dataset_2_L1[i1][i2][i3][0] - y_min_2_L1_list[i1]][final_dataset_2_L1[i1][i2][i3][1] - x_min_2_L1_list[i1]].append(final_dataset_2_L1[i1][i2][i3][1])
            i3 = i3 + 1
        i2 = i2 + 1
    
    i = 0
    while (i < len(grid_values)):
        i3 = 0
        while (i3 < len(grid_values[i])):
            temp1 = []
            flag2 = -1
            if grid_values[i][i3] != []:
                if grid_values[i][i3][0] == 0:
                    flag2 = 1
                elif grid_values[i][i3][0] == y_axis - 1:
                    flag2 = 2
                else:
                    flag2 = 0
            
            if flag2 == 0:
                if i3 == 0:
                    if ((grid_values[i][i3][1] - 1) < 0): # if x - 1 < 0
                        # checking left side is not possible
                        if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        else:
                            if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                            #if L_1_2_grid[grid_values[i + 1][i3][0]][grid_values[i + 1][i3][1]] != []:
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        else:
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                    else:
                        #if (grid_values[i][i3 - 1] == []):
                        if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                            temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                        if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        else:
                            if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        else:
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                elif i3 == len(grid_values[i]) - 1:
                    if (grid_values[i][i3][1] + 1) == x_axis: # if x + 1 == x_axis
                        if (grid_values[i][i3 - 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                        if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) # AFTER THIS
                        else:
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) # AFTER THIS
                        if ((i + 1) < len(grid_values)) and grid_values[i + 1][i3] != [] and L_1_2_grid[grid_values[i + 1][i3][0] - 1][grid_values[i + 1][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i + 1][i3][0] - 1][grid_values[i + 1][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i + 1][i3][0] - 1][grid_values[i + 1][i3][1]])
                    else:
                        if (grid_values[i][i3 - 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                        #elif (grid_values[i][i3 + 1] == []):
                        if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        else:
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                else:
                    if (grid_values[i][i3 - 1] == []):
                        if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                            temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                    if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                        if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                    else:
                        if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                    if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                        if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                    else:
                        if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                    if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                        if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                            temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
            
            elif flag2 == 1:
                if i3 == 0:
                    if ((grid_values[i][i3][1] - 1) < 0): # if x - 1 < 0
                        # checking left side is not possible
                        if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        else:
                            if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        else:
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                    else:
                        #if (grid_values[i][i3 - 1] == []):
                        if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                            temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                        if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        else:
                            if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        else:
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                elif i3 == len(grid_values[i]) - 1:
                    if (grid_values[i][i3][1] + 1) == x_axis: # if x + 1 == x_axis
                        if (grid_values[i][i3 - 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                        if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        else:
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                    else:
                        if (grid_values[i][i3 - 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                        #elif (grid_values[i][i3 + 1] == []):
                        if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                        else:
                            if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                else:
                    if (grid_values[i][i3 - 1] == []):
                        if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                            temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                    if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                        if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                    else:
                        if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                    if ((i + 1) < len(grid_values)) and (grid_values[i + 1][i3] == []):
                        if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                    else:
                        if L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0] + 1][grid_values[i][i3][1]])
                                
            elif flag2 == 2:
                if i3 == 0:
                    if ((grid_values[i][i3][1] - 1) < 0): # if x - 1 < 0
                        # checking left side is not possible
                        if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        else:
                            if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                    else:
                        #if (grid_values[i][i3 - 1] == []):
                        if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                            temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                        if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        else:
                            if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                                if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                    temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                elif i3 == len(grid_values[i]) - 1:
                    if (grid_values[i][i3][1] + 1) == x_axis: # if x + 1 == x_axis
                        if (grid_values[i][i3 - 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                        if ((i + 1) < len(grid_values)) and grid_values[i + 1][i3] != [] and L_1_2_grid[grid_values[i + 1][i3][0] - 1][grid_values[i + 1][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i + 1][i3][0] - 1][grid_values[i + 1][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i + 1][i3][0] - 1][grid_values[i + 1][i3][1]])
                    else:
                        if (grid_values[i][i3 - 1] == []):
                            if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                        #elif (grid_values[i][i3 + 1] == []):
                        if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                        if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
                else:
                    if (grid_values[i][i3 - 1] == []):
                        if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1] != []:
                            temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] - 1])
                    if ((i3 + 1) < len(grid_values[i])) and (grid_values[i][i3 + 1] == []):
                        if L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                    else:
                        if (grid_values[i][i3][1] + 1 < len(L_1_2_grid[grid_values[i][i3][0]])) and L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1] != []:
                            if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1]) == False:
                                temp1.append(L_1_2_grid[grid_values[i][i3][0]][grid_values[i][i3][1] + 1])
                    if L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]] != []:
                        if temp1.__contains__(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]]) == False:
                            temp1.append(L_1_2_grid[grid_values[i][i3][0] - 1][grid_values[i][i3][1]])
            
            if temp1 != []:    
                j1 = len(final_dataset_acinar_1_2) - 1 # doubtful
                flag1 = 0
                while (j1 >= 0):
                    if j1 != temp2:
                        for k_1 in temp1:
                            j2 = len(final_dataset_acinar_1_2[j1][0]) - 1
                            while (j2 >= 0):
                                if final_dataset_acinar_1_2[j1][0][j2] == k_1: #temp1
                                    # add elements from last list to this list
                                    j3 = 0
                                    while (j3 < len(final_dataset_acinar_1_2[temp2][0])):
                                        j4 = len(final_dataset_acinar_1_2[j1][0]) - 1
                                        flag3 = 0
                                        while (j4 >= 0):
                                            if final_dataset_acinar_1_2[j1][0][j4] == final_dataset_acinar_1_2[temp2][0][j3]:
                                                flag3 = 1
                                                break
                                            j4 = j4 - 1
                                        if flag3 == 0: #j4 == -1:
                                            final_dataset_acinar_1_2[j1][0].append(final_dataset_acinar_1_2[temp2][0][j3])
                                        #if final_dataset_acinar_1_2[j1][0].__contains__(final_dataset_acinar_1_2[temp2][0][j3]) == False:
                                        #    final_dataset_acinar_1_2[j1][0].append(final_dataset_acinar_1_2[temp2][0][j3])
                                        j3 = j3 + 1
                                    j3 = 0
                                    while (j3 < len(final_dataset_acinar_1_2[temp2][1])):
                                        j4 = len(final_dataset_acinar_1_2[j1][1]) - 1
                                        flag3 = 0
                                        while (j4 >= 0):
                                            if final_dataset_acinar_1_2[j1][1][j4] == final_dataset_acinar_1_2[temp2][1][j3]:
                                                flag3 = 1
                                                break
                                            j4 = j4 - 1
                                        if flag3 == 0: #j4 == -1:
                                            final_dataset_acinar_1_2[j1][1].append(final_dataset_acinar_1_2[temp2][1][j3])
                                        j3 = j3 + 1
                                    final_dataset_acinar_1_2[j1][2] = len(final_dataset_acinar_1_2[j1][1])
                                    del final_dataset_acinar_1_2[temp2]
                                    if temp2 > j1:
                                        temp2 = j1
                                    else:
                                        temp2 = j1 - 1
                                    
                                    flag1 = 1
                                    break
                                j2 = j2 - 1
                            if j2 >= 0:
                                break
                    j1 = j1 - 1
                if flag1 == 0:
                    if len(final_dataset_acinar_1_2[temp2][0]) == 0:
                        for k_1 in temp1:
                            final_dataset_acinar_1_2[temp2][0].append(k_1)
                    else:
                        for k_1 in temp1:
                            j2 = len(final_dataset_acinar_1_2[temp2][0]) - 1
                            while (j2 >= 0):
                                if final_dataset_acinar_1_2[temp2][0][j2] == k_1:
                                    break
                                j2 = j2 - 1
                            if j2 == -1:
                                final_dataset_acinar_1_2[temp2][0].append(k_1)
                    final_dataset_acinar_1_2[temp2][2] = len(final_dataset_acinar_1_2[temp2][1])
            i3 = i3 + 1
        i = i + 1
            
    i1 = i1 + 1
    
# add L1 values to L_1_2_grid
i1 = 0
while (i1 < len(final_dataset_L1)):
    i2 = 0
    while (i2 < len(final_dataset_L1[i1])):
        i3 = 0
        while (i3 < len(final_dataset_L1[i1][i2])):
            L_1_2_grid[final_dataset_L1[i1][i2][i3][0]][final_dataset_L1[i1][i2][i3][1]].append(0)
            # append only one value (like '0') since L1 positions are not referred for joining groups
            i3 = i3 + 1
        i2 = i2 + 1
    i1 = i1 + 1
i1 = 0
while (i1 < len(final_dataset_2_L1)):
    i2 = 0
    while (i2 < len(final_dataset_2_L1[i1])):
        i3 = 0
        while (i3 < len(final_dataset_2_L1[i1][i2])):
            L_1_2_grid[final_dataset_2_L1[i1][i2][i3][0]][final_dataset_2_L1[i1][i2][i3][1]].append(0)
            i3 = i3 + 1
        i2 = i2 + 1
    i1 = i1 + 1

print()
# detect valid acinar as per no. of L1_4 sets
i1 = 0
while (i1 < len(final_dataset_acinar_1_2)):
    if final_dataset_acinar_1_2[i1][2] >= 3:
        i1 = i1 + 1
    else:
        del final_dataset_acinar_1_2[i1]

# concatanate all groups in final_dataset_acinar_1_2
x_min_1_2_list = []
x_max_1_2_list = []
y_min_1_2_list = []
y_max_1_2_list = []

final_1_2_concatanate = []

# find limits of final_1_2_concatanate
i1 = 0
while (i1 < len(final_dataset_acinar_1_2)):    
    x_max_1_2_list.append(0)
    y_max_1_2_list.append(0)
    
    i = 0
    while (i < len(final_dataset_acinar_1_2[i1][0])):
        if final_dataset_acinar_1_2[i1][0][i][0] == 1:
            if x_max_1_2_list[i1] < x_max_list[final_dataset_acinar_1_2[i1][0][i][1]]:
                x_max_1_2_list[i1] = x_max_list[final_dataset_acinar_1_2[i1][0][i][1]]
            if y_max_1_2_list[i1] < y_max_list[final_dataset_acinar_1_2[i1][0][i][1]]:
                y_max_1_2_list[i1] = y_max_list[final_dataset_acinar_1_2[i1][0][i][1]]
        else:
            if x_max_1_2_list[i1] < x_max_2_list[final_dataset_acinar_1_2[i1][0][i][1]]:
                x_max_1_2_list[i1] = x_max_2_list[final_dataset_acinar_1_2[i1][0][i][1]]
            if y_max_1_2_list[i1] < y_max_2_list[final_dataset_acinar_1_2[i1][0][i][1]]:
                y_max_1_2_list[i1] = y_max_2_list[final_dataset_acinar_1_2[i1][0][i][1]]
        i = i + 1
    
    i = 0
    while (i < len(final_dataset_acinar_1_2[i1][1])):
        if final_dataset_acinar_1_2[i1][1][i][0] == 1:
            if x_max_1_2_list[i1] < x_max_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]:
                x_max_1_2_list[i1] = x_max_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]
            if y_max_1_2_list[i1] < y_max_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]:
                y_max_1_2_list[i1] = y_max_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]
        else:
            if x_max_1_2_list[i1] < x_max_2_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]:
                x_max_1_2_list[i1] = x_max_2_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]
            if y_max_1_2_list[i1] < y_max_2_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]:
                y_max_1_2_list[i1] = y_max_2_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]
        i = i + 1
    
    x_min_1_2_list.append(x_max_1_2_list[i1])
    y_min_1_2_list.append(x_max_1_2_list[i1])    
    
    i = 0
    while (i < len(final_dataset_acinar_1_2[i1][0])):
        if final_dataset_acinar_1_2[i1][0][i][0] == 1:
            if x_min_1_2_list[i1] > x_min_list[final_dataset_acinar_1_2[i1][0][i][1]]:
                x_min_1_2_list[i1] = x_min_list[final_dataset_acinar_1_2[i1][0][i][1]]
            if y_min_1_2_list[i1] > y_min_list[final_dataset_acinar_1_2[i1][0][i][1]]:
                y_min_1_2_list[i1] = y_min_list[final_dataset_acinar_1_2[i1][0][i][1]]
        else:
            if x_min_1_2_list[i1] > x_min_2_list[final_dataset_acinar_1_2[i1][0][i][1]]:
                x_min_1_2_list[i1] = x_min_2_list[final_dataset_acinar_1_2[i1][0][i][1]]
            if y_min_1_2_list[i1] > y_min_2_list[final_dataset_acinar_1_2[i1][0][i][1]]:
                y_min_1_2_list[i1] = y_min_2_list[final_dataset_acinar_1_2[i1][0][i][1]]
        i = i + 1
    
    i = 0
    while (i < len(final_dataset_acinar_1_2[i1][1])):
        if final_dataset_acinar_1_2[i1][1][i][0] == 1:
            if x_min_1_2_list[i1] > x_min_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]:
                x_min_1_2_list[i1] = x_min_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]
            if y_min_1_2_list[i1] > y_min_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]:
                y_min_1_2_list[i1] = y_min_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]
        else:
            if x_min_1_2_list[i1] > x_min_2_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]:
                x_min_1_2_list[i1] = x_min_2_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]
            if y_min_1_2_list[i1] > y_min_2_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]:
                y_min_1_2_list[i1] = y_min_2_L1_list[final_dataset_acinar_1_2[i1][1][i][1]]
        i = i + 1
        
    i1 = i1 + 1

# store adjacent groups in final_1_2_concatanate
i1 = 0
while (i1 < len(final_dataset_acinar_1_2)):
    final_1_2_concatanate.append([])
    for i in range(y_max_1_2_list[i1] - y_min_1_2_list[i1] + 1):
        final_1_2_concatanate[i1].append([])
    
    i = 0
    while (i < len(final_dataset_acinar_1_2[i1][0])):
        if final_dataset_acinar_1_2[i1][0][i][0] == 1:
            y_index = final_dataset[final_dataset_acinar_1_2[i1][0][i][1]][0][0][0]
            y_index = y_index - y_min_1_2_list[i1] - 1 # + 1 when starting from position 0
            j1 = 0
            while (j1 < len(final_dataset[final_dataset_acinar_1_2[i1][0][i][1]])):
                y_index = y_index + 1
                j2 = 0
                while (j2 < len(final_dataset[final_dataset_acinar_1_2[i1][0][i][1]][j1])):
                    final_1_2_concatanate[i1][y_index].append(final_dataset[final_dataset_acinar_1_2[i1][0][i][1]][j1][j2])
                    #print(len(final_1_2_concatanate) - 1, final_dataset[final_dataset_acinar_1_2[i1][0][i][1]][j1][j2][0], y_min_list[final_dataset_acinar_1_2[i1][0][i][1]], y_max_list[final_dataset_acinar_1_2[i1][0][i][1]], y_min_1_2_list[i1], y_max_1_2_list[i1])
                    #final_1_2_concatanate[i1][final_dataset[final_dataset_acinar_1_2[i1][0][i][1]][j1][j2][0] - y_min_1_2_list[i1]].append(final_dataset[final_dataset_acinar_1_2[i1][0][i][1]][j1][j2])
                    j2 = j2 + 1
                j1 = j1 + 1
            
            final_dataset[final_dataset_acinar_1_2[i1][0][i][1]] = []
        else:
            y_index = final_dataset_2[final_dataset_acinar_1_2[i1][0][i][1]][0][0][0]
            y_index = y_index - y_min_1_2_list[i1] - 1 # + 1 when starting from position 0
            j1 = 0
            while (j1 < len(final_dataset_2[final_dataset_acinar_1_2[i1][0][i][1]])):
                y_index = y_index + 1
                j2 = 0
                while (j2 < len(final_dataset_2[final_dataset_acinar_1_2[i1][0][i][1]][j1])):
                    final_1_2_concatanate[i1][y_index].append(final_dataset_2[final_dataset_acinar_1_2[i1][0][i][1]][j1][j2])
                    #print(len(final_1_2_concatanate[i1]) - 1, final_dataset_2[final_dataset_acinar_1_2[i1][0][i][1]][j1][j2][1], y_min_2_list[final_dataset_acinar_1_2[i1][0][i][1]])
                    #final_1_2_concatanate[i1][final_dataset_2[final_dataset_acinar_1_2[i1][0][i][1]][j1][j2][0] - y_min_1_2_list[i1]].append(final_dataset_2[final_dataset_acinar_1_2[i1][0][i][1]][j1][j2])
                    j2 = j2 + 1
                j1 = j1 + 1
            
            final_dataset_2[final_dataset_acinar_1_2[i1][0][i][1]] = []
        i = i + 1
    
    i = 0
    while (i < len(final_dataset_acinar_1_2[i1][1])):
        if final_dataset_acinar_1_2[i1][1][i][0] == 1:
            y_index = final_dataset_L1[final_dataset_acinar_1_2[i1][1][i][1]][0][0][0]
            y_index = y_index - y_min_1_2_list[i1] - 1 # + 1 when starting from position 0
            j1 = 0
            while (j1 < len(final_dataset_L1[final_dataset_acinar_1_2[i1][1][i][1]])):
                y_index = y_index + 1
                j2 = 0
                while (j2 < len(final_dataset_L1[final_dataset_acinar_1_2[i1][1][i][1]][j1])):
                    final_1_2_concatanate[i1][y_index].append(final_dataset_L1[final_dataset_acinar_1_2[i1][1][i][1]][j1][j2])
                    #final_1_2_concatanate[i1][final_dataset_L1[final_dataset_acinar_1_2[i1][1][i][1]][j1][j2][0] - y_min_1_2_list[i1]].append(final_dataset_L1[final_dataset_acinar_1_2[i1][1][i][1]][j1][j2])
                    j2 = j2 + 1
                j1 = j1 + 1
            
            final_dataset_L1[final_dataset_acinar_1_2[i1][1][i][1]] = []
        else:
            y_index = final_dataset_2_L1[final_dataset_acinar_1_2[i1][1][i][1]][0][0][0]
            y_index = y_index - y_min_1_2_list[i1] - 1 # + 1 when starting from position 0
            j1 = 0
            while (j1 < len(final_dataset_2_L1[final_dataset_acinar_1_2[i1][1][i][1]])):
                y_index = y_index + 1
                j2 = 0
                while (j2 < len(final_dataset_2_L1[final_dataset_acinar_1_2[i1][1][i][1]][j1])):
                    final_1_2_concatanate[i1][y_index].append(final_dataset_2_L1[final_dataset_acinar_1_2[i1][1][i][1]][j1][j2])
                    #final_1_2_concatanate[i1][final_dataset_2_L1[final_dataset_acinar_1_2[i1][1][i][1]][j1][j2][0] - y_min_1_2_list[i1]].append(final_dataset_2_L1[final_dataset_acinar_1_2[i1][1][i][1]][j1][j2])
                    j2 = j2 + 1
                j1 = j1 + 1
            
            final_dataset_2_L1[final_dataset_acinar_1_2[i1][1][i][1]] = []
        i = i + 1    
    i1 = i1 + 1

del final_dataset_acinar_1_2

# sort final_1_2_concatanate
i1 = 0
while (i1 < len(final_1_2_concatanate)):
    i2 = 0
    while (i2 < len(final_1_2_concatanate[i1])):
        final_1_2_concatanate[i1][i2].sort(key = elem_1)
        i2 = i2 + 1
    i1 = i1 + 1

# fill gaps in final_1_2_concatanate
i1 = 0
while (i1 < len(final_1_2_concatanate)):
    #print('i1: ', i1)
    if (s_size < (x_max_1_2_list[i1] - x_min_1_2_list[i1] + 1)) or (s_size < (y_max_1_2_list[i1] - y_min_1_2_list[i1] + 1)):
        gaps_list = []
        gaps_list_c = []
        gaps_list_s = []
        segments_1_2 = []
        
        x_1_2_total = math.ceil((x_max_1_2_list[i1] - x_min_1_2_list[i1] + 1) / s_size)
        y_1_2_total = math.ceil((y_max_1_2_list[i1] - y_min_1_2_list[i1] + 1) / s_size)   
        yx_1_2_total = y_1_2_total * x_1_2_total
        
        # not correct
        for i in range(yx_1_2_total): # separate list for each block
            gaps_list_c.append([[],[],[],[]]) # left, right, top, bottom
            gaps_list_s.append([])
            segments_1_2.append([])
            
        # fill segments_1_2
        i2 = 0
        while (i2 < len(final_1_2_concatanate[i1])):
            #print('ERROR: ', i1, final_1_2_concatanate[i1][i2])
            if len(final_1_2_concatanate[i1][i2]) > 0:
                y_value = int((final_1_2_concatanate[i1][i2][0][0] - y_min_1_2_list[i1]) / s_size)
                i3 = 0
                while (i3 < len(final_1_2_concatanate[i1][i2])):
                    x_value = int((final_1_2_concatanate[i1][i2][i3][1] - x_min_1_2_list[i1]) / s_size)
                    yx_value = (x_1_2_total * y_value) + x_value
                    # if len(list) == positio_of_y; len(list) needs to be incremented
                    if len(segments_1_2[yx_value]) <= final_1_2_concatanate[i1][i2][i3][0]:
                        for j in range(len(segments_1_2[yx_value]), final_1_2_concatanate[i1][i2][i3][0] + 1):
                            segments_1_2[yx_value].append([])
                    segments_1_2[yx_value][final_1_2_concatanate[i1][i2][i3][0]].append(final_1_2_concatanate[i1][i2][i3])
                    i3 = i3 + 1
            i2 = i2 + 1
          
        # identify gaps as per blocks # store values in gaps_list_s
        i_0 = 0
        while (i_0 < len(segments_1_2)):
            i = 0
            while (i < len(segments_1_2[i_0])): # final_1_2_concatanate[i1]
                #print('i, i1: ', i, i1)
                j1 = 1
                while (j1 < len(segments_1_2[i_0][i])):
                    if (segments_1_2[i_0][i][j1][1] - segments_1_2[i_0][i][j1 - 1][1] > 1) == True:
                        gap_range = [segments_1_2[i_0][i][j1][0], segments_1_2[i_0][i][j1 - 1][1] + 1, segments_1_2[i_0][i][j1][1] - 1]
                        # search for any adjacency to this range in gaps_list_s[i_0] through reverse order
                        j2 = gap_range[1]
                        flag1 = 0
                        while (j2 <= gap_range[2]):
                            if flag1 == 1:
                                pass
                            else:
                                temp1 = len(gaps_list_s[i_0]) - 1
                                while (temp1 >= 0):
                                    #print(gaps_list_s[i_0][temp1], gaps_list_s[i_0][temp1][1][0][0], gap_range[0], x_total, gap_range[0] - 1)
                                    temp2 = len(gaps_list_s[i_0][temp1]) - 1
                                    while (temp2 > 0): # since 0th position is for checking validity
                                        #print('temp2', gaps_list_s[i_0][temp1])
                                        if gaps_list_s[i_0][temp1][temp2][0][0] == gap_range[0] - 1: # x_total
                                            temp3 = len(gaps_list_s[i_0][temp1][temp2]) - 1
                                            while (temp3 >= 0):
                                                if gaps_list_s[i_0][temp1][temp2][temp3][1] == j2: # gaps_list_s[i_0][temp1][temp2][1]
                                                    gaps_list_s[i_0][temp1].append([])
                                                    j3 = gap_range[1]
                                                    while (j3 <= gap_range[2]):
                                                        gaps_list_s[i_0][temp1][-1].append([gap_range[0],j3])
                                                        j3 = j3 + 1
                                                    break
                                                temp3 = temp3 - 1
                                            if temp3 != -1:
                                                flag1 = 1
                                        elif gaps_list_s[i_0][temp1][temp2][0][0] < gap_range[0] - 1 == True: # x_total
                                            break
                                        temp2 = temp2 - 1
                                    temp1 = temp1 - 1
                            j2 = j2 + 1
                        
                        if flag1 == 0: # j2 == gap_range[2] + 1
                            gaps_list_s[i_0].append([1,[]]) # first layer; 1 -> 0 for invalid
                            j3 = gap_range[1]
                            while (j3 <= gap_range[2]):
                                gaps_list_s[i_0][-1][1].append([gap_range[0],j3])
                                j3 = j3 + 1
                    j1 = j1 + 1
                i = i + 1
            i_0 = i_0 + 1
        
        print('final_1_2_concatanate i1 gaps : ', i1)

        print('final_1_2_concatanate i1 1 : ', i1)
        """# join adjacent gaps as per blocks
        j_0 = 0
        while (j_0 < len(gaps_list_s)):            
            flag2 = 1
            while (flag2 == 1):
                #print('flag2, i1: ', flag2, i1)
                flag2 = 0
                j1 = 0
                while (j1 < len(gaps_list_s[j_0]) - 1):
                    #print('j1, len, i1: ', j1, len(gaps_list) - 1, i1)
                    j2 = len(gaps_list_s[j_0][j1]) - 1
                    while (j2 > 0):
                        j3 = 0
                        while (j3 < len(gaps_list_s[j_0][j1][j2])):
                            k1 = j1 + 1
                            while (k1 < len(gaps_list_s[j_0])):
                                flag1 = 0
                                k2 = 1
                                while (k2 < len(gaps_list_s[j_0][k1])):
                                    k3 = 0
                                    while (k3 < len(gaps_list_s[j_0][k1][k2])):
                                        if gaps_list_s[j_0][k1][k2][k3][1] == gaps_list_s[j_0][j1][j2][j3][1]:
                                            if abs(gaps_list_s[j_0][k1][k2][k3][0] - gaps_list_s[j_0][j1][j2][j3][0]) == 1:
                                                flag1 = 1
                                                temp1 = gaps_list_s[j_0][j1][-1][0][0] # store last Y value of list where pixels are to be added 
                                                k2_a = 1
                                                while ((k2_a < len(gaps_list_s[j_0][k1])) and (gaps_list_s[j_0][k1][k2_a][0][0] <= temp1)): # k2_a < len(gaps_list_s[j_0][k1])
                                                    k3_a = 0
                                                    while (k3_a < len(gaps_list_s[j_0][k1][k2_a])):
                                                        j2_a = 1 # might have to start from the position where Y matches
                                                        while (j2_a < len(gaps_list_s[j_0][j1])):
                                                            if gaps_list_s[j_0][j1][j2_a][0][0] == gaps_list_s[j_0][k1][k2_a][k3_a][0]:
                                                                #pass
                                                                j3_a = 0
                                                                while (j3_a < len(gaps_list_s[j_0][j1][j2_a])):
                                                                    # refer left and right before adding
                                                                    if (gaps_list_s[j_0][k1][k2_a][k3_a][1] < gaps_list_s[j_0][j1][j2_a][j3_a][1]) == True:
                                                                        gaps_list_s[j_0][j1][j2_a].insert(j3_a, gaps_list_s[j_0][k1][k2_a][k3_a])
                                                                        break #
                                                                    elif (gaps_list_s[j_0][k1][k2_a][k3_a][1] > gaps_list_s[j_0][j1][j2_a][j3_a][1]) == True:
                                                                        if (j3_a + 1) < len(gaps_list_s[j_0][j1][j2_a]) == True:
                                                                            if (gaps_list_s[j_0][k1][k2_a][k3_a][1] < gaps_list_s[j_0][j1][j2_a][j3_a + 1][1]) == True:
                                                                                gaps_list_s[j_0][j1][j2_a].insert(j3_a + 1, gaps_list_s[j_0][k1][k2_a][k3_a])
                                                                                break
                                                                            else:
                                                                                pass
                                                                        else:
                                                                            gaps_list_s[j_0][j1][j2_a].insert(j3_a + 1, gaps_list_s[j_0][k1][k2_a][k3_a])
                                                                            break
                                                                    j3_a = j3_a + 1
                                                            j2_a = j2_a + 1
                                                        k3_a = k3_a + 1
                                                    k2_a = k2_a + 1
                                                # add the remaining pixels in nested list of k1 directly to j1
                                                while (k2_a < len(gaps_list_s[j_0][k1])):
                                                    gaps_list_s[j_0][j1].append(gaps_list_s[j_0][k1][k2_a])                                            
                                                    k2_a = k2_a + 1
                                                flag2 = 1
                                                del gaps_list_s[j_0][k1]
                                                break #pass # add from here
                                            elif (gaps_list_s[j_0][k1][k2][k3][0] > gaps_list_s[j_0][j1][j2][j3][0] + 1) == True:
                                                flag1 = 2
                                                break # MIGHT HAVE TO CHANGE
                                        k3 = k3 + 1
                                    if flag1 == 2:
                                        flag1 = 0
                                        #break
                                    elif flag1 == 1:
                                        break
                                    k2 = k2 + 1
                                if flag1 == 1:
                                    pass
                                else:
                                    k1 = k1 + 1
                            j3 = j3 + 1
                        j2 = j2 - 1
                        
                    j1 = j1 + 1
            j_0 = j_0 + 1"""
        
        if i1 == 6:
            """for j1 in range(len(gaps_list_s)):
                for j2 in range(len(gaps_list_s[j1])):
                    print(str(j1) + ' len ' + str(j2) + ': ' + str(len(gaps_list_s[j1][j2])) + ' ' + str(gaps_list_s[j1][j2][0]) + ' ' + str(gaps_list_s[j1][j2][1]))
            print('min, max: ', x_min_1_2_list[i1], x_max_1_2_list[i1], y_min_1_2_list[i1], y_max_1_2_list[i1])"""
            for j1 in gaps_list_s:
                temp1 = random.randint(180,255)
                temp2 = random.randint(180,255)
                temp3 = random.randint(180,255)
                for j2 in j1:
                    for j3 in range(1, len(j2)):
                        for k1 in j2[j3]:
                            imarray0[k1[0]][k1[1]][0] = temp1
                            imarray0[k1[0]][k1[1]][1] = temp2
                            imarray0[k1[0]][k1[1]][2] = temp3
    
    i1 = i1 + 1
        
#for i1 in final_1_2_concatanate:
#    print(i1)
            
# add final_dataset values to image0
for i1 in final_1_2_concatanate:
    for i2 in i1:
        for i3 in i2:
            imarray0[i3[0]][i3[1]][0] = 0
            imarray0[i3[0]][i3[1]][1] = 255
            imarray0[i3[0]][i3[1]][2] = 255
            
print('acinar from dataset: ', len(final_1_2_concatanate))

#viewer = skimage.viewer.ImageViewer(imarray0) # np.array(imarray0)
#viewer.show()

data = Image.fromarray(imarray0)
data.save(image_o_name + '_acinar_c1_0' '.' + image_exten)