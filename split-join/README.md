# **SPLIT/JOIN files**

Above named scripts are used to split, and then join big files in chunks.
#### *split.py* 
##### Usage: python split.py \[PATH-TO-FILE\] \[RESULT-FOLDER\] \[CHUNK-SIZE\]
  - **PATH-TO-FILE** - path to the file to be split
  - **RESULT-FOLDER** - folder name/path where the chunks will be saved (created the folder if it doesn't already exist)
    ***Warning: if an existing folder provided, the script will delete all the files already contained there***
  - **CHUNK-SIZE** - Size of the information chunk in bytes (ex 1024 for 1Kb etc.).
    If skipped, files will be split in chunks of 1 MB.
###### All the arguments are optional, if none provided, the user will get prompted to input the values interactively.
###### The script creates an metadata textfile containing some information about the operation as:
1. Original file checksum (will be checked on joining to assure file integrity)
2. Number of chunks created.
3. The length of the file name created (Depends on the number of chunks created)
