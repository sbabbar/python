"Grab status from the netstat command."

import subprocess


def get_established_connections():
    "Invoke the netstat command and return all live connections."

    output = subprocess.check_output("netstat -n", shell=True)

    lines = output.splitlines()

    matching_lines = []
    for line in lines:
        if line.endswith("ESTABLISHED"):
            matching_lines.append(line)
            print line

get_established_connections()
