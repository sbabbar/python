"Get top CPU Mem Consuming process"

import subprocess


def get_top_cpumem():
    "Invoke the ps command and get the top cpu mem process"

    #output = subprocess.check_output("ps aux | sort -nrk 3,3 | head -n 5", shell=True)
    output = subprocess.check_output("ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head", shell=True)

    lines = output.splitlines()

    for line in lines:
            print line

get_top_cpumem()
