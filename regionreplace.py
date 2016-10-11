#!/usr/bin/python
# Region parsing for MUGEN
# bv Jesuszilla
# http://www.trinitymugen.net
import os
import re

# Enter relative (or absolute, if you wish) directory path here. This is where files
# to replace will be.
directories = ["../"]

# Enter your system subdirectory here. This is where replacement files will come from.
subdirectory = "cvscommon"

# Enter your files to copy completely from the subdirectory here and their directory to copy to.
copyFiles = {
    "cvssystem.lol": "../",
}

regionSearch = re.compile("(?<=;#region).*?(?=;#endregion)", re.DOTALL)
firstRegion = re.compile("(.*\n)?")

# Go over each directory
for directory in directories:
    # Go over every goddamn file in the directory.
    for filename in os.listdir(directory):
        # Copy the entire file if it's in copyFiles
        if filename.strip() in copyFiles:
            with open(directory + "/" + filename, "w+") as file:
                with open(str.format("{0}/{1}/{2}", directory, subdirectory, filename), "r") as copyFile:
                    file.seek(0)
                    contents = copyFile.read()
                    file.write(contents)
                    file.truncate()
                    print "Overwrote " + os.path.basename(file.name) + "\n"

        # Exclude this file or things will fuck up. Also exclude SFF's
        elif filename != os.path.basename(__file__) and not filename.lower().endswith(".sff"):
            try:
                # "with" keyword ftw, it's like "using" in C#!
                with open(directory + "/" + filename, "r+") as file:
                    # I don't give a shit about the size, it shouldn't be anything major.
                    # If it is, that's your own goddamn fault.
                    contents = file.read()
                    result = regionSearch.findall(contents)

                    if result:
                        for region in result:
                            # Now split the first element to get the filename to replace the contents with.
                            with open(str.format("{0}/{1}/{2}", directory, subdirectory, firstRegion.search(region).group().strip(), "r")) as regionFile:
                                replacement = " " + os.path.basename(regionFile.name) + "\n" + regionFile.read() + "\n"
                                contents = contents.replace(region, replacement)
                                print str.format("Replaced region {0}\n", os.path.basename(regionFile.name))

                        file.seek(0)
                        file.write(contents)
                        file.truncate()

                        print str.format("Done writing {0}!\n", filename)

            # Fuck 'em
            except Exception as e:
                continue
