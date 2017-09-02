import os, csv

def create_directory_structure(spectrum_path, values_dict, peak_list_objects, peakLists):
    spectrum_dir = spectrum_path+'/spectra/'
    os.mkdir(spectrum_dir)
    for z_key in values_dict['z']:
        pls1 = [plo for plo in peak_list_objects if plo.z_cond == z_key]
        os.mkdir(os.path.join(spectrum_dir, z_key))
        for y_key in values_dict['y']:
            pls2 = [plo for plo in pls1 if plo.y_cond == y_key]
            os.mkdir(os.path.join(spectrum_dir, z_key, y_key))
            for x_key in values_dict['x']:
                pls3 = [plo for plo in pls2 if plo.x_cond == x_key]
                fout = open(os.path.join(spectrum_dir, z_key, y_key, "%s.csv" % x_key), 'w')
                write_peaklist_file(fout, peakLists[pls3[0].peak_list])
                fout.close()


def write_peaklist_file(fin, peak_list):
    writer = csv.writer(fin)
    header = ['Number', '#', 'Position F1', 'Position F2', 'Assign F1', 'Assign F2', 'Height', 'Volume',
              'Line Width F1 (Hz)', 'Line Width F2 (Hz)', 'Merit', 'Details', 'Fit Method', 'Vol. Method']
    writer.writerow(header)
    for ii, peak in enumerate(peak_list):
        writer.writerow([
            ii,
            peak.peak_number,
            peak.positions[0],
            peak.positions[1],
            peak.assignments[0],
            peak.assignments[1],
            peak.height,
            peak.volume,
            peak.linewidths[0],
            peak.linewidths[1],
            None,
            None,
            None,
            None
        ])

def list_all_files_in_path(path):
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames]
    return result