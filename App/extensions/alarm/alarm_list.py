import subprocess
from pprint import pprint


def process():
    process = subprocess.Popen(['atq'], stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    stdout = str(stdout)
    if stdout == "b''":
        pprint('notihng')
    else:
        stdout = stdout.replace('\\t', ' ')
        stdout = stdout.replace('\\n', '\n')
        stdout = stdout.replace("b'", '')
        stdout = stdout.replace("'", '')
        stdout = stdout.strip()
        splits = stdout.split("\n")
        output = ""
        for split in splits:
            output += ' '.join(split.split()[0:5])
            output += '\n'
        output = output.strip()
        pprint(output)

process()