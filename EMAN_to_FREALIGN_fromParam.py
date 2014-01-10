#!/usr/bin/env python

from sys import *
import os
from optparse import OptionParser
import glob
import subprocess
from os import system
import sys
import optparse 

def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog -p <parameter filek>")
        parser.add_option("-p",dest="param",type="string",metavar="FILE",
                help="EMAN2 parameter file")
	parser.add_option("--num",dest="num",type="int", metavar="INT",
		help="number of models used in refinement (only necessary when outputting SPIDER document files")
	parser.add_option("-s", action="store_true",dest="spider",default=False,
		help="Flag to output converted angles in SPIDER documentation format")

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

def Eman2Freali(az,alt,phi):

    t1 = Transform({"type":"eman","az":az,"alt":alt,"phi":phi,"mirror":False})

    #t_conv = Transform({"type":"eman","alt":31.717474411458415,"az":90,"phi":-90,"mirror":False})

    #t2 = t1*t_conv.inverse()

    d = t1.get_params("eman")

    psi = d["phi"]+90

    if psi >360:

        psi = psi-360

    theta= d["alt"]

    phi = d["az"]-90

    return psi,theta,phi

def main1(params):
	parm=params['param']
	num=float(params['num'])
	spi = params['spider']

	if num == 1:
		f=open(parm,'r')
		out = open("%s_01_frealign"%(parm),'w')
	  	count=1
		count2=1
		count=1
		if spi is True:
	
				spiOut = open("%s_01.spi" %(parm),'w')
		print "\n"
		print "Calculating euler angle conversion..."
		print "\n"
				
		for line in f:
					
			l = line.split()
		
			parmPSI = float(l[0])
			parmTHETA = float(l[1])
			parmPHI = float(l[2])
			sx =(float(l[3]))
			sy =(float(l[4]))
			model = float(l[5])

			psi,theta,phi = Eman2Freali(parmPSI,parmTHETA,parmPHI)	
			
			out.write("%s 	%s	%s	%s	%s	%s\n"%(psi,theta,phi,sx,sy,model))

			if spi is True:			
				if model == 999:
		
					spiOut.write("%7d	%7d	%8.3f	%8.3f	%8.3f	%8.3f	%8.3f	%8.3f\n" %(count2,6,psi,theta,phi,sx,sy,count))
					count2 = count2 + 1
			count=1+count

		f.close()
		out.close()
		spiOut.close()

	if num == 2:
		f=open(parm,'r')
		out = open("%s_frealign"%(parm),'w')
	  	count1=1
		count2=1
		count=1
		if spi is True:
	
				spiOut1 = open("%s_01.spi" %(parm),'w')
				spiOut2 = open("%s_02.spi" %(parm),'w')

		print "\n"
		print "Calculating euler angle conversion..."
		print "\n"
				
		for line in f:
					
			l = line.split()
		
			parmPSI = float(l[0])
			parmTHETA = float(l[1])
			parmPHI = float(l[2])
			sx =(float(l[3]))
			sy =(float(l[4]))
			model = float(l[5])

			psi,theta,phi = Eman2Freali(parmPSI,parmTHETA,parmPHI)	
			
			out.write("%s 	%s	%s	%s	%s	%s\n"%(psi,theta,phi,sx,sy,model))

			if spi is True:			
				if model == 0:
		
					spiOut1.write("%7d	%7d	%8.3f	%8.3f	%8.3f	%8.3f	%8.3f	%8.3f\n" %(count1,6,psi,theta,phi,sx,sy,count))
					count1 = count1 + 1

				if model == 1:
		
					spiOut2.write("%7d	%7d	%8.3f	%8.3f	%8.3f	%8.3f	%8.3f	%8.3f\n" %(count2,6,psi,theta,phi,sx,sy,count))
					count2 = count2 + 1
			count=count+1

		f.close()
		out.close()
		spiOut1.close()
		spiOut2.close()


	if num == 3:
                f=open(parm,'r')
                out = open("%s_frealign"%(parm),'w')
                count1=1
                count2=1
		count3=1
                count=1
                if spi is True:

                                spiOut1 = open("%s_01.spi" %(parm),'w')
                                spiOut2 = open("%s_02.spi" %(parm),'w')
				spiOut3 = open("%s_03.spi" %(parm),'w')
                print "\n"
                print "Calculating euler angle conversion..."
                print "\n"

                for line in f:

                        l = line.split()

                        parmPSI = float(l[0])
                        parmTHETA = float(l[1])
                        parmPHI = float(l[2])
                        sx =(float(l[3]))
                        sy =(float(l[4]))
                        model = float(l[5])

                        psi,theta,phi = Eman2Freali(parmPSI,parmTHETA,parmPHI)

                        out.write("%s   %s      %s      %s      %s      %s\n"%(psi,theta,phi,sx,sy,model))

                        if spi is True:
                                if model == 0:

                                        spiOut1.write("%7d      %7d     %8.3f   %8.3f   %8.3f   %8.3f   %8.3f   %8.3f\n" %(count1,6,psi,theta,phi,sx,sy,count))
                                        count1 = count1 + 1

                                if model == 1:

                                        spiOut2.write("%7d      %7d     %8.3f   %8.3f   %8.3f   %8.3f   %8.3f   %8.3f\n" %(count2,6,psi,theta,phi,sx,sy,count))
                                        count2 = count2 + 1

				if model == 2:

                                        spiOut3.write("%7d      %7d     %8.3f   %8.3f   %8.3f   %8.3f   %8.3f   %8.3f\n" %(count2,6,psi,theta,phi,sx,sy,count))
                                        count3 = count3 + 1
                        count=count+1

		f.close()
                out.close()
                spiOut1.close()
                spiOut2.close()
		spiOut3.close()

#Need this at the end for the parse commands
if __name__ == "__main__":
     getEMANPath()
     from EMAN2 import *
     from sparx  import *
     params=setupParserOptions()
     main1(params)
