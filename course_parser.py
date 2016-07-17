# -*- coding: utf-8 -*-
#parse courses from input file and update course list (courses.csv)
inputfile = open('C:courses_input.txt')
outputfile = open('C:courses.csv', 'w')

my_text = inputfile.readlines()

for i in range(0,len(my_text)):
	if my_text[i].startswith('0'):
		outputfile.write(my_text[i-1]+","+my_text[i]+"\n");
	
inputfile.close()
outputfile.close()

print " complete"

