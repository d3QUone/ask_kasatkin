#
# Vladimir Kasatkin. April, 2015
#

from config import SOURCE_DIRS, TARGET_DIR, TARGET_FILES
from os import listdir, remove
import sys
import os

BASE_DIR = os.getcwd() + "/"
print "BASE_DIR: ", BASE_DIR

# 
# just put filename in tag insted of your include. This file will be searching in the same 
# folder with current "Target-File", example: 
# 
# Good: [[[ "question__block.html" ]]]
#
#  Bad: [[[ " question__block.html  "]]] 
#

def parse_base_file(folder, filename):
	try:
		f = open(BASE_DIR + folder + filename, "r")
		copy = f.read()
		f.close()

		# create empty file:
		f = open(BASE_DIR + TARGET_DIR + filename, "w")
		f.close()

		# open it for writing at the end:
		f = open(BASE_DIR + TARGET_DIR + filename, "a")

		left_t = 0
		right_t = 0
		ins = 0  # just stats

		# move 'left' side of file in new file adding nessesary insertions 
		while True:
			left_t = copy.find("[[[")

			if left_t == -1:
				print """File "{0}" complete with {1} insertions""".format(BASE_DIR + TARGET_DIR + filename, ins)

				# insert what left!!!
				f.write(copy)
				f.close()
				break  # will be the last cycle 

			buf = copy[:left_t]

			f.write(buf)

			copy = copy[left_t + 3:]  # cut that,  len("[[[") = 3, that is flexible

			right_t = copy.find("]]]")

			# parse filename properly:
			buf = copy[:right_t]
			i = buf.find('"')
			buf = buf[i+1:]
			i = buf.find('"')
			include = buf[:i]

			# open include, add content....
			print 'Found "{0}"'.format(include)
			try:
				include_file = open(BASE_DIR + folder + include, "r")
				include_content = include_file.read()
				include_file.close()

				f.write(include_content)
			except:
				print "No matching file found..."
				f.close()
				# delete target file...
				remove(BASE_DIR + TARGET_DIR + filename)
				break

			copy = copy[right_t + 3:]
			ins += 1

	except Exception as e:
		print "Error (parse_base_file): {0}".format(e)


if __name__ == "__main__":
	print "--"*40
	for targ_file in TARGET_FILES:
		for folder in SOURCE_DIRS:
			all_files = listdir(folder)

			if targ_file in all_files:
				parse_base_file(folder, targ_file)
				print "--"*40
				break

