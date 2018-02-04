class Peak(object):

    def __init__(self, peak_number, positions, assignments, linewidths, height, volume, atoms,
                 fit_method=None, merit=None,
                 volume_method=None, details=None):

        self.peak_number = peak_number
        self.positions = positions
        self.assignments = assignments
        self.atoms = atoms
        self.linewidths = linewidths
        self.height = height
        self.volume = volume
        self.fit_method = fit_method
        self.merit = merit
        self.volume_method = volume_method
        self.details = details
        

