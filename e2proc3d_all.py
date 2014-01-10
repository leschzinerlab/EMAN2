#!/usr/bin/env python 

#This will convert all volumes within an HDF file into separate SPIDER volumes

#To run:

#./e2proc3d_all.py [number of volumes per file]

import glob
import subprocess
import sys

numVols=float(sys.argv[1])

list=glob.glob('volf*')

for line in list:

	new=line.strip('.hdf')

	for i in range(0,numVols):
		next=i+1

		cmd="e2proc3d.py --first=%s --last=%s %s %s_%03d.hdf" %(i,i,line,new,next)
		subprocess.Popen(cmd,shell=True).wait()
		
		cmd="proc3d %s_%03d.hdf %s_%03d.img imagic" %(new,next,new,next)
		subprocess.Popen(cmd,shell=True).wait()

		cmd="rm %s_%03d.hdf" %(new,next)
		subprocess.Popen(cmd,shell=True).wait()

		cmd="./e2proc3d_all.b %s_%03d" %(new,next)
		subprocess.Popen(cmd,shell=True).wait()

		cmd="rm %s_%03d.img" %(new,next)
		subprocess.Popen(cmd,shell=True).wait()

		cmd="rm %s_%03d.hed" %(new,next)
		subprocess.Popen(cmd,shell=True).wait()
