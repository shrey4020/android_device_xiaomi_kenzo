# Copyright (C) 2016 The CyanogenMod Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import common
import re
import sha

def FullOTA_Assertions(info):
  pass

def IncrementalOTA_Assertions(info):
  pass

image_partitions = {
   'adspso.bin'        : 'dsp',
   'cmnlib.mbn'        : 'cmnlib',
   'devinfo.img'       : 'devinfo',
   'emmc_appsboot.mbn' : 'aboot',
   'hyp.mbn'           : 'hyp',
   'keymaster.mbn'     : 'keymaster',
   'mdtp.img'          : 'mdtp',
   'NON-HLOS.bin'      : 'modem',
   'rpm.mbn'           : 'rpm',
   'sbl1.mbn'          : 'sbl1',
   'splash.img'        : 'splash',
   'tz.mbn'            : 'tz',
}

def FullOTA_InstallEnd(info):
  for img_name, partition in image_partitions.iteritems():
    try:
      img_file = info.input_zip.read("RADIO/" + img_name)
      info.script.Print("update image " + img_name + "...")
      common.ZipWriteStr(info.output_zip, 'firmware-update/' + img_name, img_file)
      info.script.AppendExtra(('package_extract_file("firmware-update/' + img_name + '", "/dev/block/bootdevice/by-name/' + partition + '");'))
    except KeyError:
      print "warning: no " + img_name + " image in input target_files; not flashing " + img_name


def IncrementalOTA_InstallEnd(info):
  for img_name, partition in image_partitions.iteritems():
    try:
      source_file = info.source_zip.read("RADIO/" + img_name)
      target_file = info.target_zip.read("RADIO/" + img_name)
      if source_file != target_file:
        common.ZipWriteStr(info.output_zip, 'firmware-update/' + img_name, target_file)
        info.script.AppendExtra(('package_extract_file("firmware-update/' + img_name + '", "/dev/block/bootdevice/by-name/' + partition + '");'))
      else:
        print img_name + " image unchanged; skipping"
    except KeyError:
      print "warning: " + img_name + " image missing from target; not flashing " + img_name

