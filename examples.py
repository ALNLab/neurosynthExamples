#!/usr/bin/env python

# This script is meant to show some examples for using neurosynth. Hard paths are used in places so be careful

# import necessary modules
import os # this is sometimes helpful
from neurosynth import Dataset
from neurosynth import meta, decode, network

# First we need to import dataset and tools with which to use neurosynth. Feel free to add your own.
dataset = Dataset('/usr/local/lib/python2.7/site-packages/neurosynth/database.txt')
dataset.add_features('/usr/local/lib/python2.7/site-packages/neurosynth/features.txt')

# Here is an example for how to do coactivation analysis. Lets say you want to do a fine grained analysis where you get coavtivation with individual voxels in an ROI or something like that. This snippet of code will go through your list of coordinates (saved as a seperate text file), and get a coactivation for each coordinate (see code for formatting)
inTextFile = '/Users/ateghipc/Desktop/spt/ROI/PT/PT_REVERSEINFERENCE_pFgA_z_FDR_0.01_BIN_MNI.txt';

# now read in a text file of coordinates from 2mm MNI brain. Delimiter is single space. Fourth column is 'intensity' value of a binarized GM mask. Only coordinates with value of one are included (i.e. in a binarized mask). 
with open(inTextFile,'r') as reader :
    for line in reader :
        print(line)
        allLine = line.split(' ', 5 ) #split line to remove intensity value for each line
        xCoord = allLine[0] #was zero
        print(xCoord)
        yCoord = allLine[1] #was 2
        print(yCoord)
        zCoord = allLine[2] #was 4
        print(zCoord)

        pre='Voxel_' #this is just a prefix for the file name
        intra='_'
        prfx= pre+xCoord+intra+yCoord+intra+zCoord # full filename will is: Voxel_ x y z coordinate

        network.coactivation(dataset, [[int(xCoord), int(yCoord), int(zCoord)]], threshold=0.1, r=2, output_dir='/Users/ateghipc/Desktop/spt/coactivation/2mmRadius/2mmSpace', prefix=prfx) # note the radius! Your seed is a 2 mm sphere in 2mm mni space (THIS WILL LOOK FUNKY! TALK TO TAL!)
        network.coactivation(dataset, [[int(xCoord), int(yCoord), int(zCoord)]], threshold=0.1, r=3, output_dir='/Users/ateghipc/Desktop/spt/coactivation/3mmRadius/3mmSpace', prefix=prfx) # this will look better. There's some bug fundamental to the python module we are provided by neurosynth. 
        array.append(line)

# Now lets say you want to do a meta-analysis of a term. You need to choose a term and a frequency threshold for including a study in your meta-analysis     
feat = "planum temporale"
fq = 0.01 # this means studies must use the phrase 1/100 times
pt_ids = dataset.get_studies(feat, frequency_threshold=fq) # this gets all of the unique study identifiers matching your search
numPTstudies = len(pt_ids)  #this tells you the number of studies using the phrase you selected at the frequency you selected (i.e. what goes into the meta-analysis)
ma = meta.MetaAnalysis(dataset, pt_ids) # now do meta-analysis
ma.save_results('.', '/PT') # change the output name to something you like. Saved to working directory (i.e. pwd)

# Okay but lets say you want to do a contrast analaysis where you compare studies in one feature to those in another (e.g. Planum Temporale vs Heschl's Gyrus; this way you see the activity associated with PT over HG). 
feat2 = "auditory cortex"
hg_ids = dataset.get_studies(feat2, frequency_threshold=fq)
ma = meta.MetaAnalysis(dataset, pt_ids, hg_ids)
ma.save_results('.', '/PTvsHG')

# and what if you want to play around with FDR?
feature_list = dataset.get_feature_names(['word recognition','speech production'])
meta.analyze_features(dataset, feature_list, threshold=0.001, q=0.05, output_dir='/Users/ateghipc/Desktop/DualStreamUpdateFigs/manual/q001')


# here's an example for classifying ROIs without getting your hands dirty
from neurosynth.analysis import classify
roi1 = "/Users/ateghipc/Desktop/spt/ROI/PT/clusterSolutions/Kmeans_solution_2_Cluster_2_bin.nii"
roi2 = "/Users/ateghipc/Desktop/spt/ROI/PT/clusterSolutions/Kmeans_solution_2_Cluster_1.nii"

results = classify.classify_regions(dataset, [roi2, roi1],threshold=0.2)
results['n'] #studies in the first class vs the second 
results['score'] # this is your classification score
results = classify.classify_regions(dataset, [roi2, roi1],threshold=0.2, method="Dummy") 
results['score'] #this is a dummy classifier score

# here's an example for classification with a lot of parameterization 
(X, y) = classify.get_studies_by_regions(dataset,[roi2, roi1], threshold=0.2,remove_overlap=True, studies=None, features=None, regularization='scale')
method='ERF'
threshold=0.08
remove_overlap=True
regularization='scale'
output='summary'
studies=None
features=None
class_weight='auto'
classifier=None
cross_val='4-Fold'
param_grid=None
scoring='accuracy'
refit_all=True
feat_select=None
clf_method='ERF'

clf = classify.Classifier(clf_method, classifier, param_grid)
score = clf.cross_val_fit(X, y, cross_val, scoring=scoring, feat_select=feat_select, class_weight=class_weight)

# for a permutation testing and proper cross val get sklearn 
from sklearn.svm import SVC
svm = SVC(kernel='linear')
from sklearn.model_selection import permutation_test_score
from sklearn.model_selection import StratifiedKFold
cv = StratifiedKFold(10)
score, permutation_scores, pvalue = permutation_test_score(svm, X, y, scoring="accuracy", cv=cv, n_permutations=1,n_jobs=1) #cv should really be self.cver
print("Classification score %s (pvalue : %s)" % (score, pvalue))

# and here's an example where we use a decoder
from neurosynth.analysis import decode
decoder = decode.Decoder(dataset=dataset, method='pearson', features=None, mask=None, image_type='pFgA_z', threshold=0.001)
result = decoder.decode('/Users/ateghipc/Desktop/DualStreamUpdateFigs/newerNeurosynthverTest/speechproduction_specificity_z_FDR_0.001.nii.gz', save='/Users/ateghipc/Desktop/DualStreamUpdateFigs/newerNeurosynthverTest/speechproduction_specificity_z_FDR_0.001_decoded.txt')
