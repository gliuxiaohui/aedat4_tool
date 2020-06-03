##!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import aedat
from PIL import Image


def mkdir(path):
  # 去除首位空格
  path = path.strip()
  # 去除尾部 \ 符号
  path = path.rstrip("\\")
  path = path.split(".aedat4")[0]
  path = path.split("/")[-1]
  aedat4_name = path
  path = "frame/" + path

  # 判断路径是否存在  存在: True; 不存在: False
  isExists=os.path.exists(path)

  # 判断结果
  if not isExists:    
    print(path, " create file success")
    # 创建目录操作函数
    os.makedirs(path)
    return aedat4_name
  else:
    # 如果目录存在则不创建，并提示目录已存在
    print(path, " the fail is exited")
    return aedat4_name



if (len(sys.argv)!= 2):
    print("input fail. The format: python test.py youraedat4")
    os._exit(0)

input_file = sys.argv[1]
decoder = aedat.Decoder(input_file)
aedat4_name = mkdir(input_file)

print(decoder.id_to_stream())
event_txt_name = aedat4_name + "-even.txt"
imu_txt_name = aedat4_name + "-imu.txt"
triggers_txt_name = aedat4_name + "-triggers.txt"

event_txt = open(event_txt_name, "w")
imu_txt = open(imu_txt_name, "w")
triggers_txt = open(triggers_txt_name, "w")
for packet in decoder:
    print(packet['stream_id'], end=': ')
    if 'events' in packet:
        print('{} polarity events'.format(len(packet['events'])))
        for i in range(len(packet['events'])):
            string = "  ".join(str(x) for x in packet['events'][i])
            string = str(packet['stream_id'])+ "  " + string + "\n"
            event_txt.write(string)

    elif 'frame' in packet:
        print('{} x {} frame'.format(packet['frame']['width'], packet['frame']['height']))     
        frame_name =  "frame/"+ aedat4_name+  "/"+ str(packet['stream_id'])+ "  "+ str(packet['frame']['t'])+".jpeg"
        im = Image.fromarray(packet['frame']['pixels'])
        im.save(frame_name) 
    elif 'imus' in packet:
        print('{} IMU samples'.format(len(packet['imus'])))       
        for i in range(len(packet['imus'])):
            string = ""

            for x in range(len(packet['imus'][i])):
                if (x == 0):
                    a = str(packet['imus'][i][x])
                elif (x == 1):
                    a = '{:.2f}'.format(packet['imus'][i][x])
                else:
                    # d = '{:.7e}'.format(packet['imus'][i][x])
                    a = str('{:.7e}'.format(packet['imus'][i][x]))
                string = string + str(a) + "  "
            string = str(packet['stream_id'])+ "  " + string + "\n"
            imu_txt.write(string)

    elif 'triggers' in packet:
        print('{} trigger events'.format(len(packet['triggers'])))
        for i in range(len(packet['triggers'])):
            string = "  ".join(str(x) for x in packet['triggers'][i])
            string = str(packet['stream_id'])+ "  " + string + "\n"
            triggers_txt.write(string)

event_txt.close()
imu_txt.close()
triggers_txt.close()

event_txt_size = os.path.getsize(event_txt_name)
if event_txt_size == 0:
    os.remove(event_txt_name)

imu_txt_size = os.path.getsize(imu_txt_name)
if imu_txt_size == 0:
    os.remove(imu_txt_name)

triggers_txt_size = os.path.getsize(triggers_txt_name)
if triggers_txt_size == 0:
    os.remove(triggers_txt_name)

"""
    packet['events'] is a structured numpy array with the following dtype:
    [
        ('t', '<u8'),
        ('x', '<u2'),
        ('y', '<u2'),
        ('on', '?'),
    ]
"""

"""
    packet['frame'] is a dictionary with the following structure:
    {
        't': <int>,
        'begin_t': <int>,
        'end_t': <int>,
        'exposure_begin_t': <int>,
        'exposure_end_t': <int>,
        'format': <str>,
        'width': <int>,
        'height': <int>,
        'offset_x': <int>,
        'offset_y': <int>,
        'pixels': <numpy.array(shape=(height, width), dtype=uint8)>,
    }
    format is one of 'Gray', 'BGR', 'BGRA'
"""

"""
    packet['imus'] is a structured numpy array with the following dtype:
    [
        ('t', '<u8'),
        ('temperature', '<f4'),
        ('accelerometer_x', '<f4'),
        ('accelerometer_y', '<f4'),
        ('accelerometer_z', '<f4'),
        ('gyroscope_x', '<f4'),
        ('gyroscope_y', '<f4'),
        ('gyroscope_z', '<f4'),
        ('magnetometer_x', '<f4'),
        ('magnetometer_y', '<f4'),
        ('magnetometer_z', '<f4'),
        ]
"""

"""
    packet['triggers'] is a structured numpy array with the following dtype:
    [
        ('t', '<u8'),
        ('source', 'u1'),
    ]
        the source value has the following meaning:
            0: timestamp reset
            1: external signal rising edge
            2: external signal falling edge
            3: external signal pulse
            4: external generator rising edge
            5: external generator falling edge
            6: frame begin
            7: frame end
            8: exposure begin
            9: exposure end
"""

