#! /usr/bin/env python3

"""
Joins a file from pieces created by split.py
"""

import os, sys
from hashlib import sha256

def join(piecespath, filename, resultpath=os.getcwd()):
    if not os.path.exists(piecespath):
        raise FileNotFoundError('Folder %s not found.' % piecespath)
    if not os.path.exists(resultpath):
        os.makedirs(resultpath)
    checksum_check = False
    result = 0
    try:
        meta = open(os.path.join(piecespath, 'meta'), 'r')
        checksum = meta.readline()[:-1]
        num_files = int(meta.readline()[:-1])
        len_file = int(meta.readline()[:-1])
    except FileNotFoundError:
        result = 1 # warn user
        list_files = os.listdir(piecespath)              # Get a list of files to identify
        num_files = len(list_files)                      # their file name length and count
        len_file = len(os.path.basename(list_files[0]))
    else:
        checksum_check = True
        checksum_finnal = sha256()

    result_file_path = os.path.join(resultpath, filename)
    result_file = open(result_file_path, 'wb')

    for i in range(num_files):
        namepattern = '%0' + str(len_file) + 'd'
        try:
            with open(os.path.join(piecespath, namepattern % (i+1)), 'rb') as f:
                data = f.read()
                result_file.write(data)
                if checksum_check: checksum_finnal.update(data)
        except FileNotFoundError:
            result_file.close()
            os.remove(result_file_path)
            raise FileNotFoundError('Some files were deleted from the folder. Operation not possible.')
    
    # Check file integrity
    if checksum_check:
        checksum_finnal = checksum_finnal.hexdigest()
        if checksum != checksum_finnal:
            raise Exception('File was corrupted.')

    result_file.close()
    return result

if __name__ == "__main__":

    if any([x in sys.argv for x in ['help', '-help', '--help', '-h', '--h']]):
        print('Usage: python fjoin.py [<Path to split files> <Result file name> [<Result folder>]]')
        sys.exit(0)

    interactive = False
    if len(sys.argv) < 3:
        interactive = True
        piecespath = input('Please provide the path to folder, containing the split files: ')
        filename = input('Please input the result filename (with extension): ')
        resultpath = input('Please input the path where result file should be saved (leave blank for current folder): ')
        if not len(resultpath): resultpath = os.getcwd()
    else:
        piecespath = sys.argv[1]
        filename = sys.argv[2]
        if len(sys.argv) >= 4: 
            resultpath = sys.argv[3]
        else: resultpath = os.getcwd()

    print('Start joining the file in %s\n...\n...' % os.path.abspath(piecespath))
    try:
        r = join(piecespath, filename, resultpath)
    except:
        print('Error durring join operation')
        print(sys.exc_info()[0], sys.exc_info()[1])
    else:
        if r == 0:
            print('Successful join.')
        elif r == 1:
            print('Warning: meta file was deleted from the folder\nInformation might get corrupted.')
        else:
            print('Some errors occured while joining.\nFile was joined, but might be unreadable.')
        if interactive: input('Press Enter to exit') # if interactive. ex. by clicking the file