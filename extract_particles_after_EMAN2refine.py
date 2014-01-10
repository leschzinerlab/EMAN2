#!/usr/bin/env python 

import sys
import subprocess
from optparse import OptionParser
import optparse

def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog -f <stack> -p <parameter file> --num=<FLOAT>")
        parser.add_option("-f",dest="stack",type="string",metavar="FILE",
                help="HDF particle stack")
        parser.add_option("-p",dest="param",type="string",metavar="FILE",
                help="EMAN2 output parameter file")
        parser.add_option("--num",dest="num",type="int", metavar="INT",
                help="number of models used in refinement")
        options,args = parser.parse_args()

        if len(args) > 4:
                parser.error("Unknown commandline options: " +str(args))

        if len(sys.argv) < 4:
                parser.print_help()
                sys.exit()
	params={}        
	for i in parser.option_list: 
        	if isinstance(i.dest,str):
	                params[i.dest] = getattr(options,i.dest)        
	return params
def main(params):

	stack=params['stack'] 
	numMods=int(params['num'])
	new=stack.strip('.hdf')

	if numMods == 1:

       		param=open(params['param'],'r')
       		count=1
       		text='%s_%02d.txt' %(new,1)

       		text=open(text,'w')

       		for line in param:
                	l=line.split()
                 	member=float(l[5])

                 	if member == 999:

                         text.write("%s\n" %(count-1))
	
        	         count=count+1

      		text.close()
       		param.close()
	        cmd="e2proc2d.py --list=%s_%02d.txt %s %s_%02d.hdf " %(new,1,stack,new,1)
       		subprocess.Popen(cmd,shell=True).wait()
	else:
		for n in range(0,numMods):
			param=open(params['param'],'r')

			count=1

			text='%s_%02d.txt' %(new,n)	

			text=open(text,'w')

			for line in param:

				l=line.split()
				member=float(l[5])
	
				if member == n:

					text.write("%s\n" %(count-1))

			
				count=count+1
			text.close()
			param.close()
			cmd="e2proc2d.py --list=%s_%02d.txt %s %s_%02d.hdf " %(new,n,stack,new,n)
			subprocess.Popen(cmd,shell=True).wait()

if __name__ == "__main__":
     params=setupParserOptions()
     main(params)
