
# coding: utf-8

# In[19]:

import re, os


ANSIG_PATTERN = re.compile(r'^\s*ANSIG\s.+crosspeak')
AUTOASSIGN_PATTERN = re.compile(r'^\s*\d+\s+\d+\.\d+\s+\d+\.\d+\s.*\s*\S.+\d+\s\S+\s*')
NMRVIEW_PATTERN = re.compile(r'^\d+\s+{.+}\s+\d+\.?\d*\s+\d+\.?\d*\s+\d+\.?\d*')
NMRDRAW_PATTERN = re.compile(r'^DATA\s+X_AXIS\s+')
NMRSTAR_PATTERN = re.compile(r'^\s*save_shift_set|save_assigned_chem_shift_list|save_peak_list')
SPARKY_PATTERN = re.compile(r'^\s*Assignment\s.* w1 .+')
SPARKY_SAVE_PATTERN = re.compile(r'^<sparky save file>')
XEASY_PATTERN = re.compile(r'^#\s+Number of dimensions\s+\d')
WHITESPACE_AND_NULL = set(['\x00', '\t', '\n', '\r', '\x0b', '\x0c'])


def getPeakListFileFormat(filePath):
    if os.path.isdir(filePath):
        fileNames = os.listdir(filePath)

    # check not binary

    fileObj = open(filePath, 'rb')
    firstData = fileObj.read(1024)
    fileObj.close()

    testData = set([c for c in firstData]) - WHITESPACE_AND_NULL
#     print(testData)
#     if min([ord(c) for c in testData]) < 32:
#         return

    fileObj = open(filePath, 'r')

    for line in fileObj:
        if not line.strip():
            continue

        if SPARKY_SAVE_PATTERN.search(line):
            return "SPARKY"
        
        if NMRSTAR_PATTERN.search(line):
            return "NMRSTAR"

        if ANSIG_PATTERN.search(line):
            return "ANSIG"

        if XEASY_PATTERN.search(line):
            return "XEASY"

        if NMRDRAW_PATTERN.search(line):
            return "NMRDRAW"

        if NMRVIEW_PATTERN.search(line):
            return "NMRVIEW"

        if SPARKY_PATTERN.search(line):
            return "SPARKY"

        if AUTOASSIGN_PATTERN.search(line):
            return "AUTOASSIGN"



# In[181]:

res1to3dict = {
     
     'A': 'Ala',
     'C': 'Cys',
     'D': 'Asp',
     'E': 'Glu',
     'F': 'Phe',
     'G': 'Gly',
     'H': 'His',
     'I': 'Ile',
     'K': 'Lys',
     'L': 'Leu',
     'M': 'Met',
     'N': 'Asn',
     'P': 'Pro',
     'Q': 'Gln',
     'R': 'Arg',
     'S': 'Ser',
     'T': 'Thr',
     'V': 'Val',
     'W': 'Trp',
     'Y': 'Tyr'
}

def parseSparkyPeakList(peaklist_file):
    peaks = []
    with open(peaklist_file) as f:
        lines = f.readlines()[1:]
        f.close()
        for line in lines:
            
            l = line.strip().split()
            if '?' in l[0]:
                continue
            assignment = re.sub(r"([A-Z])([0-9]+)([A-Z])","\\1 \\2 \\3",l[0]).split()
            resname = assignment[0]
            resnumber = assignment[1]
            atoms = [assignment[2].split('-')[0], assignment[-1]]
            labels = [resnumber+res1to3dict[resname]+x[0] for x in  atoms]
            pos1 = l[1]
            pos2 = l[2]
            height = l[3]
            volume = l[4]
            peaks.append([labels[0], labels[1], pos1, pos2, height, volume])
    return peaks
            
def parseAnsigPeakList(peaklist_file):
    peaks = []
    dimension_count=2
    intensCol = 13*dimension_count
    specNameCol = intensCol+13
    assnColStart = 3*13+12+7*6
    lineWidth = None
    boxWidth = None
    fileObj = open(peaklist_file, 'rU')
    lines = fileObj.readlines()[2:]
    for line in lines:

        if line.strip().startswith('!'):
            continue  
        if line.strip().startswith('ANSIG'):
            continue

        height = float(line[intensCol:intensCol+13].strip() or '0') 
        volume = height
        details = line[specNameCol:specNameCol+12].strip()
        positions = [0] * dimension_count
        labels = [None] * dimension_count
        lineWidths = [None] * dimension_count
        boxWidths = [None] * dimension_count
        
        for dim in range(dimension_count):
    
          ppmCol = dim*13
          seqCol = assnColStart + (dim*4)
          resCol = assnColStart + (dimension_count*4) + (dim*4)
          atmCol = assnColStart + (dimension_count*8) + (dim*4)

          positions[dim] = float(line[ppmCol:ppmCol+13])
          res_number = line[seqCol:seqCol+4].strip() or '?'
          res_name = line[resCol:resCol+4].strip() or '?'
          atom = line[atmCol:atmCol+4].strip() or '?'
          labels[dim] = '%s%s%s' % (res_number, res_name, atom[0])
        if not '?' in labels:
            peaks.append([labels[0], labels[1], positions[0], positions[1], height, volume])
    return peaks


# In[182]:

import pprint
import os
fin = 'sparky.peaks'
pl_format = getPeakListFileFormat(fin)
if pl_format == 'SPARKY':
    peaks = parseSparkyPeakList(fin)
elif pl_format == 'ANSIG':
    peaks = parseAnsigPeakList(fin)
pprint.pprint(peaks)


# In[ ]:




# In[ ]:



