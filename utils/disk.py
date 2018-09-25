# -*- coding: utf-8 -*-

__author__ = 'http://zongming.net'

import re
import subprocess


# Disk 
class Disk(object):

    def __init__(self, dev):

        # init
        self.disk = dev
        self.parted = "/sbin/parted"

    # partition
    def get_info(self, flag=False):

        # centos {'free': ('10.7', '75.2', '64.4'), 'extended': False, 'logical': False}
        # ubuntu {'free': ('10.7', '85.9', '75.2'), 'logical': ('5', 'logical', '                lvm'),
        # 'extended': ('2', 'extended')}

        status, out = subprocess.getstatusoutput('%s %s print free' % (self.parted, self.disk))

        string = str(out)
        free = re.search(r'[ ]*(.*?)GB[ ]*(.*?)GB[ ]*(.*?)GB[ ]*Free Space', string)
        ext = re.search(r"[ ](\d+).*?(extended)", string)
        lgi = re.findall(r"[ ](\d+).*?(logical).*?(.*)[ ]?", string)

        result = dict()
        result['free'] = free.groups() if free else False
        result['extended'] = ext.groups() if ext else False
        result['logical'] = lgi.pop() if lgi else False

        return result

    # extended
    def create_ext_part(self):

        info = self.get_info()

        if info.get('free') and not info['extended']:

            start = info['free'][0] + "GB"
            end = info['free'][1] + "GB"

            status, out = subprocess.getstatusoutput("%s %s mkpart extended %s %s" % (self.parted, self.disk, start, end))
            print("%s return value: %s" % ("%s %s mkpart extended %s %s" % (self.parted, self.disk, start, end), status))

        else:
            print("There is no space available for this disk, and an extended partition cannot be created!!")
            return False

        return self.get_info()['extended'][0]

    # logical
    def create_lgi_part(self):

        info = self.get_info()

        if info.get('extended') and info.get('free'):

            start = info['free'][0] + "GB"
            end = info['free'][1] + "GB"

            status, out = subprocess.getstatusoutput("%s %s mkpart logical %s %s %s" % (self.parted, self.disk, 'ext4', start, end))
            print("%s return value: %s" % ("%s %s mkpart logical %s %s %s" % (self.parted, self.disk, 'ext4', start, end), status))

        else:
            print("Error. A logical partition cannot be created because the extended partition does not exist")
            return False

        return self.get_info()['logical'][0]

    # set flag
    def set_flag(self, num):

        info = self.get_info()

        if str(num) in info.get('logical'):

            status, out = subprocess.getstatusoutput("%s %s toggle %s lvm" % (self.parted, self.disk, num))
            print("%s return value: %s" % ("%s %s toggle %s lvm" % (self.parted, self.disk, num), status))

        else:
            print("Error. The logical partition flag cannot be set because the logical partition does not exist")
            return False

        return self.get_info()

    # resize extend
    def resize_ext_part(self):

        info = self.get_info()

        if info.get('free') and info.get('extended'):

            num = info['extended'][0]
            end = '100%'

            status, out = subprocess.getstatusoutput("%s %s resizepart %s %s" % (self.parted, self.disk, num, end))
            print("%s return value: %s" % ("%s %s resizepart %s %s" % (self.parted, self.disk, num, end), status))

        else:
            return False

        return self.get_info()['extended'][0]
