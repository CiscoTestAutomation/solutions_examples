import os
from pyats.easypy import run
def main():
    test_path = os.path.dirname(os.path.abspath(__file__))
    testscript = os.path.join(test_path, 'pyats_android.py')
    run(testscript=testscript)