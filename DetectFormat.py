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
    if min([ord(c) for c in testData]) < 32:
        return

    fileObj = open(filePath, 'rU')

    for line in fileObj:
        if not line.strip():
            continue

        if SPARKY_SAVE_PATTERN.search(line):
            print("SPARKY")

        if NMRSTAR_PATTERN.search(line):
            print("NMRSTAR")

        if ANSIG_PATTERN.search(line):
            print("ANSIG")

        if XEASY_PATTERN.search(line):
            print("XEASY")

        if NMRDRAW_PATTERN.search(line):
            print("NMRDRAW")

        if NMRVIEW_PATTERN.search(line):
            print("NMRVIEW")

        if SPARKY_PATTERN.search(line):
            print("SPARKY")

        if AUTOASSIGN_PATTERN.search(line):
            print("AUTOASSIGN")

