class Peak(object):

    def __init__(self, peak_number, positions, assignments, linewidths, height, volume, atoms, **extra_info):

        self.peak_number = peak_number
        self.positions = positions
        self.assignments = assignments
        self.atoms = atoms
        self.linewidths = linewidths
        self.height = height
        self.volume = volume

