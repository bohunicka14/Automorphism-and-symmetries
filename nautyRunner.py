import os
import subprocess
import time

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
    runs = 0
    while runs < 10:
        try:
            stream = os.popen('grep -o "grpsize=[0-9,\.]*" ./nauty26r12/myoutput.txt | grep -o [0-9,\.]*')
            result = stream.read()
            if '.' in str(result):
                grp_size = 0
            else:
                grp_size = int(result)
            break
        except ValueError:
            print(open('./nauty26r12/myoutput.txt', 'r').read())
            time.sleep(1)
        runs += 1

    stream = os.popen('grep "([0-9]* [0-9]*)" ./nauty26r12/myoutput.txt')
    grp = str(stream.read())
    stream.close()
    return grp_size, grp

def nauty_get_aut_group_size():
    run_nauty()
    stream = os.popen('grep -o "grpsize=[0-9,\.]*" ./nauty26r12/myoutput.txt | grep -o [0-9,\.]*')
    result = stream.read()
    if '.' in str(result):
        return_value = 0
    else:
        return_value = int(result)

    stream.close()
    return return_value

def nauty_get_aut_group():
    run_nauty()
    stream = os.popen('grep "([0-9]* [0-9]*)" ./nauty26r12/myoutput.txt')
    return_value = str(stream.read())
    stream.close()
    return return_value

