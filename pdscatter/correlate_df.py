import numpy as np
###############################################################################
def valid_indices(df, *args):
    df_type = type(df[args[0]])
    validinds = df_type( np.ones(df.shape[0], dtype = bool), index = df.index )
    for aa in args:
        validinds &= ~df[aa].map(np.isnan) & ~df[aa].map(np.isinf)
    return validinds
 

class correlate_df():
    def __init__(self, df, aa, bb, output_valid= False):
        self.aa = aa
        self.bb = bb
        self.output_valid = output_valid
        "correlation"
        self.validinds = valid_indices(df, aa, bb)
        prsn = df[self.validinds][aa].corr(df[self.validinds][bb].astype('float64'), method='pearson')
        sprmn = df[aa].corr(df[bb], method='spearman')
        self.results = {'pearson': prsn, 'spearman':sprmn, 'N': len(df)}
        
        self.results['mean ' + aa] = df[self.validinds][aa].mean()
        self.results['median ' + aa] = df[aa].median()
        self.results['mean ' + bb] = df[self.validinds][bb].mean()
        self.results['median ' + bb] = df[bb].median()
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
        lenk = max([len(k) for k in keyorder]) + 1
        for k in keyorder:
            if type(self.results[k]) is int:
                formstr = '%u\n'
            else:
                formstr = '%4.4f\n'
            out_str += '%s: ' % k.ljust(lenk) + \
                        (formstr % self.results[k]).rjust(8)
        return out_str
