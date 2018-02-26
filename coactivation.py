#!/usr/bin/env python
# this is just a simple example of how you can get coactivation maps seeding from each coordinate in a giant list of coordinates. There are some hard paths here to substitute so be careful.


#import necessary modules
import os
from neurosynth import Dataset
from neurosynth import meta, decode, network

#import dataset and tools
dataset = Dataset('/usr/local/lib/python2.7/site-packages/neurosynth/database.txt')
dataset.add_features('/usr/local/lib/python2.7/site-packages/neurosynth/features.txt')


array = [] #declaring a list with name '**array**'

#now read in a text file of coordinates from 2mm MNI brain. Delimiter is single space. Fourth column is 'intensity' value of a binarized GM mask. Only coordinates with value of one ar included
with open('/Users/ateghipc/Desktop/spt/ROI/PT/PT_REVERSEINFERENCE_pFgA_z_FDR_0.01_BIN_MNI.txt','r') as reader :
    for line in reader :
        print(line)
        allLine = line.split(' ', 5 ) #split line to remove intensity value for each line
        xCoord = allLine[0] #was zero
        print(xCoord)
        yCoord = allLine[1] #was 2
        print(yCoord)
        zCoord = allLine[2] #was 4
        print(zCoord)

        pre='Voxel_'
        intra='_'
        prfx= pre+xCoord+intra+yCoord+intra+zCoord #filename prefix is x y z coordinate

        network.coactivation(dataset, [[int(xCoord), int(yCoord), int(zCoord)]], threshold=0.1, r=2, output_dir='/Users/ateghipc/Desktop/spt/coactivation/2mmRadius/2mmSpace', prefix=prfx)
        network.coactivation(dataset, [[int(xCoord), int(yCoord), int(zCoord)]], threshold=0.1, r=3, output_dir='/Users/ateghipc/Desktop/spt/coactivation/3mmRadius/3mmSpace', prefix=prfx)

        array.append(line)

