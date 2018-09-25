# -*- coding: utf-8 -*-

__author__ = 'http://zongming.net'


import os
import subprocess
import platform
from utils.disk import Disk
from utils.lvm import LVM


def get_input():

    # confirm
    confirm = None
    while confirm != "Y":
        confirm = input("The following operation may cause data loss. Y or N: ")
        if str(confirm) == "N":
            return False

    # disk
    name = input("Please enter the disk name you want to operate(like: xvda) : ")
    print('')
    path = "/dev/%s" % name

    if name and os.path.exists(str(path)):
        return path
    else:
        print("Error, '%s' does not exist." % name)
        return False


def main(sys, dev):

    # disk
    disk = Disk(dev)
    disk_parted = None
    disk_status = disk.get_info()

    if disk_status['free']:

        # extend
        if sys == 'Ubuntu':
            disk.resize_ext_part()

        else:
            # CentOS
            disk.create_ext_part()

        # logical
        logical_num = disk.create_lgi_part()

        # flag
        flag = disk.set_flag(logical_num)

        if flag:
            disk_parted = logical_num
            print("\033[0;31m%s\033[0m" % "Disk partition is complete. \n")

    # lvm
    lvm_status = None

    if disk_parted:

        partition = dev + str(disk_parted)
        lvm = LVM(partition)
        lvm_status = lvm.extend_lvm()

        if lvm_status:
            print("\033[0;31m%s\033[0m" % "The logical volume extension is complete. \n")

    # fileSystem
    if lvm_status:

        if sys == 'Ubuntu':
            result = subprocess.getstatusoutput("%s %s" % ("/sbin/resize2fs", lvm_status))
            print("%s return value: %s" % ("%s %s" % ("/sbin/resize2fs", lvm_status), result[0]))

        else:
            # CentOS
            result = subprocess.getstatusoutput("%s %s" % ("/usr/sbin/xfs_growfs", lvm_status))
            print("%s return value: %s" % ("%s %s" % ("/usr/sbin/xfs_growfs", lvm_status), result[0]))

        print("\033[0;31m%s\033[0m" % 'The root file system extension is complete.')


#
if __name__ == '__main__':

    dist = platform.dist()[0]
    device = get_input()

    if device:
        main(dist, device)
