# aedat4_tool
Tools for manipulating .aedat4 files (timestamped address-event data from neuromorphic hardware) in Python.

## Ubuntu 18.04 Dependencies:
Python >=3.5

install pip3

  $ sudo apt install python3-pip -y

then,

  $ pip3 install Pillow

  $ [pip3 install aedat](https://pypi.org/project/aedat/)

## Usage
    aedat4Totxt.py: manipulate .aedat4 files to .txt file

    $ python3 aedat4Totxt.py you.aedat4


## File Format
* xxx_event.txt
    
    There are 5 columns in txt file.
  1. stream_id(int)
  2. timestamp(uint64)
  3. x(uint16)
  4. y(uint16)
  5. polarity(bool)

* xxx_imu.txt

    There are 12 columns in txt file.

  1. stream_id(int) 
  2. timestamp(uint64)
  3. temperature(float32) 
  4. accelerometer_x(float32) 
  5. accelerometer_y(float32) 
  6. accelerometer_z(float32) 
  7. gyroscope_x(float32)
  8. gyroscope_y(float32) 
  9. gyroscope_z(float32) 
  10. magnetometer_x(float32) 
  11. magnetometer_y(float32) 
  12. magnetometer_z(float32)

* xxx_triggers.txt

    There are 3 columns in txt file.

  1. stream_id(int) 
  2. timestamp(uint64)
  3. source(uint8) 


