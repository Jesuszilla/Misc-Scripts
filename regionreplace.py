#!/usr/bin/python3
# Region parsing for MUGEN
# bv Jesuszilla
# http://www.trinitymugen.net
import io, os, re

# Enter relative (or absolute, if you wish) directory path here. This is where files
# to replace will be.
directories = ['../']

# Enter your system subdirectories here. This is where replacement files will come from.
subdirectories = ['cvscommon', 'overrides']

# Enter your post-update copy files here. These files will be copied completely from the
# subdirectory into the specified directory before all replacements have occurred, meaning
# that replacement operations will still occur on them.
preCopyFiles = {
    'cvscommon/config.txt': '../'
}

# Enter your post-update copy files here. These files will be copied completely from the
# subdirectory into the specified directory with no replacement operations occurring on
# them.
postCopyFiles = {
    'cvscommon/cvssystem.lol': '../',
    'cvscommon/point.lol': '../'
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

BOM_UTF8 = bytearray('\ufeff', 'utf8')

# Parse the damn regions. This will be recursive.
def parseRegion(filename, excludeList):
    newList = [i for i in excludeList]
    newList.append(filename)

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
                        shouldBreak = False
                        for directory in directories:
                            for subdirectory in subdirectories:
                                try:
                                    innerPath = os.path.join(directory, subdirectory, firstRegion.search(line).group().strip())
                                    replacement = parseRegion(innerPath, newList)
                                    if len(replacement) > 0:
                                        while replacement.startswith(BOM_UTF8):
                                            replacement = replacement.removeprefix(BOM_UTF8)
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
basePreCopyFiles = [os.path.basename(f) for f in preCopyFiles if os.path.splitext(f)[1].lower() not in fileExemptions]
basePostCopyFiles = [os.path.basename(f) for f in postCopyFiles if os.path.splitext(f)[1].lower() not in fileExemptions]
# Go over each directory
for directory in directories:
    # Go over every goddamn file in the directory.
    for filename in os.listdir(directory):
        # Copy the entire file if it's in copyFiles.
        strippedFilename = filename.strip()
        if strippedFilename in basePostCopyFiles:
            print(strippedFilename)
            for copyFile in postCopyFiles:
                if strippedFilename in copyFile:
                    with io.open(os.path.join(postCopyFiles[copyFile], strippedFilename), 'w+', encoding='utf8') as file:
                        with io.open(os.path.join(postCopyFiles[copyFile], copyFile), 'r', encoding='utf8') as copy:
                            file.seek(0)
                            file.write(copy.read())
                            file.truncate()
                            print('Overwrote {}\n'.format(os.path.basename(file.name)))
                    break
        elif strippedFilename in basePreCopyFiles:
            print(strippedFilename)
            for copyFile in preCopyFiles:
                if strippedFilename in copyFile:
                    newContents = parseRegion(os.path.join(preCopyFiles[copyFile], copyFile), [])
                    debugStr = str(newContents, encoding='utf8')
                    if newContents:
                        with io.open(os.path.join(preCopyFiles[copyFile], strippedFilename), 'w+', encoding='utf8') as file:
                            file.seek(0)
                            file.write(newContents.decode('utf-8'))
                            file.truncate()
                            print('Overwrote {}\n'.format(os.path.basename(file.name)))
                    break

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