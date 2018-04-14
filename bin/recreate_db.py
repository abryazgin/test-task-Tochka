#!/usr/bin/env python
import os
import sys
rootdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

sys.path.append(os.path.join(rootdir, 'src'))


from main import db
db.create_all()
