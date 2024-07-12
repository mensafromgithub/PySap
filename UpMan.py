import argparse


from os import listdir, remove, path
from os.path import isfile
from requests import get
from shutil import rmtree, move
from zipfile import ZipFile


parser = argparse.ArgumentParser(prog='UpMan')
parser.add_argument('-v', '--version', default='v0.0.0.0')
parser.add_argument('-i', '--ignore', nargs='*', default='')
parser.add_argument('-c', '--clear', default='False', choices=['True', 'False'])

args = parser.parse_args()
ignore_const = {'boards', 'saves', 'UpMan.py'}
files_dirs = set(listdir())
if args.clear == 'True':
    rmtree('boards')
    rmtree('saves')
    ignore_const = {'UpMan.py'}
files_dirs -= (ignore_const | set(args.ignore))
for i in list(files_dirs):
    if isfile(i):
        remove(i)
    else:
        rmtree(i)
resp = get(f'https://github.com/mensafromgithub/PySap/archive/refs/tags/{args.version}.zip')
if resp.status_code != 200:
    print('Unkown version')
else:
    with open('update.zip', 'wb') as f:
        f.write(resp.content)
    with ZipFile('update.zip', 'r') as f:
        directory = f.namelist()[0]
        f.extractall()
    allfiles = list(set(listdir(directory)) - (ignore_const | set(args.ignore)))
    for i in allfiles:
        move(directory + '/' + i, './' + i)
    rmtree(directory)
    remove('update.zip')
