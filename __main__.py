import sys

from util.easy_extract import EasyExtract

args = sys.argv[1:]
if len(args) >= 2:
    proj_dir = args[0]
    extract_functions = args[1]
else:
    proj_dir = input("input project directory:")
    extract_functions = input('input extract functions(split by ","):').split(',')

ee = EasyExtract(proj_dir)
print(ee.export(extract_functions))
