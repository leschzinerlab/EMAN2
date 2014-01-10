#!/usr/bin/env python

import os,sys
import subprocess
import optparse

#==========================
def setupParserOptions():
	parser = optparse.OptionParser()
	parser.set_usage("%prog -s <stack>")
	parser.add_option("-s",dest="stack",type="string",metavar="FILE",
		help="HDF particle stack")
	parser.add_option("-p",dest="paramfile",type="string",metavar="FILE",
		help="EMAN2 output parameter file")
	parser.add_option("-d",dest="dim",type="int",metavar="#", default=512,
		help="dimension of output (in pixels, default is 512)")
	parser.add_option("--scale",dest="scale",type="float",metavar="FLOAT", default=1.0,
		help="multiplier to resize circles in the plot, larger number means larger circles (default=1.0)")

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

#==========================
def checkConflicts(params):
	if (params['paramfile'] and params['stack']):
		print "specify an EMAN2 stack OR a parameter file, not both"
		sys.exit()
	if params['paramfile'] and not os.path.isfile(params['paramfile']):
		print "the specified EMAN2 parameter file '%s' does not exist"%params['paramfile']
		sys.exit()
	if params['stack'] and not os.path.isfile(params['stack']):
		print "the specified EMAN2 stack file '%s' does not exist"%params['stack']
		sys.exit()

#==========================
def getParamsFromFile(params):
	print "retrieving EMAN2 Eulers from file"
	f = open(params['paramfile'])
	stackparams = []
	uniqEul=[]
	im=1
	for line in f:
		l = line.strip().split()
		if len(l) < 6:
			continue
		e_az=float(l[0])
		e_alt=float(l[1])
		e_phi=float(l[2])
		tx=float(l[3])
		ty=float(l[4])
		g=float(l[5])
		psi,theta,phi = Eman2Freali(e_az,e_alt,e_phi)

		stackparams.append({'p':im, 'psi':psi, 'theta':theta, 'phi':phi, 'tx':tx, 'ty':ty, 'group':g})
		im+=1
		## get unique Eulers
		euler = [theta,phi]
		if euler not in uniqEul:
			uniqEul.append(euler)

	return uniqEul,stackparams

#==========================
def getParamsFromStack(params):
	print "retrieving EMAN2 Eulers from stack"
	s = params['stack']
	dummy = EMData()
	nimat = EMUtil.get_image_count(s)
	stackparams = []

	foutput = open("paramsFromStack.out",'w')
	uniqEul=[]
	for im in xrange(nimat):
		dummy.read_image(s,im,True)
		param3d = dummy.get_attr('xform.projection')
		# retrieve alignments in EMAN-format
		pe = param3d.get_params('eman')
		e_az=pe['az']
		e_alt=pe['alt']
		e_phi=pe['phi']
		tx=pe['tx']
		ty=pe['ty']
		g = dummy.get_attr("group")
		psi,theta,phi = Eman2Freali(e_az,e_alt,e_phi)
		## get unique Eulers
		euler = [theta,phi]
		if euler not in uniqEul:
			uniqEul.append(euler)
		stackparams.append({'p':im+1, 'psi':psi, 'theta':theta, 'phi':phi, 'tx':tx, 'ty':ty, 'group':g})

		outstring = "%f\t%f\t%f\t%f\t%f\t%i\n" %(pe["az"], pe["alt"], pe["phi"], pe["tx"], pe["ty"], g)
		foutput.write(outstring)
	foutput.close()
	
	return uniqEul,stackparams

#==========================
def assignEulersToParticles(eulers,stackparams):
	uniqEul = sorted(eulers, key=lambda k: float(k[0]))

	# assign corresponding Euler angle from sorted unique list
	# keep track of which Euler has the most particles
	numEulers=[0]*len(eulers)
	print "assigning particles to Euler references"
	for p in stackparams:
		euler = [p['theta'],p['phi']]
		pos = uniqEul.index(euler)
		numEulers[pos]+=1
		p['ref']=pos+1
	maxEulerNum = max(numEulers)
	return uniqEul,stackparams,maxEulerNum

#==========================
def writeAngVOEA(eulers):
	print "writing angvoea.spi"
	fout=open("angvoea.spi",'w')
	for i in xrange(len(eulers)):
		line = "%5d 3   0.00000  %8.3f  %8.3f\n"%(i+1,eulers[i][0],eulers[i][1])
		fout.write(line)
	fout.close()

