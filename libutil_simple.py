from libertymetric.classLiberty import liberty as lutil

LIB = <CCS liberty>
JSON = <target json>

#%% load & convert CCS to JSON
lnode = lutil.read_lib(LIB)
lutil.dump_json(lnode,out=JSON)
lnode.keys()

# load liberty from JSON
lnode = lutil.load_json(JSON)
lnode.keys()

#%% understand the liberty format
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# most commonly used configuration for data visualization (optional)
pd.set_option('expand_frame_repr', False)
pd.set_option('precision',5)
plt.rcParams.update({'font.family': 'monospace'})
mrkL = ['o','v','^','<','>','d','s','h','H','p','*','D','+','x']
colL = list(plt.matplotlib.colors.TABLEAU_COLORS)+['k'] # 11 colors

#%% load liberty from JSON 
lnode = lutil.load_json(JSON)

lnode.keys() # items described in the library scope; press TAB
[v for v in lnode['cell']]

lnode['library'] # library name

P,V,T = lnode['nom_process'],lnode['nom_temperature'],lnode['nom_voltage'] # library PVT

cellL = lnode['cell'].keys() # cells included in this library scope

cnode = lnode['cell']['NAND2V1_T10UL_1'] # grab cell node with hash key

cnode.keys() # items described in the cell scope; press TAB

cnode['name'] # cell name

area,fp,leak = cnode['area'],cnode['cell_footprint'],cnode['cell_leakage_power'] # cell area/footprint/leakage

cnode['leakage_power'] # cell conditional leakage power

pinL = cnode['pin'].keys() # pins included in this cell scope; press TAB

inode = cnode['pin']['ZN'] # grab pin node with hash key

inode.keys() # items described in the pin scope; press TAB

inode['name'] # pin name

tnodeL = inode['timing'] # list of timing table
[v['related_pin'] for v in tnodeL]

tnode = tnodeL[0] # the 1st timing node, A1->ZN

tnode.keys() # items described in the timing scope; press TAB

rpin,tsense,ttype = tnode['related_pin'],tnode['timing_sense'],tnode['timing_type']

y,x,cfall = tnode['cell_fall'].values() # delay fall lookup-table

y,x,cfall = map(np.array,tnode['cell_fall'].values()) # map to numpy array
d = pd.DataFrame(cfall.reshape(len(y),len(x)),columns=x,index=y)

y,x,tfall = map(np.array,tnode['fall_transition'].values()) # transition fall lookup-table
d = pd.DataFrame(tfall.reshape(len(y),len(x)),columns=x,index=y)

#%% check timing & power tables
lnode = lutil.load_json(JSON)
[v for v in lnode['cell']]

cnode = lnode['cell']['NAND2D1']

#%% leakage table
lutL = cnode['leakage_power']
[v for v in lutL] # all timing lookup tables
[v for v in lutL if v['related_pg_pin']=='VDD']

##########################################################################################
#%% query timing delay table with API
# encapsulate tables indexed by arc and timing type
lutT = lutil.get_cell_timing(cnode) # query all timing tables 
[v for v in lutT]

lutT = lutil.get_cell_timing(cnode,ctype='cell_rise') # query rise delay 
[v for v in lutT]
y,x,v = lutT[('A1,ZN,', 'combinational', 'cell_rise')].values() # unpack lut

lutT = lutil.get_cell_timing(cnode,ctype='cell_fall')
[v for v in lutT]
y,x,v = lutT[('A1,ZN,', 'combinational', 'cell_fall')].values()

# encapsulate timing table into dataframe
dt = lutil.get_cell_timing(cnode,todf=True) # query all timing tables 
print(dt)
print(dt.index)

# grab lut with key values 
lut = dt.loc[('A1,ZN,','combinational','cell_rise')]
y,x,v = dt.loc[('A1,ZN,','combinational','cell_rise')] # unpack lut

