#!/usr/bin/env python

""" MultiQC submodule to parse output from edgeR MDS plot data
generated by the NGI-RNAseq best practice analysis pipeline
https://github.com/SciLifeLab/NGI-RNAseq/ """

import logging
from multiqc.plots import scatter


# Initialise the logger
log = logging.getLogger('multiqc.modules.ngi_rnaseq')


def parse_reports(self):
    """ Find bamtools stats reports and parse their data """

    # Set up vars
    self.mds_plot_data = dict()

    # Go through files and parse data using regexes
    found_mds_plot = False
    data = {}
    for f in self.find_log_files('ngi_rnaseq/mds_plot'):
        xTitle = None
        yTitle = None
        # Parse the file
        for l in f['f'].splitlines():
            s = l.split()
            if xTitle is None:
                xTitle = s[0]
                yTitle = s[1]
            else:
                data[s[0]] = [{'x': float(s[1]), 'y': float(s[2])}]
        # Should only have one MDS plot per report
        if found_mds_plot:
            log.warning("Found duplicate MDS plots! Overwriting: {}".format(f['s_name']))
        found_mds_plot = True
        self.add_data_source(f, section='mds_plot')

    if found_mds_plot:
        pconfig = {
            'title': 'MDS Plot',
            'xlab': xTitle,
            'ylab': yTitle
        }
        self.add_section(
            name = 'MDS Plot',
            anchor = 'ngi_rnaseq-mds_plot',
            description = '''Multidimensional scaling (MDS) show relatedness between samples in a project.
            These values are calculated using <a href="https://bioconductor.org/packages/release/bioc/html/edgeR.html">edgeR</a>
            in the <a href="https://github.com/SciLifeLab/NGI-RNAseq/blob/master/bin/edgeR_heatmap_MDS.r"><code>edgeR_heatmap_MDS.r</code></a> script.''',
            plot = scatter.plot(data, pconfig)
        )

    # Return number of samples found
    return 1 if found_mds_plot else 0

