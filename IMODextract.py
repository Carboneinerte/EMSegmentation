import os
import argparse
import pandas as pd
from pandas import DataFrame
import re
from collections import defaultdict
# import pprint as pp
# import seaborn as sns
# import numpy as np
# import sys
import subprocess

# TODO change name of output files : remove .mod + add .csv or .txt

parser = argparse.ArgumentParser(
    prog='IMODextract',
    description='What the program can do:',
    epilog='MAKE SURE YOUR FILE OBTAINED WITH IMODINFO CONTAINS **ONLY** THE OBJECTS AND INFO YOU WANT TO EXTRACT')

parser.add_argument('-c', '--command', action='store', choices=['l', 'v', 'su', 'u', 'b', 'o', 'n', 'e', 'p'],
                    help='Choose between \'l\'ength, \'v\'olume, \'su\'rface, \'u\'nder, \'b\'etween, \'o\'ver, \'n\'ame and'
                         ' \'e\'xclude, \'p\'oint', required=True)
parser.add_argument('-s', '--selected_name', action='store', help='Name to extract or exclude, depending on c arg. Not'
                                                                  ' case sensitive, can be partial name')
parser.add_argument('-t', '--threshold', action='store', default='5', help='set the minimum number of layers for '
                                                                           'extraction of object number \'o\'ver')
parser.add_argument('-i', '--interval', action='store', nargs='+', type=int, help='Interval of the number of layers to'
                                                                                  ' extract')
parser.add_argument('-f', '--file_path', action='store', default=os.getcwd(), help='Write full path to the folder '
                                                                                   'containing the file to extract from'
                    )

parser.add_argument('-n', '--input_file', action='store',
                    help='Input mod file', required=True
                    )

parser.add_argument('-o', '--output_file', action='store', default='imodinfo_output.txt',
                    help='Output filename which stores imodinfo results'
                    )

# TODO: add help for the imodinfo command to use depending on the command used
# TODO: command volume : add possibility of small volume (without e+)
# TODO: make -t as subargparse of -c o
# TODO: extract number of points
# TODO: extract number of contours
# TODO: IMODINFO command depending on input


args = parser.parse_args()

# print('args')
# print(args)

# imodinfo -F -f test_out CompImBio_5k_all_layers_aug1_predictions_h192_meshed_sort.mod

# base_dir = 'D:\_IMOD\SCN-PSAPP\ground truth'
# base_dir = os.getcwd()
base_dir = args.file_path
os.chdir(base_dir)


# print(os.getcwd())


# make txt file using imodinfo prompt, "test_out"
# Run imodinfo with full report

