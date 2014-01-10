#!/bin/csh 
#$ -N eman2_sGC 
#$ -S /bin/tcsh
#$ -cwd
#$ -V
#$ -pe ompi 30

# "start.hdf" is the input stack

mpirun -np $NSLOTS $EMAN2DIR/contrib/nogales/refine.py start.hdf ribo_5562_IP84_lp80.spi ref1 --ou=40 --rs=1 --xr='5 3 3 2 2' --ts='1 1 1 1 0.5'  --delta='25 20 15 10 5' --an='-1 -1 -1 180 90' --term=70 --pix_cutoff='0 0 0 0 0' --snr=0.15  --maxit=4 --ref_a=S --sym=c1 --cutoff=1 --MPI
