import sys
import re
import string
base = "{0},{1}, {2},{3}, {4}\n"
baseopt1 = "{0},{1}, {2},{3}, {4}, {5}\n"
baseopt2 = "{0},{1}, {2},{3}, {4}, {5}, {6}\n"


def main():
	if len(sys.argv) != 3:
		sys.exit("Usage: SplitAnim.py input_file output_file")

	input = sys.argv[1]
	output = sys.argv[2]
	clsn_data = ""
	clear_clsn1 = "Clsn1Default: 1\n  Clsn1[0] = 0, 0, 0, 0\n"
	is_reading_clsn = False
	had_clsn1 = False
	prev_had_clsn1 = False

	def split(s, n):
		return (s.split() + [None] * n)[:n]
		
	with open(input,"r") as f:
		with open(output,"w") as f1:
			for line in f:
				if line[0].isdigit() == False and line[0] != '-':
					# Not CLSN data, so it's begin action, comment, or loopstart.
					if line[0] in ('[', ';', 'l', 'L', '\n', '\r'):
						f1.write(line)
					# CLSN data
					else:
						if is_reading_clsn == False:
							clsn_data = ""
							is_reading_clsn = True
						# Convert to lowercase and strip whitespace from the left for easy parsing.
						linelower = line.lower().lstrip()
						# Convert CLSN to CLSNDefault
						if linelower.startswith("clsn1:"):
							linelower = linelower.replace("clsn1","Clsn1Default")
							clsn_data += linelower
							had_clsn1 = True
						elif linelower.startswith("clsn2:"):
							linelower = linelower.replace("clsn2","Clsn2Default")
							clsn_data += linelower
						else:
							clsn_data += line
				else:
					# Write the CLSN data as CLSNDefault
					if is_reading_clsn:
						is_reading_clsn = False
						f1.write(clsn_data)
					# If the previous frame had CLSN1, and this has none, clear it
					if prev_had_clsn1 == True and had_clsn1 == False:
						prev_had_clsn1 = False
						f1.write(clear_clsn1)
					# Previous frame had CLSN1
					if had_clsn1:
						prev_had_clsn1 = True
						had_clsn1 = False
					# Split up the animation elements and write them
					elements = line.split(",")
					length = len(elements)
					if length == 7:
						i,g,x,y,t,f,a = elements
					elif length == 6:
						i,g,x,y,t,f = elements
					else:
						i,g,x,y,t = elements
					if int(t) > 0:
						for k in range(int(t)):
							if length == 7:
								format = baseopt2.format(i,g,x,y,"1",f.strip(),a.strip())
							elif length == 6:
								format = baseopt1.format(i,g,x,y,"1",f.strip())
							else:
								format = base.format(i,g,x,y,"1")
							f1.write(format)
					else:
						f1.write(line)

if __name__ == "__main__":
	main()