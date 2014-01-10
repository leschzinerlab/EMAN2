#!/usr/bin/env python

import os,sys
import subprocess
import optparse

#==========================
def setupParserOptions():
	parser = optparse.OptionParser()
	parser.set_usage("%prog -p <paramout>")
	parser.add_option("-p",dest="param",type="string",metavar="FILE",
		help="EMAN2 output parameter file")
	parser.add_option("--num",dest="num",type="float",metavar="FLOAT", 
		help="Number of models used")

	options,args = parser.parse_args()

	if len(args) > 1:
		parser.error("Unknown commandline options: " +str(args))

	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit()

	params={}
	for i in parser.option_list:
		if isinstance(i.dest,str):
			params[i.dest] = getattr(options,i.dest)
	return params

def select(params):
	
	numMods = params['num']
	print 'numMods = %02d' %(numMods)
	if float(numMods) == 1:	

		fopen = open(params['param'],'r')
		fout = open('%s_model00.par' %(params['param']),'w')

		for line in fopen:
	
			l = line.split()

			group = l[5]

			if float(group) == 999:
				
				fout.write(line)

		fopen.close()			

	if float(numMods) > 1:

		modCount = 0
		numMods = numMods - 1
		while modCount <= numMods:
			print "Working on model #%01d" %(modCount)
			
	                fopen = open(params['param'],'r')
	                fout = open('%s_model%02d.par' %(params['param'],modCount),'w')

                	for line in fopen:
        
        	                l = line.split()
	
	                        group = l[5]

                        	if float(group) == modCount:
                	                                
        	                        fout.write(line)

	                fopen.close()

			modCount = modCount + 1


if __name__ == "__main__":
	
	params=setupParserOptions()
	select(params)
