import sys
import subprocess

index = sys.argv[1]
process = subprocess.run(['atrm', str(int(index))], capture_output=True)

if str(process.stderr) == "b''":
    print("successfully done!")
else:
    print("Wrong index is entered")