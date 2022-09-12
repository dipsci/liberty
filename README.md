## Liberty Metric Extraction

### installation
pip install libertymetric


### import package
from libertymetric.classLiberty import liberty as lutil


### load & convert CCS to JSON
lnode = lutil.read_lib('ccs.lib')
lutil.dump_json(lnode,out='ccs.json')
lnode.keys()


### load liberty from JSON
lnode = lutil.load_json('ccs.json')
lnode.keys()


### list cells in the liberary
[v for v in lnode['cell']]


### grab cell node by cell-name, e.g., 'ND2D1BWP'
cnode = lnode['cell']['ND2D1BWP']


### encapsulate all timing/power tables by timing-arc into a dataframe
lutT = lutil.get_cell_timing(cnode,todf=True)
lutP = lutil.get_cell_power(cnode,todf=True)
lutT.index # enumerate all lookup tables encapsulated by timing-arc
lutP.index # enumerate all lookup tables encapsulated by timing-arc


### lookup table interpolation, e.g., timing-arc ('A1,ZN,', 'combinational', 'cell_rise')
lut = lutT.loc[('A1,ZN,', 'combinational', 'cell_rise')]
y,x,v = map(np.array,lut.values()) # unpack values as numpy array


### timing interpolation based on the specified transition & load
lutil.table_lookup(lut,trans=0.0207,load=0.0010072,dflag=True)


### LS regression & prediction
lutil.lut2lsCoeff(lut1.to_dict(),trans=0.03,load=0.0017,dflag=True)


### visualization
lutil.plot_lut(lutT,keys=('A1,ZN,', 'combinational', 'cell_rise'))

