#!/usr/bin/env python

import optparse
from sys import *
import os,sys,re
from optparse import OptionParser
import glob
import subprocess

def setupParserOptions():
	parser = optparse.OptionParser()
	parser.set_usage("%prog -f <stack>")
	parser.add_option("-f",dest="stack",type="string",metavar="FILE",
		help="HDF particle stack")

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

def getEMANPath():        
	### get the eman2 directory        
	emanpath = subprocess.Popen("env | grep EMAN2DIR", shell=True, stdout=subprocess.PIPE).stdout.read().strip()        
	
	if emanpath:                
		emanpath = emanpath.replace("EMAN2DIR=","")                
	if os.path.exists(emanpath):                        
		return emanpath        
	print "EMAN2 was not found, make sure it is in your path"        
	sys.exit()

def main2(params):

	s = params['stack']
	dummy = EMData()
	nimat = EMUtil.get_image_count(s)
	o = s.strip('.hdf')
	output_file = "paramout_%s" %(o)
	foutput = open(output_file, 'w')
	for im in xrange(nimat):
		dummy.read_image(s,im,True)
		param3d = dummy.get_attr('xform.projection')
		# retrieve alignments in EMAN-format
		paramEMAN = param3d.get_params('eman')
		g = dummy.get_attr("group")
		outstring = "%f\t%f\t%f\t%f\t%f\t%i\n" %(paramEMAN["az"], paramEMAN["alt"], paramEMAN["phi"], paramEMAN["tx"], paramEMAN["ty"], g)
		foutput.write(outstring)
	foutput.close()

if __name__ == "__main__":
     getEMANPath()
     from EMAN2 import *
     from sparx  import *
     params=setupParserOptions()
     main2(params)
   

