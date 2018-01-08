from current.fslibs.Peak import Peak
import platform
import re, os, csv


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

file_extenstions = ['peaks', 'xpk', 'out', 'csv']

def getPeakListFileFormat(filePath):

    fin = open(filePath, 'r')
    if len(filePath.split('.')) < 2:
        print('Invalid File Extension')
        return
    if filePath.split('.')[1] not in file_extenstions:
        print('Invalid File Extension')
        return
    for line in fin:
        if not line.strip():
            continue

        if (line.lstrip().startswith("Assignment") and "w1" in line) or line.startswith("<sparky save file>"):
            return "SPARKY"

        if line.lstrip().startswith("ANSIG") and "crosspeak" in line:
            return "ANSIG"

        if line.startswith('#') and "Number of dimensions" in line:
            return "XEASY"

        if line.startswith("DATA") and "X_AXIS" in line:
            return "NMRDRAW"

        if line.split()[0].isdigit() and line.split()[1].startswith('{'):
            return "NMRVIEW"

        if line.startswith("Number"):
            return "CCPN"

def parseAnsig(peaklist_file):
    """Parse a 2D peaklist in ANSIG format
       From ANSIG Manual:
       For 2D crosspeaks files the record has the format:
        FORMAT (3E13.6, A12, 7I6, 6A4)

        The values for each crosspeak are given in the following order:
        E13.6	Coordinates (F1, F2, ...)
        E13.6	Intensity
        A12	Spectrum name
        I6	Symmetry connection
        2I6	F1 connections (prev, next)
        2I6	F2 connections (prev, next)
            ... (further Fdim connections)
        2I6	Corresponding connections
        A4	Sequence assignments; F1, F2, ...
        A4	Residue assignemnts; F1, F2, ...
        A4	Nucleus assignments; F1, F2, ...

ANSIG v3.3 export crosspeaks file
   190     2
 1.307676E+02 8.772405E+00 8.272293E+05Trosy_highCo     0     0     0     0     0     0     023  23  Leu Leu N   HN
 1.301636E+02 8.656933E+00 4.936973E+05Trosy_highCo     0     0     0     0     0     0     0183 183 Ala Ala N   HN
 1.298941E+02 8.845919E+00 6.773006E+05Trosy_highCo     0     0     0     0     0     0     0282 282 Ala Ala N   HN
    """
    peakList = []

    # FarSeer-NMR only supports peaklists so dimension_count must equal 2
    dimension_count = 2

    # check a 2D peaklist has been parsed in

    first_two_lines = open(peaklist_file, 'rU').readlines()[:2]
    if first_two_lines[1][11] != '2':
        print("Peak list is not from a 2D spectrum")
        return

    # Each chemical shift is 13 characters wide and intensity always follows chemical shifts
    intensity_column_number = 13*dimension_count

    # assignment field occurs after 13 character intensity field, plus 12 character spectrum name field and seven 6
    # character symmetry and connection fields
    assignment_field_start_index = intensity_column_number+13+12+7*6
    fin = open(peaklist_file, 'rU')
    lines = fin.readlines()[2:]
    for ii, line in enumerate(lines):

        if line.strip().startswith('!'):
            continue
        if line.strip().startswith('ANSIG'):
            continue

        height = float(line[intensity_column_number:intensity_column_number+13].strip() or '0')
        volume = height
        peak_positions = [0] * dimension_count
        peak_labels = [None] * dimension_count
        line_widths = [None] * dimension_count
        atoms = [None] * dimension_count

        for dimension in range(dimension_count):

          shifts_field = dimension*13
          sequence_code_field = assignment_field_start_index + (dimension*4)
          residue_name_field = assignment_field_start_index + (dimension_count*4) + (dimension*4)
          atom_name_field = assignment_field_start_index + (dimension_count*8) + (dimension*4)

          peak_positions[dimension] = float(line[shifts_field:shifts_field+13])
          residue_number = line[sequence_code_field:sequence_code_field+4].strip() or '?'
          residue_name = line[residue_name_field:residue_name_field+4].strip() or '?'
          atom = line[atom_name_field:atom_name_field+4].strip() or '?'
          atoms[dimension] = atom[0]
          peak_labels[dimension] = '%s%s%s' % (residue_number, residue_name, atom[0])
        if not '?' in peak_labels:
            peak = Peak(peak_number=ii+1, positions=peak_positions, volume=volume, height=height,
                   assignments=peak_labels, linewidths=line_widths, atoms=atoms)

            peakList.append(peak)
    return peakList


