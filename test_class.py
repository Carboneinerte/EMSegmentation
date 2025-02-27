import pandas as pd

df = pd.read_csv('csv/Dendite_test.csv', )
df = df.dropna(axis = 'columns', how = 'all')


class Dendrites():
    def __init__(self, df):
        self.df = df
    
    def length_um(self):
        self.df['total_length_um'] = self.df['total_length_nm'] / 1000
        return self.df['total_length_um']

    def syn_frq(self):
        self.df['syn_frq'] = self.df['nb of synapses'] / self.df['total_length_nm']
        return self.df['syn_frq']
    
    def other_syn(self, syntype):
        if 'total_length_um' not in df.columns:
            syn_frq()

        self.df[f'frq_{syntype}'] = self.df[syntype] / self.df['total_length_um']
        return self.df[f'frq_{syntype}']
        
    def group_age(self):
        def_age = df.groupby('sample')
        return def_age
    
debd = Dendrites(df)

# debd.syn_frq()
debd.length_um()
debd.other_syn('adcs')
def_age = debd.group_age()
print(df.head())
print(def_age.head())