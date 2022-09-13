import sys
import subprocess

index = sys.argv[1]
process = subprocess.run(['atrm', str(int(index))], capture_output=True)

if str(process.stderr) == "b''":
    print('با موفقیت انجام شد!')
else:
    print('عدد اشتباه وارد شده است')
