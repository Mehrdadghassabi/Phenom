import subprocess as sp
import sys

output = sp.getoutput("apt-cache show {}".format(sys.argv[1]))
if output == 'E: No packages found':
    print('your package because of errors is not installed')
else:
    print("your package is installed")
