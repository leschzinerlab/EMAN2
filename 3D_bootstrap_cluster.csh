#!/bin/csh -f

# Name of job
#$ -N Bootstrap

# Set parallel environment; set number of processors
#$ -pe orte 48

# Max walltime for this job (2 hrs)
##$ -l h_rt=02:00:00

# Merge the standard out and standard error to one file
##$ -j y

# Run job through csh shell
#$ -S /bin/csh

# use current working directory
#$ -cwd

# The following is for reporting only. It is not really needed
# to run the job. It will show up in your output file.
#
mpirun -np $NSLOTS sxbootstrap_bigdisk.py bdb:new wght.txt Vols buffer --nvol=26016 --nbufvol=25 --seedbase=17 --MPI
