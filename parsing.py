from current.fslibs.Peak import Peak

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

TYPE_DICT = {1:None, 2:'Random noise', 3:'Truncation artifact'}
DIM_KEYS = (('X_PPM','XW'), ('Y_PPM','YW'), ('Z_PPM','ZW'))

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


def parseAnsig(peaklist_file):
    peakList = []
    dimension_count=2
    intensCol = 13*dimension_count
    specNameCol = intensCol+13
    assnColStart = 3*13+12+7*6
    lineWidth = None
    boxWidth = None
    fileObj = open(peaklist_file, 'rU')
    lines = fileObj.readlines()[2:]
    for ii, line in enumerate(lines):

        if line.strip().startswith('!'):
            continue
        if line.strip().startswith('ANSIG'):
            continue

        height = float(line[intensCol:intensCol+13].strip() or '0')
        volume = height
        positions = [0] * dimension_count
        annotations = [None] * dimension_count
        lineWidths = [None] * dimension_count
        atoms = [None] * dimension_count

        for dim in range(dimension_count):

          ppmCol = dim*13
          seqCol = assnColStart + (dim*4)
          resCol = assnColStart + (dimension_count*4) + (dim*4)
          atmCol = assnColStart + (dimension_count*8) + (dim*4)

          positions[dim] = float(line[ppmCol:ppmCol+13])
          res_number = line[seqCol:seqCol+4].strip() or '?'
          res_name = line[resCol:resCol+4].strip() or '?'
          atom = line[atmCol:atmCol+4].strip() or '?'
          atoms[dim] = atom[0]
          annotations[dim] = '%s%s%s' % (res_number, res_name, atom[0])
        if not '?' in annotations:
            peak = Peak(peak_number=ii+1, positions=positions, volume=volume, height=height,
                   assignments=annotations, linewidths=lineWidths, atoms=atoms)

            peakList.append(peak)
    return peakList


def parseNmrDraw(peaklist_file):
  peakList = []
  isotopes = []
  fileObj = open(peaklist_file, 'r')
  numDim = 0
  colDict = {}
  boxWidth = None # Could actually extract this

  for line in fileObj:
    line = line.strip()

    if not line:
      continue

    if line.startswith('REMARK'):
      continue

    data = line.split()
    if line.startswith('DATA'):
      numDim += 1
      isotopes.append(data[2])
      continue

    if line.startswith('VARS'):
      for i, key in enumerate(data[1:]):
        colDict[key] = i

      continue

    elif not colDict:
      continue

    elif not line[0].isdigit():
      continue

    ppms = [0] * numDim
    lineWidths = [None] * numDim
    boxWidths = [None] * numDim

    height = float(data[colDict['HEIGHT']])
    volume = float(data[colDict['VOL']])
    details = TYPE_DICT[int(float(data[colDict['TYPE']]))]
    annotations = data[colDict['ASS']].split(';')
    atoms = [anno.split('.')[1] for anno in annotations if anno]
    for dim in range(numDim):
      ppmKey, linewidthKey = DIM_KEYS[dim]
      ppms[dim] = float(data[colDict[ppmKey]])
      lineWidths[dim] = float(data[colDict[linewidthKey]])

    peak = Peak(peak_number=data[0], assignments=annotations, atoms=atoms, height=height, volume=volume, positions=ppms,
                linewidths=lineWidths)
    peakList.append(peak)

  fileObj.close()

  return peakList


