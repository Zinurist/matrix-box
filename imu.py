

import numpy as np

class DummyIMU():

    def __init__(self, random=True):
        self.random = random
        
    def get_data(self):    
        data = np.random.normal(0, 1, 9)
        return {'accel':  list(data)[:3], 'gyro': list(data)[3:6], 'fusionPose': list(data)[6:] }
    
    
    
class MPUIMU():
    def __init__(self, address=0x69):
        from mpu6050 import mpu6050
        self.sensor = mpu6050(address)
        
    def get_data(self):
        accel = self.sensor.get_accel_data()
        accel = (accel['x']/9.8, accel['y']/9.8, accel['z']/9.8)
        gyro = self.sensor.get_gyro_data()
        gyro = (gyro['x'], gyro['y'], gyro['z'])
        return {'accel':  accel, 'gyro': gyro, 'fusionPose': (0,0,0) }
    
    
class RTIMU():

    def __init__(self, settings_file="RTIMULib"):
        self.data = {'accel':  (0,0,0), 'gyro': (0,0,0), 'fusionPose': (0,0,0) }
        self.settings_file = settings_file
        
        #create thread
        from threading import Thread, Lock
        thr = Thread(target=self.poll_imu)
        thr.daemon = True
        thr.start()
        
        
    def get_data(self):
        return {
            'accel' : self.data['accel'],
            'gyro' : self.data['gyro'],
            'fusionPose' : self.data['fusionPose'],
        }
        
    def poll_imu(self):
        import time
        import sys
        import os.path
        import RTIMU

        print("Using settings file " + self.settings_file + ".ini")
        if not os.path.exists(self.settings_file + ".ini"):
          print("Settings file does not exist, will be created")

        s = RTIMU.Settings(self.settings_file)
        imu = RTIMU.RTIMU(s)

        print("IMU Name: " + imu.IMUName())
        if (not imu.IMUInit()):
            print("IMU Init Failed")
            sys.exit(1)
        else:
            print("IMU Init Succeeded")

        imu.setSlerpPower(0.02)
        imu.setGyroEnable(True)
        imu.setAccelEnable(True)
        imu.setCompassEnable(False)

        poll_interval = imu.IMUGetPollInterval()
        print("Recommended Poll Interval: %dmS\n" % poll_interval)
        
        while True:
            if imu.IMURead():
                self.data = imu.getIMUData()
            time.sleep(poll_interval*1.0/1000.0)

            