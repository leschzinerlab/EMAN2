#!/usr/bin/env python

#Phase flip stack c/o Richard J. Hall

#To use:
#./phase_flip.py [stack].hdf

import sys
from EMAN2 import *

stack = sys.argv[1]

new = '%s_flip.hdf' %(stack[:-4])

def main():

	process_stack(stack, new, invert=True,edgenorm=True)


def process_stack(stackfile,outfile, phaseflip=True,phasehp=None,wiener=None,edgenorm=True,oversamp=1,default_ctf=None,invert=False,virtualout=None,storeparm=False,source_image=None):
        """Will phase-flip and/or Wiener filter particles in a file based on their stored CTF parameters.
        phaseflip should be the path for writing the phase-flipped particles
        wiener should be the path for writing the Wiener filtered (and possibly phase-flipped) particles
        oversamp will oversample as part of the processing, ostensibly permitting phase-flipping on a wider range of defocus values
        """

        im=EMData(stackfile,0)
        ys=im.get_ysize()*oversamp
        ys2=im.get_ysize()
        n=EMUtil.get_image_count(stackfile)
        lctf=None

	for i in range(n):
                
		#print ("Working on image #%s" %(i))
		im1 = EMData()
		im1.read_image(stackfile,i)
                ctf=im1["ctf"]
                
		if edgenorm : im1.process_inplace("normalize.edgemean")
                if oversamp>1 :
                        im1.clip_inplace(Region(-(ys2*(oversamp-1)/2),-(ys2*(oversamp-1)/2),ys,ys))
#                       print -(ys2*(oversamp-1)/2),-(ys2*(oversamp-1)/2),ys,ys
#               print i
                fft1=im1.do_fft()

                if phaseflip or phasehp:
                        if not lctf or not lctf.equal(ctf):
                                flipim=fft1.copy()
                                ctf.compute_2d_complex(flipim,Ctf.CtfType.CTF_SIGN)
#                               if i==0: flipim.write_image("flip.mrc")
                        fft1.mult(flipim)
                        out=fft1.do_ift()
                        out["ctf"]=ctf
                        out["apix_x"] = ctf.apix
                        out["apix_y"] = ctf.apix
                        out["apix_z"] = ctf.apix
                        out.clip_inplace(Region(int(ys2*(oversamp-1)/2.0),int(ys2*(oversamp-1)/2.0),ys2,ys2))
                        if invert: out.mult(-1.0)
                        out.process("normalize.edgemean")
                        if phaseflip: out.write_image(outfile,i)

if __name__ == "__main__":
        main()
                  