def parseNmrView(peaklist_file):
    peakList = []
    fileObj = open(peaklist_file, 'rU')

    null = fileObj.readline()
    dimNames = fileObj.readline().strip().split()
    numDim = len(dimNames)

    name = fileObj.readline()
    line = fileObj.readline()
    line = line.replace('{', '')
    line = line.replace('}', '')
    sweepWidths = [float(x) for x in line.strip().split()]

    line = fileObj.readline()
    line = line.replace('{', '')
    line = line.replace('}', '')
    specFreqs = [float(x) for x in line.strip().split()]

    headings = fileObj.readline().strip().split()
    dimHeadings = [x.split('.') for x in headings if '.' in x]
    dimHeadings = [x for x in dimHeadings if x[0] in dimNames]
    numFields = int(len(dimHeadings) / numDim)

    for line in fileObj:
        fields = line.strip().split()
        checked = []

        while fields:
            val = fields.pop()

            if val[-1] == '}':
                while val[0] != '{':
                    val = fields.pop() + val

            checked.append(val)

        checked.reverse()

        j = 1 + numDim * numFields
        volume, height, status, comment = checked[j:j+4]

        if status == '-1':
          continue

        peak_number = int(checked[0])
        volume = float(volume)
        height = float(height)
        details = comment[1:-1].strip()

        ppms = [0] * numDim
        annotations = [None] * numDim
        lineWidths = [None] * numDim
        boxWidths = [None] * numDim
        atoms = [None] * numDim


        if details == '?':
            details = None

        for i in range(numDim):
            j = 1 + i*numFields
            dimData = checked[j:j+numFields]
            anno, ppm, lineWidth, boxWidth, shape = dimData[:5]

            anno = anno[1:-1]

            if anno =='?':
                anno = None
            if anno:
                atoms[i] = anno.split('.')[1]
            ppms[i] = float(ppm)
            lineWidths[i] = float(lineWidth)
            boxWidths[i] = float(boxWidth)
            annotations[i] = anno
        peak = Peak(peak_number=peak_number, positions=ppms, volume=volume, height=height,
                   assignments=annotations, linewidths=lineWidths, atoms=atoms)

        peakList.append(peak)

    fileObj.close()

  # return peakList, extraInfo


def parseProtFile(prot_file, seq_file):
    seq_dict = get_sequence_dict(seq_file)
    annotation_dict = {}
    lines = open(prot_file, 'r').readlines()

    for line in lines:
        l = line.strip().split()
        annotation_dict[int(l[0])] = l[-1]+seq_dict[int(l[-1])]+l[-2]
    return annotation_dict

def get_sequence_dict(seq_file, first_residue=1):

    seq_dict = {}
    lines = open(seq_file, 'r').readlines()

    for ii, line in enumerate(lines):
        l = line.strip().split()
        seq_dict[ii+first_residue] = l[0].title()
    return seq_dict


def parseXeasy(peaklist_file, prot_file, seq_file):
  peakList = []
  fileObj = open(peaklist_file, 'rU')

  numDim = int(fileObj.readline().strip().split()[-1])

  lineWidth = None
  boxWidth = None
  anno = '?'
  annotation_dict = parseProtFile(prot_file, seq_file)
  for line in fileObj:
    line = line.strip()

    if not line:
      continue

    atoms = []
    if line.startswith('#'):
      atoms.append(line.strip().split()[-1])

    data = line.split()
    ppms = [0] * numDim
    annotations = [None] * numDim
    lineWidths = [None] * numDim
    boxWidths = [None] * numDim

    volume = float(data[numDim+3])
    height = None
    details = None

    for dim in range(numDim):
      ppms[dim] = float(data[dim+1])
      if data[dim+9] != '0':
        annotations[dim] = annotation_dict[int(data[dim+9])]

    peak = Peak(peak_number=data[0], positions=ppms, assignments=annotations, atoms=atoms, linewidths=lineWidth, volume=volume,
                height=height)
    peakList.append(peak)

  fileObj.close()


def parseSparkyPeakList(peaklist_file):
    peakList = []
    with open(peaklist_file) as f:
        lines = f.readlines()[1:]
        f.close()
        for ii, line in enumerate(lines):

            l = line.strip().split()
            if '?' in l[0]:
                continue
            assignment = re.sub(r"([A-Z])([0-9]+)([A-Z])","\\1 \\2 \\3",l[0]).split()
            resname = assignment[0]
            resnumber = assignment[1]
            atoms = [assignment[2].split('-')[0], assignment[-1]]
            annotations = [resnumber+res1to3dict[resname]+x[0] for x in  atoms]
            lineWidths = [None] * 2
            ppms = [l[1], l[2]]
            height = l[3]
            volume = l[4]
            peak = Peak(peak_number=ii+1, positions=ppms, assignments=annotations, atoms=atoms, linewidths=lineWidths, volume=volume,
                height=height)
            peakList.append(peak)

    return peakList

def test_xeasy():
    prot_file = 'cyana.prot'
    seq_file = 'cyana.seq'
    peaks = 'cyana.peaks'
    parseXeasy(peaks, prot_file, seq_file)

def test_nmrview():
    peaks = 'nmrview.xpk'
    parseNmrView(peaks)

def test_nmrdraw():
    peaks = 'nmrdraw.peaks'
    peaklist = parseNmrDraw(peaks)
    i=0
    for line in open(peaks, 'r').readlines()  :
        l = line.strip()
        if l:
            if l[0].isdigit():
                i+=1

    print(len(peaklist) == i)

def test_ansig():
    peaks = 'ansig.peaks'
    parseAnsig(peaks)

