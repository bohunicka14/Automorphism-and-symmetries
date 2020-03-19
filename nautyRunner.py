import os
import subprocess

def run():
    nauty = subprocess.Popen(["./nauty26r12/dreadnaut"],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           universal_newlines=True,
                           bufsize=0)

    nauty.stdin.write(">./nauty26r12/myoutput.txt <./nauty26r12/mygraph.dre x ->\n")
    nauty.stdin.write("q\n")
    nauty.stdin.close()

    stream = os.popen('grep -o "grpsize=[0-9]*" ./nauty26r12/myoutput.txt | grep -o [0-9]*')
    return int(stream.read())


