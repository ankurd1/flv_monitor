#!/usr/bin/python

import subprocess
import sys
from threading import Timer
import time

last_filename = ""
last_filesize = 0
last_save_filesize = 0
last_time = 0
ewma_speed = 0

EWMA_A = 0.8
EWMA_B = 0.2

TIME_SLICE = 20
COPY_THRESH = 20 * 1024 * 1024
DEST_DIR = "/home/ankur/Videos/"

def print_on_same_line(string):
    sys.stdout.write("\r" + string)
    sys.stdout.flush()

def poll():
    global last_filename
    global last_filesize
    global last_save_filesize
    global TIME_SLICE
    global COPY_THRESH
    global last_time
    global ewma_speed
    global EWMA_A
    global EWMA_B

    p = subprocess.Popen('lsof | grep deleted | grep Flash', shell=True, stdout=subprocess.PIPE)
    p.wait()
    out = p.stdout.readline()
    time_difference = (time.time() - last_time)
    last_time = time.time()

    if (len(out) == 0):
        print "No file found! Exiting..."
        sys.exit()
    out_data = out.split()
    cur_filename = out_data[8]
    cur_filesize = int(out_data[6])

    if (len(last_filename) == 0):
        last_filename = cur_filename
    
    if (last_filename != cur_filename):
        print "File lost or a new file became the top result! Exiting..."
        sys.exit()

    data_transfered = cur_filesize - last_filesize
    last_filesize = cur_filesize

    #print "data trans=", data_transfered
    #print "time_difference=", time_difference
    speed = (data_transfered / time_difference) / 1024
    ewma_speed = speed * EWMA_A + ewma_speed * EWMA_B

    print_on_same_line(cur_filename + "\t" + str(cur_filesize / (1024 * 1024)) + "MiB done\t" + ("%.2f" % ewma_speed) + "KiB/s\t\t")

    if (data_transfered == 0):
        print "No data transfered in last slice! Exiting..."
        copy_file(out_data)
        sys.exit()

    if ((cur_filesize - last_save_filesize) > COPY_THRESH):
        copy_file(out_data)
        last_save_filesize = cur_filesize

    Timer(TIME_SLICE, poll).start()

def copy_file(out_data):
    #return
    #print "Copying..."
    pid = out_data[1]
    fd_num = out_data[3][:-1]
    file_name = out_data[8].split("/")[-1]

    p = subprocess.Popen('cp /proc/' + pid + '/fd/' + fd_num + " " + DEST_DIR + file_name, shell=True)
    p.wait()

poll()