def parseNmrDraw(peaklist_file):
    """Parse a 2D peaklist in NmrDraw format
REMARK

DATA  X_AXIS 1H           1  2048   12.685ppm   -3.277ppm
DATA  Y_AXIS 15N          1  1024  135.000ppm  103.035ppm

variables   INDEX X_AXIS Y_AXIS DX DY X_PPM Y_PPM X_HZ Y_HZ XW YW XW_HZ YW_HZ X1 X3 Y1 Y3 HEIGHT DHEIGHT VOL PCHI2 TYPE ASS CLUSTID MEMCNT TROUBLE
FORMAT %5d %9.3f %9.3f %6.3f %6.3f %8.3f %8.3f %9.3f %9.3f %7.3f %7.3f %8.3f %8.3f %4d %4d %4d %4d %13e %13e %13e %.5f %d %s %4d %4d %4d

    7   502.767   136.454  2.000  2.000    8.772  130.768  2351.453   259.152   7.349   9.187   34.372   17.448  501  503  135  137  1.008628e+05  0.000000e+00  8.272293e+05 0.00000 1 480.H;480.N    0    0    0
    9   517.575   155.785  2.000  2.000    8.657  130.164  2420.710   295.866   9.572  10.187   44.768   19.346  516  518  154  156  5.761750e+04  0.000000e+00  4.936973e+05 0.00000 1 640.H;640.N    0    0    0
   11   493.340   164.410  2.000  2.000    8.846  129.894  2307.361   312.246   6.402  10.046   29.940   19.080  492  494  163  165  8.121486e+04  0.000000e+00  6.773006e+05 0.00000 1 739.H;739.N    0    0    0
   19   518.456   203.628  2.000  2.000    8.650  128.669  2424.833   386.727   6.995   9.486   32.714   18.015  517  519  202  204  1.150421e+05  0.000000e+00  9.242484e+05 0.00000 1 508.H;508.N    0    0    0
   20   682.727   211.562  2.000  2.000    7.369  128.421  3193.130   401.797   7.168   9.734   33.525   18.487  681  683  210  212  1.136131e+05  0.000000e+00  9.425642e+05 0.00000 1 542.H;542.N    0    0    0
   21   567.806   215.211  2.000  2.000    8.265  128.307  2655.641   408.726   6.202   8.294   29.007   15.752  566  568  214  216  5.714155e+04  0.000000e+00  4.769788e+05 0.00000 1 494.H;494.N    0    0    0
   23   617.869   218.059  2.000  2.000    7.875  128.218  2889.787   414.136   3.580   7.180   16.742   13.637  616  618  217  219  2.160228e+06  0.000000e+00  1.713618e+07 0.00000 1 765.H;765.N    0    0    0
   26   509.184   222.297  2.000  2.000    8.722  128.085  2381.465   422.184   6.314   9.337   29.531   17.733  508  510  221  223  1.404175e+05  0.000000e+00  1.127275e+06 0.00000 1 510.H;510.N    0    0    0
   31   655.592   258.869  2.000  2.000    7.581  126.943  3066.220   491.641   5.359   8.513   25.065   16.167  654  656  257  259  7.345364e+04  0.000000e+00  5.971680e+05 0.00000 1 682.H;682.N    0    0    0

    Line starting VARS or variables contains contents of each column.
    """


    peakList = []
    isotopes = []
    fin = open(peaklist_file, 'r')
    dimension_count = 0

    # create a dictionary to store key:value pairs of column_label: column_index
    field_dictionary = {}

    for line in fin:
      line = line.strip()
      # ignore blank lines and lines starting with REMARK
      if not line:
        continue

      if line.startswith('REMARK'):
        continue

      data = line.split()
      # 
      if line.startswith('DATA'):
        dimension_count += 1
        isotopes.append(data[2])
        continue

      if line.startswith('VARS') or line.startswith('variables'):
        # populate field_dictionary with key:value pairs of column_label: column_index
        for i, key in enumerate(data[1:]):
            field_dictionary[key] = i

        continue

      elif not field_dictionary:
        continue

      elif not line[0].isdigit():
        continue

      ppms = [0] * dimension_count
      lineWidths = [None] * dimension_count
      dimension_labels = (('X_PPM','XW'), ('Y_PPM','YW'), ('Z_PPM','ZW'))

      height = float(data[field_dictionary['HEIGHT']])
      volume = float(data[field_dictionary['VOL']])
      annotations = data[field_dictionary['ASS']].split(';')
      atoms = [anno.split('.')[1] for anno in annotations if anno]
      for dimension in range(dimension_count):
        ppmKey, linewidthKey = dimension_labels[dimension]
        ppms[dimension] = float(data[field_dictionary[ppmKey]])
        lineWidths[dimension] = float(data[field_dictionary[linewidthKey]])

      peak = Peak(peak_number=data[0], assignments=annotations, atoms=atoms, height=height, volume=volume, positions=ppms,
                  linewidths=lineWidths)
      peakList.append(peak)

    fin.close()

    return peakList


