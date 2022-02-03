# Capcom vs. SNK 2 palette converter
# by Jesuszilla
# Huge thanks goes to aokmaniac13 for telling me the palette structure!
import argparse
from struct import unpack
import array
from os import SEEK_END

# Argument parser
parser = argparse.ArgumentParser(description='Enter the filename')
parser.add_argument('filename', type=str, nargs=1, help="Name of the file from which to rip palettes")

# Constants
END_OFFSET = 0x600
MASK_B = 0x001F
MASK_G = 0x03E0
MASK_R = 0x7C00
MASK_A = 0x8000
COLOR_COUNT = 96

def main():
    # Parse the argument vector.
    argv = parser.parse_args().filename
    filename = argv[0]

    # Open the PLPAK
    with open(filename, "rb") as pak:
        # Palettes are always at the "ass end" of the file, specifically, end-0x600.
        pak.seek(-END_OFFSET, SEEK_END)

        # Need to terminate out of this next loop somehow.
        loop = True
        actList = [4,5,6,1,2,3,10,7] # LP, MP, HP, LK, MK, HK, 3P, 3K

        # Loop until we reach the end of the file
        for actNo in actList:
            # Palette: the entire color palette
            palette = []
            
            # 84 colors per palette.
            for x in range(0,COLOR_COUNT):
                # Read the color (2 bytes)
                currColor = pak.read(2)
                currColor = unpack("1H", currColor)[0]

                # Red component
                r = (currColor&MASK_R) >> 10
                palette.insert(0, (r << 3) | (r >> 2))
                # Green component
                g = (currColor&MASK_G) >> 5
                palette.insert(1, (g << 3) | (g >> 2))
                # Blue component
                b = currColor&MASK_B
                palette.insert(2, (b << 3) | (b >> 2))
                # Alpha component not necessary for our purposes

            # Fill in the rest with 0's
            for x in range(0,256-COLOR_COUNT):
                palette.insert(0,0)
                palette.insert(1,0)
                palette.insert(2,0)

            # Write the file
            with open(str.format("act{0:03}.act", actNo), "wb") as actFile:
                shit = bytearray(palette)
                actFile.write(shit)

        # We're done with the file, now close it.
        pak.close()

        print(palette)

if __name__ == "__main__":
    main()