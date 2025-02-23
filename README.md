# Repeat music player with RPi0, Audio Hat and RTC

A repeat music player with RPi0, Audio Hat, RTC and an LED. It is used to play mp3 files kept in a folder (morning and evening) at a set time. In my case I play in the morning 0900hrs and evening 1830hrs. 

## I used the following components:
- Raspberry Pi 0 - 2w
- [WM8960 Audio HAT]
- [PCF8563 RTC Board]
- A Green LED

## Connections
![image](https://github.com/user-attachments/assets/21929334-1121-46c5-83fc-f2d150c74154)

LED: GPIO 27 / PIN 13
RTC PIN: VCC 3V3, GND PIN 6, SDA GPIO 0/ PIN 27, SCL GPIO 1 / Pin 28


## Steps
RPIOS Bookworm 32-bit Lite
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo apt-get install python3-smbus
sudo apt install git
sudo mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old
sudo pip3 install RPi.GPIO
```

Enable I2C in Raspberry Pi Configuration
sudo raspi-config
Interface Options → I2C and enable I2C

Then, lets edit config.txt to enable i2c for the RTC clock as the default is being used by Audio hat.
```
sudo nano /boot/firmware/config.txt
```
Add below line:
```
dtparam=i2c_vc=on
```
Reboot pi:
```
sudo reboot
```
Check if the hat and RTC is detected by : 
```
ls /dev/i2c*
```
```
sudo i2cdetect -y 0
```

Lets install the Audio HAT drivers:
```
git clone https://github.com/waveshareteam/WM8960-Audio-HAT
cd WM8960-Audio-HAT
sudo ./install.sh 
sudo reboot
```
Check if the hat is detected
```
sudo dkms status
```
Install mp3 support
```
sudo apt-get install mpg123
```
Testing music:
```
sudo mpg123 ~/music/extra/500miles.mp3
```
Increase volume using the mixer
```
sudo alsamixer  #to adjust sound, use F6 to select the card
```

Lets setup RTC now, we have to setup the time in RTC and also do not forget the shift the jumper on rtc to Battery instead of VCC:
```
cd ~/PCF8563-Code/code
python3 set_time_date.py
```

Lets start the python code which will run the mp3 files at a set time:
```
cd ~/music
python3 play_offline.py
```

![1](https://github.com/user-attachments/assets/8ccb6c46-9650-47ac-a95f-7faca7050677)
![2](https://github.com/user-attachments/assets/b8574ecf-2878-4122-8ff8-aad4a2d31599)
![3](https://github.com/user-attachments/assets/40fffe5b-3da5-4de3-9e07-64b3a02e660a)
![4](https://github.com/user-attachments/assets/238da8cd-0646-4bfc-8bfe-41c5872ebdfc)
![5](https://github.com/user-attachments/assets/f380cc68-ca0f-4346-8538-193a2e272df0)
