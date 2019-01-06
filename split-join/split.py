#! /usr/bin/env python3

"""
Split file binaries in chunks
"""

import sys, os
from hashlib import sha256

def split(filepath, splitpath, chunksize):
    if not os.path.exists(splitpath):
        os.makedirs(splitpath)
    else:
        # Delete all files in the directory
        for filename in os.listdir(splitpath):
            fullname = os.path.join(splitpath, filename)
            os.remove(fullname)
    
    checksum = sha256()
    counter = 0
    filelength = len(str(os.path.getsize(filepath) // chunksize)) + 4
    filepattern = '%0' + str(filelength) + 'd'

    target_f = open(filepath, 'rb')
    meta_f = open(os.path.join(splitpath, 'meta'), 'w')

    while True:
        chunk = target_f.read(chunksize)
        if not len(chunk): break
        counter += 1
        checksum.update(chunk)
        with open('%s' % os.path.join(splitpath, filepattern % counter), 'wb') as f:
            f.write(chunk)

    target_f.close()
    #write metadata
    meta_f.write(checksum.hexdigest() + '\n')   # 
    meta_f.write('%s\n' % counter)
    meta_f.write('%s\n' % filelength)
    return counter
        

if __name__ == "__main__":
    multiplier = 1024
    chunksize = multiplier ** 2 # default chunk in bytes (1 megabyte)

    # User requests help info
    if any([x in sys.argv for x in ['help', '-help', '--help', '-h', '--h']]):
        print('Usage: split [<Path to file> <Result folder path> [<Chunk size>]]')
        sys.exit(0)

    interactive = False
    if len(sys.argv) < 3:
        interactive = True # Ask user for filename to split and path to store the result
        filepath = input('Please provide the file to split: ')
        splitpath = input('Please provide the path to store the result files: ')
        _chunksize = input('Please provide the chunk size (leave blank for default): ')
        if len(_chunksize) != 0:
            chunksize = int(_chunksize)
    else:
        filepath = sys.argv[1]
        splitpath = sys.argv[2]
        if len(sys.argv) >= 4: chunksize = int(sys.argv[3])
    if not os.path.exists(filepath) or \
       not os.path.isfile(filepath):
        print("Invalid or inexistent file => %s\nPlease check." % filepath)
        sys.exit(1)
    print("Start splitting %s by %s bytes...\n...\n..." % (filepath, chunksize))
    try:
        r = split(filepath, splitpath, chunksize)
    except:
        print('Error durring split')
        print(sys.exc_info()[0], sys.exc_info()[1])
    else:
        print('Split finished with %s parts.' % r)
    if interactive: input('Press <Enter> to finish')

    

