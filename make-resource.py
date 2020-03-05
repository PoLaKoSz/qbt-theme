import subprocess
import glob
import argparse
import os.path
import sys
import fnmatch

parser = argparse.ArgumentParser(description='Tool to crate .qbttheme files for qBittorrent.')
parser.add_argument('-o', '--output', type=str, help='Name of the output .qbtheme file', default='style.qbtheme')
parser.add_argument('-s', '--style', type=str, help='stylesheet', required=True)
parser.add_argument('-e', '--exclude', type=str, default='*.qrc', help='files to ignore')
parser.add_argument('files', metavar='file', type=str,
                    nargs='*', help='files for icons, supports glob patterns')
args = parser.parse_args()

args.exclude = args.exclude.split(',')

def allFiles(glob):
    [dir, pattern] = os.path.split(glob)
    l = list()
    for root, subdir, files in os.walk(dir):
        l.extend([os.path.join(root, x) for x in files if fnmatch.fnmatch(x, pattern)])
    return l

if len(args.output) > 0 and not args.output.endswith('.qbtheme'):
    args.output += '.qbtheme'
if not len(args.output) or os.path.exists(args.output):
    if input('"{}" already exists. Do you want to overwrite? (y,n) '.format(args.output)) == 'n':
        exit()

#ResourceFiles = ['\t\t<file>' + x + '</file>\n' for  x in [z for z in [allFiles(y) for y in args.files]]]

ResourceFiles = list()
[ResourceFiles.extend(x) for x in [allFiles(y) for y in args.files]]
ResourceFiles = [os.path.relpath(x, './') for x in ResourceFiles for y in args.exclude if not fnmatch.fnmatch(os.path.split(x)[1], y)]

with open('resources.qrc', 'w') as rcc:
    rcc.write('<!DOCTYPE RCC><RCC version="1.0">\n')
    rcc.write('\t<qresource>\n')
    rcc.writelines(['\t\t<file>' + x + '</file>\n' for x in ResourceFiles])
    rcc.write('\t</qresource>\n')
    rcc.write('</RCC>')

subprocess.call(['rcc', '-binary', '-o', args.output, '--root', '/', 'resources.qrc'])
