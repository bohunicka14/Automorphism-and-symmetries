import os
import subprocess

def run_nauty():
    nauty = subprocess.Popen(["./nauty26r12/dreadnaut"],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True,
                             bufsize=0)

    nauty.stdin.write(">./nauty26r12/myoutput.txt <./nauty26r12/mygraph.dre x ->\n")
    nauty.stdin.write("q\n")
    nauty.stdin.close()

def nauty_dre_to_dot(path):
    os.popen('./nauty26r12/dretodot ./nauty26r12/mygraph.dre {}'.format(path))

def nauty_get_automorphism_group_info():
    '''
    :return: Tuple (group size, group)
    '''
    run_nauty()
    stream = os.popen('grep -o "grpsize=[0-9]*" ./nauty26r12/myoutput.txt | grep -o [0-9]*')
    grp_size = int(stream.read())
    stream = os.popen('grep -o "([0-9]* [0-9]*)" ./nauty26r12/myoutput.txt')
    grp = str(stream.read())
    stream.close()
    return grp_size, grp

def nauty_get_aut_group_size():
    run_nauty()
    stream = os.popen('grep -o "grpsize=[0-9]*" ./nauty26r12/myoutput.txt | grep -o [0-9]*')
    return_value = int(stream.read())
    stream.close()
    return return_value

def nauty_get_aut_group():
    run_nauty()
    stream = os.popen('grep -o "([0-9]* [0-9]*)" ./nauty26r12/myoutput.txt')
    return_value = str(stream.read())
    stream.close()
    return return_value

