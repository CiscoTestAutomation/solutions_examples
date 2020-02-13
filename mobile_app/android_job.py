import os
def main(runtime):
    test_path = os.path.dirname(os.path.abspath(__file__))
    testscript = os.path.join(test_path, 'pyats_android.py')
    runtime.tasks.run(testscript=testscript)