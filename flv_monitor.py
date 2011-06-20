#!/usr/bin/python
#
# flv_monitor
# Monitors the system for any flash videos that you are watching on your
# browser. Displays the speed and periodically copies them to a more
# 'suitable' directory.
#
# Author: Ankur Dahiya <legalos.LOTR@gmail.com>
#
# You can get the latest version of this script from
# https://github.com/legalosLOTR/flv_monitor

import subprocess
import sys
from threading import Timer
import time

EWMA_A = 0.8
EWMA_B = 0.2

TIME_SLICE = 20
COPY_THRESH = 20 * 1024 * 1024
DEST_DIR = "/home/ankur/Videos/"

def print_on_same_line(string):
    sys.stdout.write("\r" + string)
    sys.stdout.flush()

class flv_video():
    file_name = ""
    last_size = 0
    last_save_size = 0
    last_time = 0
    ewma_speed = 0

def poll():
    global EWMA_A
    global EWMA_B
    global TIME_SLICE
    global COPY_THRESH

    fileHash = {}
    while True:
        p = subprocess.Popen('lsof | grep deleted | grep /tmp/Flash', shell=True, stdout=subprocess.PIPE)
        p.wait()
        found_file = False
        
        for line in p.stdout:
            found_file = True
            file_data = line.split()
            file_name = file_data[8]
            
            if (file_name not in fileHash):
                flv = flv_video()
                flv.file_name = file_data[8]
                fileHash[file_name] = flv
            else:
                flv = fileHash[file_data[8]]

            cur_size = int(file_data[6])
            data_transfered = cur_size - flv.last_size
            time_difference = time.time() - flv.last_time
            flv.last_time = time.time()
            
            speed = (data_transfered / time_difference) / 1024
            flv.ewma_speed = speed * EWMA_A + flv.ewma_speed * EWMA_B

            print flv.file_name + "\t" + str(cur_size / \
                (1024 * 1024)) + "MiB done\t" + ("%.2f" % flv.ewma_speed) \
                + "KiB/s\t\t"

            if ((cur_size - flv.last_save_size) > COPY_THRESH):
                copy_file(file_data)
                flv.last_save_size = cur_size
        
            flv.last_size = cur_size

        if (not found_file):
            print "No files found! Exiting..."

        print ""
        time.sleep(TIME_SLICE)

def copy_file(out_data):
    #return
    #print "Copying..."
    pid = out_data[1]
    fd_num = out_data[3][:-1]
    file_name = out_data[8].split("/")[-1]

    p = subprocess.Popen('cp /proc/' + pid + '/fd/' + fd_num + " " + DEST_DIR + file_name, shell=True)
    p.wait()

if (__name__ == "__main__"):
    poll()
