import numpy as np
###############################################################################
class correlate_df():
    def __init__(self, df_sites, aa, bb, output_valid= False):
        self.aa = aa
        self.bb = bb
        self.output_valid = output_valid
        "correlation"
        self.validinds = ~df_sites[aa].map(np.isnan) & ~df_sites[aa].map(np.isinf) & \
            ~df_sites[bb].map(np.isnan) & ~df_sites[bb].map(np.isinf)
        prsn = df_sites[self.validinds][aa].corr(df_sites[self.validinds][bb].astype('float64'), method='pearson')
        sprmn = df_sites[aa].corr(df_sites[bb], method='spearman')
        self.results = {'pearson': prsn, 'spearman':sprmn, 'N': len(df_sites)}
        
        self.results['mean ' + aa] = df_sites[self.validinds][aa].mean()
        self.results['median ' + aa] = df_sites[aa].median()
        self.results['mean ' + bb] = df_sites[self.validinds][bb].mean()
        self.results['median ' + bb] = df_sites[bb].median()
    def __call__(self, output_valid = False):
        if output_valid:
            return self.results, self.validinds
        else:
            return self.results
    def __repr__(self):
        keyorder = [ 'median ' + self.aa, 'mean ' +self.aa ,
                     'median ' + self.bb, 'mean ' + self.bb,
                     'N', 'pearson', 'spearman']
        out_str = ''
        for k in keyorder:
            if type(self.results[k]) is int:
                out_str += '%s:\t%u\n' % (k, self.results[k])
            else:
                out_str += '%s:\t%4.4f\n' % (k, self.results[k])
        return out_str