def imodinfo(arglist):
    process = subprocess.run(arglist,
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
    lines = process.stdout.split('\n')
    f = open(args.output_file, "w")
    f.write(process.stdout)
    f.close()
    return lines


if args.command == 'l':
    lines = imodinfo(['imodinfo', '-L -h', args.input_file])
elif args.command == 'p':
    lines = imodinfo(['imodinfo', args.input_file])
elif args.command == 'n':
    lines = imodinfo(['imodinfo', args.input_file])
elif args.command == 'su':
    lines = imodinfo(['imodinfo', args.input_file])
else:
    lines = imodinfo(['imodinfo', '-F', args.input_file])


#objects_file = args.input_file
#with open(objects_file, 'r') as f:
#    lines = [line.rstrip() for line in f]
#    lines = process.stdout.split('\n')

def over():
    objects = {}
    if (lines[13].split(' #')[0] == 'Object') & (lines[25].split(' ')[1] == 'Box'):

        for i in range(len(lines)):
            if 'Object # ' in lines[i]:
                object_num = lines[i]
                object_name = lines[i + 1]
                num_contours = float(lines[i + 3].split('=')[-1])
                bbox = lines[i + 12]
                corner1 = bbox[bbox.find("(") + 1:bbox.find(")")]
                first_layer = float(corner1.split(',')[-1])
                bbox_2 = bbox[bbox.find(")") + 1:]
                corner2 = bbox_2[bbox_2.find("(") + 1:bbox_2.find(")")]
                last_layer = float(corner2.split(',')[-1])
                num_layers = last_layer - first_layer + 1
                objects[object_num] = [object_name, num_contours, num_layers]
        df = DataFrame.from_dict(objects, orient='index', columns=['Name', 'Num Contours', 'Num Layers'])
        df.to_csv('list_obj.csv', index=True)
        print(df.describe())
        print()

        if args.command == 'o':
            min_num_layers = int(args.threshold)
            objects_above_min = list(df[df['Num Contours'] >= min_num_layers].index)
            print('Objects above', min_num_layers, 'contours =', len(objects_above_min))
            print()
            objects_above_min_strs = ','.join([x.split('# ')[-1][:-1] for x in objects_above_min])
            content = str(objects_above_min_strs)
            file = open("objects_above.txt", "w+")
            file.write(content)
            file.close()
        elif args.command == 'b':
            max_num_layers = args.interval[1]
            min_num_layers = args.interval[0]
            objects_between = list(df[df['Num Layers'].between(min_num_layers, max_num_layers)].index)
            objects_between_strs = ','.join([x.split('# ')[-1][:-1] for x in objects_between])
            print('Objects between', min_num_layers, 'and', max_num_layers, 'layers =', len(objects_between))
            print()
            content = str(objects_between_strs)
            file = open("objects_between.txt", "w+")
            file.write(content)
            file.close()
        elif args.command == 'u':
            min_num_layers = int(args.threshold)
            objects_below_min = list(df[df['Num Layers'] <= min_num_layers].index)
            print('Objects below', min_num_layers, 'layers =', len(objects_below_min))
            print()
            objects_below_min_strs = ','.join([x.split('# ')[-1][:-1] for x in objects_below_min])
            content = str(objects_below_min_strs)
            file = open("objects_below.txt", "w+")
            file.write(content)
            file.close()
        else:
            print('How did you even get here?')
    else:
        print('Possible wrong type of object in mod file?')


def length():
    print('Extraction of length')
    lines = imodinfo(['imodinfo', '-L', '-h', args.input_file])
    if (lines[14].split(' #')[0] == 'Object') & (re.split(', | =', lines[16])[1] == 'length total'):
        objects = {}
        for i in range(len(lines)):
            if 'Object # ' in lines[i]:
                Obj_num_name = lines[i]
                Obj_num_name2 = Obj_num_name.split(':  ')
                object_num = Obj_num_name2[0]
                object_name = Obj_num_name2[1]
                leng = lines[i + 2]
                leng2 = float(re.split(', | =', leng)[2])
                leng_f = leng2 / 1000
                objects[object_num] = [object_name, leng_f]
        df = DataFrame.from_dict(objects, orient='index', columns=['Name', 'Length um'])
        df.to_csv('length.csv', index=True)
        print(df.describe())
        print()
    else:
        print('Possible wrong type of object in mod file?')


def point():
    print('Extraction of nb point/contour')
    if (lines[13].split(' ')[0] == 'OBJECT') & (lines[16].split(' ')[-2] == 'scattered'):
        objects = {}
        for i in range(len(lines)):
            if 'OBJECT' in lines[i]:
                object_num = lines[i].split(' ')[1]
                Obj_name = lines[i + 1].split(':  ')[1]
                point = lines[i + 6].split(' ')[-5]
                objects[object_num] = [Obj_name, point]
        df = DataFrame.from_dict(objects, orient='index', columns=['Name', 'Points'])
        df.to_csv('point.csv', index=True)
        # print(df.describe())
        print()
    else:
        print('Possible wrong type of object in mod file?')


def volume():
    print('Extraction of Volume')
    if (lines[13].split(' #')[0] == 'Object') & (lines[28].split(' ')[2] == 'Mesh'):
        objects = {}
        for i in range(len(lines)):
            if 'Object # ' in lines[i]:
                object_num = lines[i]
                object_name = lines[i + 1]
                vol = lines[i + 15]
                # print('vol', vol)
                vol2 = vol.split('=')[-1]
                # print('vol2', vol2)
                vol_mesh_e = vol2.split(' ')[1]
                # print('vol_mesh_e', vol_mesh_e)
                # vol_mesh = float(vol_mesh_e.split('e+')[0]) * (10 ** (int(vol_mesh_e.split('e+')[1]) - 9))
                vol_mesh = float(vol_mesh_e)
                # print('vol_mesh', vol_mesh)
                objects[object_num] = [object_name, vol_mesh]
        df = DataFrame.from_dict(objects, orient='index',
                                 columns=['Name', 'Volume Mesh um3'])
        volume_name = f"{args.input_file}{'_volume'}{'.csv'}"
        df.to_csv(volume_name, index=True)
        print(df.describe())
        print()
    else:
        print('Possible wrong type of object in mod file?')

def surface():
    print('surface')
    objects_info = {}
    current_object_name = None
    current_contour_sum = 0

    for line in lines:
        # Identify the object name
        if line.startswith('NAME:'):
            if current_object_name:
                # Save the sum for the previous object
                objects_info[current_object_name] = current_contour_sum

            # Start a new object
            current_object_name = line.split(': ')[1].strip().strip("'")
            current_contour_sum = 0

        # Calculate the sum of values in contour lines
        if line.startswith('\tCONTOUR'):
            parts = line.split(',')
            # Extract the value from the "area = " part
            for part in parts:
                if 'area =' in part:
                    area_value = float(part.split('=')[1].strip())
                    current_contour_sum += area_value

    # Save the sum for the last object
    if current_object_name:
        objects_info[current_object_name] = current_contour_sum

    df = pd.DataFrame(list(objects_info.items()), columns=['Object Name', 'Total Area'])

    surface_name = f"{args.input_file}{'_surface'}{'.csv'}"
    df.to_csv(surface_name, index=False)

def name():
    if (lines[13].split(' ')[0] == 'OBJECT') & (lines[15].split(' ')[-1] == 'contours'):
        selected_name = args.selected_name
        named_objects = defaultdict(list)
        objects = {}

        for i in range(len(lines)):
            if 'OBJECT ' in lines[i] and 'NAME:' in lines[i + 1]:
                object_numb = lines[i]
                object_number = lines[i].split(' ')[-1]
                name = lines[i + 1][7:]
                named_objects[name].append(object_number)
                objects[object_numb] = [object_number, name]
        df = DataFrame.from_dict(objects, orient='index', columns=['object_number', 'name'])

        if args.command == 'n':
            list_name = list(df[df['name'].str.contains(selected_name, case=False)].index)
            print('Objects named', selected_name, '=', len(list_name))
            print()
            list_name_strs = ','.join([x.split(' ')[-1][:] for x in list_name])
            content = str(list_name_strs)
            file = open("object_list_name.txt", "w+")
            file.write(content)
            file.close()
        elif args.command == 'e':
            list_name = list(df[~df['name'].str.contains(selected_name, case=False)].index)
            print('Objects not named', selected_name, '=', len(list_name))
            print()
            list_name_strs = ','.join([x.split(' ')[-1][:] for x in list_name])
            content = str(list_name_strs)
            file = open("object_list_name_excluded.txt", "w+")
            file.write(content)
            file.close()
        else:
            print('How did you even get here?')
    else:
        print('Possible wrong type of object in mod file?')


commands = {
    'o': over,
    'b': over,
    'u': over,
    'p': point,
    'l': length,
    'v': volume,
    'n': name,
    'e': name,
    'su': surface
}

func = commands.get(args.command)
if func:
    func()
else:
    print('WRONG ARGUMENT, try again or check the help (-h)')

# if __name__ == "__main__":
#   main()
