# Region parsing for MUGEN
# bv Jesuszilla
# http://www.trinitymugen.net
import os
import re

# Enter relative (or absolute, if you wish) directory path here. This is where files
# to replace will be.
directories = ["../"]

# Enter your system subdirectories here. This is where replacement files will come from.
subdirectories = ["cvscommon", "overrides"]

# Enter your files to copy completely from the subdirectory here and their directory to copy to.
copyFiles = {
    "cvscommon/cvssystem.lol": "../",
}

# Region searches
firstRegion = re.compile("\s*(?<=;#region).*")
tagStart = re.compile("\s*;#region\s*")
tagEnd = re.compile("\s*;#endregion")

# Files to exempt. Do not fuck with this unless you know what you're doing. You have been warned.
fileExemptions = ["sff", "act", "snd", "7z", "rar", "lzh", "dgc", "zip", "png", "gif", "jpg", "pcx", "bat", "bin", "sh"
                  "gitmodules", "py", "exe", "pl", "perl", "java", "jar", "pyc", "c", "cpp", "cs", "c++", "wav", "mp3",
                  "ogg", "h", "hpp", "m", "tar", "gz", "afs", "pak"]

# Don't fuck with this
textChars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
isBinaryString = lambda bytes: bool(bytes.translate(None, textChars))

# Parse the damn regions. This will be recursive.
def parseRegion(filename):
    # We're gonna be doing a LOT of appending.
    newContents = bytearray()
    # "with" keyword ftw, it's like "using" in C#!
    with open(filename, "rb") as file:
        # Keep track of the current depth
        regionDepth = 0
        file.seek(0)
        for line in file.readlines():
            # Start recording the region
            if regionDepth > 0:
                if tagEnd.match(line):
                    regionDepth -= 1
                    if regionDepth == 0:
                        newContents.extend([elem.encode("utf-8") for elem in line])
                elif tagStart.match(line):
                    regionDepth += 1
            elif tagStart.match(line):
                regionDepth += 1
                newContents.extend([elem.encode("utf-8") for elem in line])
                for subdirectory in subdirectories:
                    try:
                        newContents.extend(parseRegion(str.format("{0}/{1}/{2}", directory, subdirectory, firstRegion.search(line).group().strip())))
                    except:
                        continue
            else:
                newContents.extend([elem.encode("utf-8") for elem in line])
        return newContents + '\n'.encode("utf-8")

# Get the basepaths for easier searching
baseCopyFiles = [os.path.basename(f) for f in copyFiles]
# Go over each directory
for directory in directories:
    # Go over every goddamn file in the directory.
    for filename in os.listdir(directory):
        # Copy the entire file if it's in copyFiles.
        strippedFilename = filename.strip()
        if strippedFilename in baseCopyFiles:
            for copyFile in copyFiles:
                if strippedFilename in copyFile:
                    with open(copyFiles[copyFile] + "/" + strippedFilename, "w+") as file:
                        with open(copyFiles[copyFile] + "/" + copyFile, "r") as copy:
                            file.seek(0)
                            file.write(copy.read())
                            file.truncate(0)
                            print "Overwrote " + os.path.basename(file.name) + "\n"
        elif filename != os.path.basename(__file__):
            try:
                newContents = parseRegion(directory + "/" + filename)
                if newContents:
                    with open(str.format("{0}/{1}", directory, filename), "w") as file:
                        file.write(newContents)
                        print str.format("Done writing {0}!\n", filename)
            # Fuck 'em
            except Exception as e:
                print "Error with " + filename + ": " + e.message
                continue
