from _config_section import ConfigSection

import os
REAL_PATH = os.path.dirname(os.path.realpath(__file__))

data = ConfigSection("data")
data.dir = "%s/%s" % (REAL_PATH, "data")

clones = ConfigSection("clones")
clones.dir = "%s/%s" % (REAL_PATH, "clones")

splits = ConfigSection("splits")
splits.dir = "%s/%s" % (REAL_PATH, "splits")

extract = ConfigSection("extract")
extract.dir = "%s/%s" % (REAL_PATH, "extract")

split_config = {
    'folders':{
        'Q1':['CircuitApp.java', 'CircuitApp', 'CircuitApp.class', 'data.txt'],
        'Q2':['SpellChecker.java', 'SpellChecker', 'SpellChecker.class', 'bonk.txt', 'dictionary.txt'],
        'Q3':['Course.java', 'Course', 'Course.class', 'Student.java', 'Student', 'Student.class','Department.java', 'Department', 'Department.class','TestApp.java', 'TestApp', 'TestApp.class']
    }
}

extract_config = {
    'file_types':['.java', '.txt', '.md']
}