def parseNmrView(peaklist_file):
      peakList = []
      fin = open(peaklist_file, 'rU')

      null = fin.readline()
      dimNames = fin.readline().strip().split()
      numDim = len(dimNames)
      name = fin.readline()
      line = fin.readline()
      line = line.replace('{', '')
      line = line.replace('}', '')

      line = fin.readline()
      line = line.replace('{', '')
      line = line.replace('}', '')
      headings = fin.readline().strip().split()
      dimHeadings = [x.split('.') for x in headings if '.' in x]
      dimHeadings = [x for x in dimHeadings if x[0] in dimNames]
      numFields = int(len(dimHeadings) / numDim)

      for line in fin:
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

      fin.close()

      return peakList


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
    fin = open(peaklist_file, 'rU')

    numDim = int(fin.readline().strip().split()[-1])
    lineWidth = None
    annotation_dict = parseProtFile(prot_file, seq_file)
    for line in fin:
      line = line.strip()

      if not line:
        continue

      atoms = []
      if line.startswith('#'):
        atoms.append(line.strip().split()[-1])
        continue
      data = line.split()

      if len(data) < 10:
          continue
      ppms = [0] * numDim
      annotations = [None] * numDim
      volume = float(data[numDim+3])
      height = None

      for dim in range(numDim):
        ppms[dim] = float(data[dim+1])
        if data[dim+9] != '0':
          annotations[dim] = annotation_dict[int(data[dim+9])]

      peak = Peak(peak_number=data[0], positions=ppms, assignments=annotations, atoms=atoms, linewidths=lineWidth, volume=volume,
                  height=height)
      peakList.append(peak)

    fin.close()

def parseCcpn(peaklist_file):
  fin = open(peaklist_file, 'rU')
  next(fin)
  peakList = []
  reader = csv.reader(fin)
  for row in reader:
      atoms = []
      for v in res1to3dict.values():
          if v in row[4]:
              a1 = row[4].strip().split(v)[-1]
              atoms.append(a1)
          if v in row[5]:
              a2 = row[5].strip().split(v)[-1]
              atoms.append(a2)
      peak = Peak(peak_number=row[1], positions=[row[2], row[3]], assignments=[row[4], row[5]], atoms=atoms, linewidths=[row[8], row[9]],
                  volume=row[7], height=row[6], fit_method=row[12], merit=row[10], volume_method=row[13], details=row[11])

      peakList.append(peak)

  fin.close()
  return peakList

def parseSparkyPeakList(peaklist_file):
  peakList = []
  with open(peaklist_file) as f:
      lines = f.readlines()[1:]
      f.close()
      for ii, line in enumerate(lines):
          l = line.strip().split()
          if len(l) < 4:
              continue
          if '?' in l[0]:
              continue
          assignment = re.sub(r"([A-Z])([0-9]+)([A-Z])","\\1 \\2 \\3",l[0]).split()
          resname = assignment[0]
          resnumber = assignment[1]
          atoms = [assignment[2].split('-')[0], assignment[-1]]
          annotations = [resnumber+res1to3dict[resname]+x[0] for x in atoms]
          lineWidths = [None] * 2
          ppms = [l[1], l[2]]
          height = l[3]
          volume = l[4]
          peak = Peak(peak_number=ii+1, positions=ppms, assignments=annotations, atoms=atoms, linewidths=lineWidths,
                      volume=volume, height=height)
          peakList.append(peak)

  return peakList

def fixpath(path):
  if path.startswith('/') and  platform.system() == "Windows":
      path = os.path.normpath(path[1:])
  else:
      path = os.path.normpath(os.path.expanduser(path))
  return path


def read_peaklist(fin, prot_file=None, seq_file=None):

  peaklist_file = fixpath(fin)
  file_format = getPeakListFileFormat(peaklist_file)
  print(fin)

  if file_format == 'ANSIG':
      return parseAnsig(peaklist_file)
  # elif file_format == 'CYANA':
  #     return parseXeasy(peaklist_file, prot_file, seq_file)
  elif file_format == 'NMRDRAW':
      return parseNmrDraw(peaklist_file)
  elif file_format == 'NMRVIEW':
      return parseNmrView(peaklist_file)
  elif file_format == 'SPARKY':
      return parseSparkyPeakList(peaklist_file)
  # elif file_format == 'XEASY':
  #     return parseXeasy(peaklist_file, prot_file, seq_file)
  elif file_format == 'CCPN':
      return parseCcpn(peaklist_file)

