## Liberty Metric Extraction

### installation
pip install libertymetric

### import package
from classLiberty import liberty as lutil

### load & convert CCS to JSON
lnode = lutil.read_lib('ccs.lib')
lutil.dump_json(lnode,out='ccs.json')
lnode.keys()

### load liberty from JSON
lnode = lutil.load_json('ccs.json')
lnode.keys()

