#! /usr/local/bin/python
#
#  This script is an improved version of the 'qstat' command 
#   that prints out only USEFUL information (like the job's
#   FULL name) in a readable way.
#
#  To run from any directory, just use do type
#
#  python /casa/benw/scripts/bstat.py
#
#
#  All of the output of qstat -f is captured and organized,
#   so it would be very easy to print out additional info 
#   by copying this file into your own directory and 
#   modifying the last loop of the script. 
#

import subprocess

# get user name
user = subprocess.check_output(['whoami']).strip()
# get all jobs data
out = subprocess.check_output(['qstat','-f'])
lines = out.split('\n')

# build list of jobs, each job is a dictionary
jobs = []
for line in lines:
    if "Job Id:" in line:  # new job
        job = {}
        s = line.split(":")
        job_id = s[1].split('.')[0].strip()
        job[s[0].strip()] = job_id
    if '=' in line:
        s = line.split("=")
        job[s[0].strip()] = s[1].strip()
    elif line == '':
        jobs.append(job)

# print out useful information about user's jobs
print "\n   " + user + "'s jobs:\n"
for job in jobs:
    if job['Job_Owner'].split('@')[0] == user:        
        print "   " +  job['Job_Name']
        print "   Id: " + job['Job Id']
        if 'resources_used.walltime' in job.keys():
            print "   Wall time: " + job['resources_used.walltime']
        print "   State: " + job['job_state']
        print
