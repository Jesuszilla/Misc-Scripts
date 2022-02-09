import sys
base = "{0},{1}, {2},{3}, {4}\n"
baseopt1 = "{0},{1}, {2},{3}, {4}, {5}\n"
baseopt2 = "{0},{1}, {2},{3}, {4}, {5}, {6}\n"


def main():
	if len(sys.argv) != 3:
		sys.exit("Usage: CheckBoxWidths.py input_file output_file")

	input = sys.argv[1]
	output = sys.argv[2]

	def split(s, n):
		return (s.split() + [None] * n)[:n]
		
	with open(input,"r") as f:
		with open(output,"w") as f1:
			lineNo = 1
			for line in f:
				if line[0].isdigit() == False and line[0] != '-':
					# Not CLSN data, so it's begin action, comment, or loopstart.
					if line[0] not in ('[', ';', 'l', 'L', '\n', '\r'):
						# Convert to lowercase and strip whitespace from the left for easy parsing.
						linelower = line.lower().lstrip()
						# Convert CLSN to CLSNDefault
						if linelower.startswith("clsn1[") or linelower.startswith("clsn2["):
							l,t,r,b = [int(n) for n in linelower[linelower.index('=')+1:].lstrip().split(',')]
							w_x = r - l
							h_y = b - t
							
							# Width is not even
							linesToWrite = []
							if (w_x&1) != 0:
								linesToWrite.append(f"Problem at line {lineNo}: width is not even ({w_x} px)\r\n")
							if (h_y&1) != 0:
								linesToWrite.append(f"Problem at line {lineNo}: height is not even ({h_y} px)\r\n")
							if len(linesToWrite) > 0:
								f1.writelines(linesToWrite)
				lineNo = lineNo + 1


if __name__ == "__main__":
	main()