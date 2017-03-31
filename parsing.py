from current.fslibs.Peak import Peak

TYPE_DICT = {1:None, 2:'Random noise', 3:'Truncation artifact'}
DIM_KEYS = (('X_PPM','XW'), ('Y_PPM','YW'), ('Z_PPM','ZW'))

def parseAnsig(peaklist_file):
    pass

def parseCyana(peaklist_file, prot_file=None, assign_file=None):
    pass

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

        peakNum = int(checked[0])
        volume = float(volume)
        height = float(height)
        details = comment[1:-1].strip()

        ppms = [0] * numDim
        annotations = [None] * numDim
        lineWidths = [None] * numDim
        boxWidths = [None] * numDim

        if details == '?':
            details = None

        for i in range(numDim):
            j = 1 + i*numFields
            dimData = checked[j:j+numFields]
            anno, ppm, lineWidth, boxWidth, shape = dimData[:5]

            anno = anno[1:-1]
            if anno =='?':
                anno = None

            ppms[i] = float(ppm)
            lineWidths[i] = float(lineWidth)
            boxWidths[i] = float(boxWidth)
            annotations[i] = anno

            # peak = GeneralPeak(ppms, volume, height, details,
            #            annotations, lineWidths, boxWidths)
            #
            # peakList.append(peak)
        print(lineWidths)

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



  fileObj.close()


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
