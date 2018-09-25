# -*- coding: utf-8 -*-

__author__ = 'http://zongming.net'

import re
import subprocess


# LVM 
class LVM(object):

    def __init__(self, dev):

        self.disk = dev
        self.lvs = "/sbin/lvdisplay"
        self.vgs = "/sbin/vgdisplay"
        self.pvce = "/sbin/pvcreate"
        self.vgext = "/sbin/vgextend"
        self.lvext = "/sbin/lvextend"

    # 获得 LVS 信息
    def get_info(self):

        result = {}
        status, output = subprocess.getstatusoutput('%s' % self.lvs)

        if status != 0:
            return False

        result['path'] = re.search(r"[ ]LV Path[ ]*(.*?[^swap])\n", output).group(1)
        result['lv'] = re.search(r"[ ]LV Name[ ]*(.*?[^swap])\n", output).group(1)
        result['vg'] = re.search(r"[ ]VG Name[ ]*(.*?)\n", output).group(1)

        return result

    # 可用 PE
    def get_free_pe(self):

        status, output = subprocess.getstatusoutput(self.vgs)
        if status != 0:
            return False

        pe = re.search(r"[ ]Free  PE.*?Size[ ]*(\d+).*?\n", output).group(1)

        return pe

    # 逻辑卷
    def extend_lvm(self):
        lvs_info = self.get_info()

        # 创建物理卷
        status, output = subprocess.getstatusoutput("%s %s" % (self.pvce, self.disk))
        if status == 0:
            print("%s return value: %s" % ("%s %s" % (self.pvce, self.disk), status))
        else:
            return False

        # 扩展卷组
        vg = lvs_info['vg']
        status, output = subprocess.getstatusoutput("%s %s %s" % (self.vgext, vg, self.disk))

        if status == 0:
            print("%s return value: %s" % ("%s %s %s" % (self.vgext, vg, self.disk), status))
        else:
            return False

        # 扩展逻辑卷
        path = lvs_info['path']
        free_pe = self.get_free_pe()

        status, output = subprocess.getstatusoutput("%s -l +%s %s" % (self.lvext, free_pe, path))

        if status == 0:
            print("%s return value: %s" % ("%s -l +%s %s" % (self.lvext, free_pe, path), status))
        else:
            return False

        # path
        return path