# convert to Pandas
d = lutil.lut2df(lut.to_dict())

#%% inetrnal power table
lutP = lutil.get_cell_power(cnode) # query all power tables
[v for v in lutP]
y,v = lutP[(',A1,!A2', 'fall_power')].values() # unpack lut 2D

lutP = lutil.get_cell_power(cnode,ctype='rise_power') # query rise power
[v for v in lutP]

# unpack lut 3D
y,x,v = lutP[('A1,ZN,A2', 'rise_power')].values() # rise power lookup table, when A2==1
y,x,v = lutP[('A2,ZN,A1', 'rise_power')].values() # rise power lookup table, when A1==1

# encapsulate power table into dataframe
dp = lutil.get_cell_power(cnode,todf=True) # query all power tables
print(dp)
print(dp.index)

# grab lut with key values 
lut = dp.loc[('A1,ZN,A2', 'fall_power')]
y,x,v = dp.loc[('A1,ZN,A2', 'fall_power')] # unpack lut

# convert to Pandas
d = lutil.lut2df(lut)

#%%
lutil.lookup_cell_pincap(cnode,dflag=True)
lutil.lookup_cell_leakage(cnode,dflag=True)


##########################################################################################
#%% grab timing tables encapsulated in a dictionary form
lutT = lutil.get_cell_timing(cnode)
[v for v in lutT]

# decapsulate lookup table (as a dictionary)
lut = lutT[('A1,ZN,', 'combinational', 'cell_rise')]
y,x,v = map(np.array,lut.values()) # unpack values as numpy array

# timing interpolation based on the specified transition & load
lutil.table_lookup(lut,trans=0.0207,load=0.0010072,dflag=True)

# convert lut into dataframe
d1 = lutil.lut2df(lutT[('A1,ZN,', 'combinational', 'cell_rise')])
d2 = lutil.lut2df(lutT[('A2,ZN,', 'combinational', 'cell_rise')])

# timing operation
(d1+d2)/2 # average A1->ZN and A2->ZN delay
d1*1.02 # increase 2% margin
d2*0.98 # decrease 2% margin

#%% metric API
lutil.lookup_cell_pincap(cnode,dflag=True)
lutil.lookup_cell_leakage(cnode,dflag=True)

cr = lutil.lookup_cell_timing(cnode,ctype='cell_rise',trans=0.0207,load=0.0010072,dflag=True)
cf = lutil.lookup_cell_timing(cnode,ctype='cell_fall',trans=0.0207,load=0.0010072,dflag=True)
(cr+cf)/2

pr,pi,po = lutil.lookup_cell_power(cnode,ctype='rise_power',trans=0.02,load=0.001,dflag=True)
pf,pi,po = lutil.lookup_cell_power(cnode,ctype='fall_power',trans=0.02,load=0.001,dflag=True)
(pr+pf)/2

dt = lutil.get_cell_timing(cnode,todf=True)
lut1 = dt.loc[('A1,ZN,', 'combinational', 'cell_rise')]
lut2 = dt.loc[('A1,ZN,', 'combinational', 'cell_fall')]
lutil.lut2lsCoeff(lut1.to_dict(),trans=0.03,load=0.0017,dflag=True)
lutil.lut2lsCoeff(lut2.to_dict(),trans=0.03,load=0.0017,dflag=True)

#%% visualization
cnode = lnode['cell']['DFFD1']
lutT = lutil.get_cell_timing(cnode)
[v for v in lutT]

# cell delay
lutil.plot_lut(lutT,keys=('CK,Q,', 'rising_edge', 'cell_rise'))

# constraint
keyC = [('CK,D,','hold_rising', 'rise_constraint'),
        ('CK,D,','setup_rising','rise_constraint')]
lutil.plot_lut(lutT,keys=keyC,xylabel=('clock','data'))

lutil.plot_cell_constraint(cnode,arc='CK,D',ctype='rise_constraint')

