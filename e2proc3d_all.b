#!/bin/csh -f

set file=$1

setenv IMAGIC_BATCH 1
echo "! "
echo "! "
echo "! ====================== "
echo "! IMAGIC ACCUMULATE FILE "
echo "! ====================== "
echo "! "
echo "! "
echo "! IMAGIC program: em2em ------------------------------------------------"
echo "! "
/opt/qb3/imagic-110326/stand/em2em.e <<EOF
IMAGIC
SPI
SIN
3
${file}
${file}.spi
LINUX
YES
EOF
