# Region parsing for MUGEN
# bv Jesuszilla
# http://www.trinitymugen.net
import os
import re

# Enter your system subdirectory here. This is where replacement files will come from.
subdirectory = "cvscommon"

regionSearch = re.compile("(?<=;#region).*?(?=;#endregion)", re.DOTALL)
firstRegion = re.compile("(.*\n)?")

# Go over every goddamn file in the directory.
for filename in os.listdir(os.getcwd()):
    # Exclude this file or things will fuck up. Also exclude SFF's
    if filename != os.path.basename(__file__) and not filename.lower().endswith(".sff"):
        try:
            # "with" keyword ftw, it's like "using" in C#!
            with open(filename, "r+") as file:
                # I don't give a shit about the size, it shouldn't be anything major.
                # If it is, that's your own goddamn fault.
                contents = file.read()
                result = regionSearch.findall(contents)

                if result:
                    for region in result:
                        # Now split the first element to get the filename to replace the contents with
                        with open(subdirectory + "/" + firstRegion.search(region).group().strip(), "r") as regionFile:
                            replacement = " " + regionFile.name + "\n" + regionFile.read() + "\n"
                            contents = contents.replace(region, replacement)
                            print str.format("Replaced region {0}\n", regionFile.name)

                    file.seek(0)
                    file.write(contents)
                    file.truncate()

                    print str.format("Done writing {0}!\n", filename)
        # Fuck 'em
        except:
            continue