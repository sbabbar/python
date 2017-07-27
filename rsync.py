#!/usr/bin/python
# sbabbar
import os
import sys
import subprocess
import argparse
import time

# argv[1] Input filename with hostname,source,destination
# argv[2] run option

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", dest="inp",
        help="enter filename with comma separated hostname,source,destination", metavar="INPUT_FILE")
parser.add_argument("-r", "--run", dest="opt",
        help="Runs rsync if -r|--run=yes , runs dryrun if -r|--run=no , runs dryrun if -r|--run option not specified", metavar="yes|no")

date = (time.strftime("%m_%d_%Y_%H%M"))

args = parser.parse_args()
if len(sys.argv) < 3 or len(sys.argv) > 5:
    parser.print_help()
    parser.exit(0)

file_inp = []
file_inp_fd = open(args.inp)

for line in file_inp_fd.readlines():
    cleaned_line = line.strip()
    fields = cleaned_line.split(',')
    host, source, destination = fields
    print host
    print '-' * 20
    if len(sys.argv) == 3:
       rsync_cmd = 'rsync -avrznHS -e \'ssh -qxa\' --stats --progress ' + source + ' ' +  host  + ':' + destination
       print rsync_cmd 
    elif len(sys.argv) == 5 and args.opt == 'yes':
       rsync_cmd = 'rsync -avrzHS -e \'ssh -qxa\' --stats --progress ' + source + ' ' +  host  + ':' + destination
       print rsync_cmd
    elif len(sys.argv) == 5 and args.opt == 'no':
       rsync_cmd = 'rsync -avrznHS -e \'ssh -qxa\' --stats --progress ' + source + ' ' +  host  + ':' + destination
       print rsync_cmd
    else:
       parser.print_help()
       parser.exit(0)
    out_file = ('/tmp/' + host + '_rsyncLog_' + date + '.out')
    err_file = ('/tmp/' + host + '_rsyncLog_' + date + '.err') 
    with open(out_file,"wb") as out, open(err_file,"wb") as err:   
      pr = subprocess.Popen(rsync_cmd, shell=True, stdout=out, stderr=err)
      pr.wait()
      print 'Verify output file:', out_file
      print 'Verify Error file:', err_file, "\n"
