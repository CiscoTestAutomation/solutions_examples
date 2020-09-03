import os

from genie.harness.main import gRun
from pyats.datastructures.logic import Or

def main():
    datafile_path = os.path.dirname(os.path.abspath(__file__))
    datafile_path += '/datafiles'

    gRun(trigger_datafile=datafile_path+'/trigger_datafile.yaml',
         subsection_datafile=datafile_path+'/subsection_datafile.yaml',
         trigger_uids=Or(''))