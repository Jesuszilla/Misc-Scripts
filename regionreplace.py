#!/usr/bin/python3
# Region parsing for MUGEN
# bv Jesuszilla
# http://www.trinitymugen.net
from ast import List
import io
import os
import re

# Enter relative (or absolute, if you wish) directory path here. This is where files
# to replace will be.
directories = ['../']

# Enter your system subdirectories here. This is where replacement files will come from.
subdirectories = ['cvscommon', 'overrides']

# Enter your files to copy completely from the subdirectory here and their directory to copy to.
copyFiles = {
    'cvscommon/cvssystem.lol': '../',
}

# Region searches
firstRegion = re.compile('\s*(?<=;#region).*')
tagStart = re.compile('\s*;#region\s*')
tagEnd = re.compile('\s*;#endregion')

# Files to exempt. Do not fuck with this unless you know what you're doing. You have been warned.
fileExemptions = ['.sff', '.act', '.snd', '.7z', '.rar', '.lzh', '.dgc', '.zip', '.png', '.gif', '.jpg', '.jpeg', '.pcx', '.bat',
                  '.bin', '.sh', '.gitmodules', '.gitignore', '.py', '.exe', '.pl', '.perl', '.java', '.jar', '.pyc', '.c', '.cpp',
                   '.cs', '.c++', '.wav', '.mp3', '.ogg', '.h', '.hpp', '.m', '.tar', '.gz', '.afs', '.pak', '.webm', '.a', '.mp4',
                   '.avi', '.mpg', '.mpeg', '.psd']

# Folders to exempt. It's best not to fuck with this, either.
folderExemptions = ['.git']

# Don't fuck with this
textChars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
isBinaryString = lambda bytes: bool(bytes.translate(None, textChars))

# Parse the damn regions. This will be recursive.
def parseRegion(filename, excludeList):
    # We're gonna be doing a LOT of appending.
    # Start keeping track of the region
    regionDepth = 0
    
    # Check to see if the file's not already being read
    if filename not in excludeList:
        # 'with' keyword ftw, it's like 'using' in C#!
        with io.open(filename, 'r', encoding='utf8') as file:
            # Keep track of the current depth
            file.seek(0)
            newContents = bytearray('', encoding='utf8')
            for line in file.readlines():
                # Start recording the region
                if tagStart.match(line):
                    regionDepth += 1
                    if regionDepth == 1:
                        newContents.extend(bytearray(line, 'utf8'))
                        excludeList.append(filename)
                    shouldBreak = False
                    for directory in directories:
                        for subdirectory in subdirectories:
                            try:
                                replacement = parseRegion(os.path.join(directory, subdirectory, firstRegion.search(line).group().strip()), excludeList)
                                if len(replacement) > 0:
                                    newContents.extend(replacement)
                                    newContents.extend(bytearray('\n', 'utf8'))
                                    shouldBreak = True
                                    break
                            except Exception as e:
                                continue
                        if shouldBreak:
                            break
                # If we're down a few levels, don't record because we're reading from a file.
                elif regionDepth > 0:
                    if tagEnd.match(line):
                        regionDepth -= 1
                        if regionDepth == 0:
                            newContents.extend(bytearray(line, 'utf8'))
                elif regionDepth == 0:
                    newContents.extend(bytearray(line, 'utf8'))
            return newContents
    return bytearray()

# Get the basepaths for easier searching
baseCopyFiles = [os.path.basename(f) for f in copyFiles if os.path.splitext(f)[1].lower() not in fileExemptions]
print('AAAAAAAAAAGH: {}'.format(str(baseCopyFiles)))
# Go over each directory
for directory in directories:
    # Go over every goddamn file in the directory.
    for filename in os.listdir(directory):
        # Copy the entire file if it's in copyFiles.
        strippedFilename = filename.strip()
        if strippedFilename in baseCopyFiles:
            print(strippedFilename)
            for copyFile in copyFiles:
                if strippedFilename in copyFile:
                    with io.open(copyFiles[copyFile] + strippedFilename, 'w+', encoding='utf8') as file:
                        with io.open(copyFiles[copyFile] + copyFile, 'r', encoding='utf8') as copy:
                            file.seek(0)
                            file.write(copy.read())
                            file.truncate()
                            print('Overwrote {}\n'.format(os.path.basename(file.name)))
        elif filename != os.path.basename(__file__) and os.path.splitext(filename)[1].lower() not in fileExemptions and \
        filename not in fileExemptions and filename not in folderExemptions and not os.path.isdir(os.path.join(directory, filename)):
            try:
                newContents = parseRegion(os.path.join(directory, filename), [])
                if newContents:
                    with io.open(os.path.join(directory, filename), 'w', encoding='utf8') as file:
                        file.write(newContents.decode('utf-8'))
                        file.truncate()
                        print('Done writing {0}!\n'.format(filename))
            # Fuck 'em
            except Exception as e:
                print('Error with {}: {}'.format(filename, str(e)))
                continue