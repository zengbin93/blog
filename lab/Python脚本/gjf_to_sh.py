# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 15:32:41 2016

@author: Mike
"""
import os
from tkinter.filedialog import askdirectory

path = askdirectory()
os.chdir(path)

part1 = '''#!/bin/bash
APP_NAME=intelg_small
NP=1
RUN="RAW"
CURDIR=$PWD
NP_PER_NODE=12


'''


part4 = '''

## Gaussian 09 setup
export g09root=/home-gg/Soft/Gaussian.D01.Linda
export GAUSS_SCRDIR=/home-gg/users/nscc1352_CCX/scratch
export GAUSS_EXEDIR=$g09root/g09
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$g09root/g09
export PATH=$g09root/g09:$PATH
cd $PWD

#start creating .nodelist
rm -f $PWD/nodelist >& /dev/null
for i in `echo $LSB_HOSTS`
do
    echo "$i" >> $PWD/nodelist
done
nodelist=$(cat $PWD/nodelist | uniq | awk '{print $1}' | tr '\\n' ',')
NProcShared=$NP_PER_NODE
cat $INPUT | sed -e "s/%[Nn][Pp][Rr][Oo][Cc][^ \\t]*=[0-9]*//" \\
           | sed -e "s/%[Ll][Ii][Nn][Dd][Aa][^ \\t]*//" \\
           | sed -e "1i\\%NProcShared=$NProcShared" \\
           | sed -e "1a\\%LindaWorker=$nodelist" \\
           | sed -e "s/\\r$//"  \\
           >"$INPUT".linda

##Run  Gaussian 09 
date > time
g09 < "$INPUT".linda > $OUTPUT
date >> time
sleep 1







'''
def sh_to_gjf(gjf_file,part1,part4):
    f_name = gjf_file.replace('.gjf','')
    print(f_name)
    part2 = 'INPUT='+f_name+'.com\n'
    part3 = 'OUTPUT='+f_name+'.log\n'
    sh_file = f_name + '.sh'
    sh_file = open(sh_file,'w')
    sh_file.write(part1)
    sh_file.write(part2)
    sh_file.write(part3)
    sh_file.write(part4)
    sh_file.close()


for root, dirs, files in os.walk(path):
    for file in files:
        if '.gjf' in file:
            sh_to_gjf(file,part1,part4)
            