#==========================
def writeAPMQ(stackparams):
	print "writing apmq.spi"
	fout=open("apmq.spi",'w')
	for part in stackparams:
		pnum=part['p']
		ref=part['ref']
		rot=part['psi']
		tx=part['tx']
		ty=part['ty']
		fout.write("%8i 6  %5i  999.99   %8.3f   %8.3f   %8.3f  %7i\n"%(pnum,ref,rot,tx,ty,pnum))
	fout.close()
	
#==========================
def Eman2Freali(az,alt,phi):
	t1 = Transform({"type":"eman","az":az,"alt":alt,"phi":phi,"mirror":False})
	d = t1.get_params("eman")
	psi = d["phi"]+90
	if psi >360:
		psi = psi-360
	theta= d["alt"]
	phi = d["az"]-90
	return psi,theta,phi

#==========================
def getEMANPath():
	### get the eman2 directory        
	emanpath = subprocess.Popen("env | grep EMAN2DIR", shell=True, stdout=subprocess.PIPE).stdout.read().strip()
	if emanpath:                
		emanpath = emanpath.replace("EMAN2DIR=","")                
	if os.path.exists(emanpath):                        
		return emanpath        
	print "EMAN2 was not found, make sure it is in your path"        
	sys.exit()

#==========================
def runSpiderPlot(params):
	## first write script
	spi=open("eulerplotScript.spi",'w')
	dim = params['dim']
	scalingFactor=dim/20
	scalingFactor*=params['scale']
	# generate how many file
	spi.write("VO MQ\n0.0\napmq\n%i\ntmpselect****\nhow_many\n\n"%params['numE'])
	# generate blank image
	spi.write("BL\n_1\n%i,%i\nN\n0.0\n\n"%(dim,dim))
	# add outer circle
	cen=(params['dim']/2)+1
	margin = 4
	rad=cen-margin
	spi.write("PT\n_1\nCL\n%i,%i\n%i\nN\n\n"%(cen,cen,rad))
	# add cross hairs
	spi.write("PT\n_1\nL\n%i,%i\n%i,%i\n"%(margin+1,cen,dim-margin,cen))
	spi.write("Y\nL\n%i,%i\n%i,%i\nN\n\n"%(cen,margin+1,cen,dim-margin))
	# loop through all eulers
	spi.write("UD N x19\nhow_many\n")
	spi.write("DO LB1 x20=1,x19\n")
	spi.write("  UD IC,x20,x51,x52,x53\nangvoea\n\n")
	spi.write("  IF(x52.LE.90.0) GOTO LB2\nx52=180.0-x52\nx53=x53+180.0\n\n")
	spi.write("  IF(x53.LT.360.0) GOTO LB2\nx53=x53-360.0\n\n")
	spi.write("  LB2\n\n")
	spi.write("  x61=x52/90\nx55=%i-3\nx61=x61*x55\nx81=cos(x53)\nx82=sin(x53)\n"%(rad))
	spi.write("  x81=x81*x61\nx82=x82*x61\nx81=x81+%i\nx82=x82+%i\n\n"%(cen,cen))
	spi.write("  UD x20,x71\nhow_many\n\n")
	spi.write("  IF(x71.eq.0) GOTO LB1\n\n")
	# scale values to 0-1 based on euler with most particles
	spi.write("  x72=(x71/%i)\n"%params['maxnum'])
	spi.write("  x72=x72*%i\n\n"%scalingFactor)
	spi.write("  PT\n_1\nC\n(x81,x82)\n(x72)\nN\n\n")
	spi.write("  LB1\n\n")
	# invert contrast
	spi.write("NEG\n_1\n_2\n\n")
	spi.write("CP\n_2\nfinalplot\n\n")
	spi.write("DE A\ntmpselect0001\n\n")
	spi.write("EN D\n\n")
	
	spi.close()

	# run script
	print "running SPIDER"
	subprocess.Popen("spider spi @eulerplotScript",shell=True).wait()

#=========================
def cleanup():
	if os.path.isfile("finalplot.spi"):
		flist = ["eulerplotScript.spi","LOG.spi","how_many.spi"]
		for f in flist:
			if os.path.isfile(f):
				os.remove(f)
	print "\nFinal image saved as 'finalplot.spi'\n"

#==========================
if __name__ == "__main__":
	getEMANPath()
	from EMAN2 import *
	from sparx import *
	params=setupParserOptions()
	if params['paramfile']:
		eulers,stackparams=getParamsFromFile(params)
	else:
		eulers,stackparams=getParamsFromStack(params)
	params['numE']=len(eulers)
	print "found %i unique Eulers"%(len(eulers))
	
	eulers,stackparams,params['maxnum']=assignEulersToParticles(eulers,stackparams)
	writeAngVOEA(eulers)
	writeAPMQ(stackparams)
	runSpiderPlot(params)
	cleanup()


