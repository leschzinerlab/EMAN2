#!/usr/bin/env python

import os
from optparse import OptionParser
import sys
import subprocess

def getEMAN2():
	### get the imagicroot directory        
        emanpath = subprocess.Popen("env | grep EMAN2DIR", shell=True, stdout=subprocess.PIPE).stdout.read().strip()

        if emanpath:
                emanpath = emanpath.replace("EMAN2DIR=","")
        if os.path.exists(emanpath):
                return emanpath
        print "EMAN2 was not found, make sure eman2/2.05 is in your path"        
        sys.exit()	

def main2():
	arglist = []
        for arg in sys.argv:
		arglist.append( arg )
	        progname = os.path.basename(arglist[0])
	        usage = progname + " raw_images apix <CTFparfile>"
	        parser = OptionParser(usage,version="1.0")
	        (options, args) = parser.parse_args(arglist[1:])
        if len(args) < 2:
                print "usage: " + usage
                print "Please run '" + progname + " -h' for detailed options"
	else:
		a = EMData()
		fname = args[0]
		apix = float(args[1])
		ctfpar = None
		helical = False
		if len(args) == 3:
			ctfpar = args[2]
			if not os.path.isfile(ctfpar):
				print "Error: ctf file '%s' is not found"%ctfpar
				sys.exit()
			# get ctf values from parfile
			from utilities import generate_ctf
			pfile = open(ctfpar).readlines()
			ctfinfo=[0]*len(pfile)

			# check if there are helical parameters:
			if len(pfile[0].strip().split())==9:
				helical = True
				hinfo=[0]*len(pfile)

			# store info
			for p in pfile:
				nfo = p.strip().split()
				pnum=int(float(nfo[0]))-1
				df1=float(nfo[1])
				df2=float(nfo[2])
				astig = float(nfo[3])
				kv = int(float(nfo[4]))
				cs = float(nfo[5])
				ampc = float(nfo[6])*100
				
				if helical is True:
					hnum = int(float(nfo[7]))
					angle = float(nfo[8])
					angle = -angle+90
					if angle > 360: angle -= 360
					if angle < 0: angle += 360
					hinfo[pnum]=angle
				"""
				# For future use if taking from FREALIGN
				if p[0]=="C":
					continue
				(pnum,psi,theta,phi,shx,shy,mag,hnum,ctf1,ctf2,angle,pres,delta)=p.strip().split()
				pnum=int(pnum)-1
				kv=300
				cs=2.7
				ampc=5
				"""
				df=(float(df1)+float(df2))/2
				ctfinfo[pnum]=generate_ctf([df,cs,kv,apix,0.0,ampc])

		imn = EMUtil.get_image_count(fname) 
		print "Generating 'start.hdf' with %i particles"%imn
		for i in xrange(imn):
			a.read_image(fname,i)
			a.set_attr_dict({'active':1})
			if ctfpar is not None:
				a.set_attr("ctf",ctfinfo[i])
			if helical is True:
				a.set_attr("h_angle",hinfo[i])
			t2 = Transform({"type":"spider","phi":0,"theta":0,"psi":0})
		        a.set_attr("xform.projection", t2)
			a.set_attr("apix_x",apix )
			a.write_image("start.hdf",i)
			print "%3i%% complete\t\r"%(int(float(i)/imn*100)),
		print "100% complete\t"

if __name__ == "__main__":
        getEMAN2()
	from global_def import *
	from EMAN2  import *
	main2()

