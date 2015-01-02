from __future__ import print_function
import os
import glob
import argparse
import shutil
from zipfile import ZipFile


maps = {
    'itead': {
        'Top.gbr': '.gtl',
        'Bottom.gbr': '.gtb',
        'TopMask.gbr': '.gts',
        'BottomMask.gbr': '.gbs',
        'TopSilk.gbr': '.gto',
        'BottomSilk.gbr': '.gbo',
        'BoardOutline.gbr': '.do',
        'Through.drl': '.txt',
    },
    'osh': {
        'Top.gbr': '.gtl',
        'Bottom.gbr': '.gtb',
        'TopMask.gbr': '.gts',
        'BottomMask.gbr': '.gbs',
        'TopSilk.gbr': '.gto',
        'BottomSilk.gbr': '.gbo',
        'BoardOutline.gbr': '.gko',
        'Through.drl': '.xln',
    }
}


def parse_args():

    parser = argparse.ArgumentParser(description="""Utility to rename and zip diptrace files \
                                                    for different pcb board houses""")

    parser.add_argument('boardname',
                        default='pcb',
                        help='Name of the board or project')

    parser.add_argument('mfr', choices=['osh', 'itead'],
                        default='itead',
                        help='Select the manufacturer of the board')

    parser.add_argument('--delete', '-d',
                        action='store_true',
                        help='Delete converted file after added to the zip file')

    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='Prints out status and warnings')

    return parser.parse_args()


def main():

    opts = parse_args()
    diptrace_exts = ('*.gbr', '*.drl')
    current_path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(current_path)
    diptrace_files = []

    for exts in diptrace_exts:
        diptrace_files.extend(glob.glob(exts))

    try:
        if opts.verbose:
            print("Creating archive {}.zip ...".format(opts.boardname))
        with ZipFile('{}.zip'.format(opts.boardname), 'w') as myzip:
            for key in maps[opts.mfr]:
                if key not in diptrace_files:
                    if opts.verbose:
                        print(u"******* Warning *******!")
                        print(u" Missing Gerber File: {} required by manufacturer".format(key))
                else:
                    new_file_name = "{}{}".format(opts.boardname, maps[opts.mfr][key])
                    shutil.copy2(key, new_file_name)
                    if opts.verbose:
                        print('file added to archive - {}'.format(new_file_name))
                    myzip.write(new_file_name)
                    if opts.delete:
                        os.remove(new_file_name)
    except Exception as e:
        print("ERROR! An exception has occurred.")
        print(e.__doc__)


if __name__ == "__main__":
    main()