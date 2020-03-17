
import display, imu
from sandsim import SandSim
import sys, time

def main():
    sleep_ms = 10
    size = (64,64)

    display_ = display.RGBMatrixDisplay(size)
    #display_ = display.PILDisplay(size)
    
    imu_ = imu.RTIMU()
    #imu_ = imu.DummyIMU(random=True)
    
    sandsim = SandSim(size)
    
    try:
        print("Press CTRL-C to stop")
        
        start_time = time.time()
        while True:
            time.sleep(sleep_ms)
            end_time = time.time()
            deltatime = end_time-start_time
            start_time = end_time
            
            data = imu_.get_data()
            sandsim.step(deltatime, data)
            img = sandsim.render()
            display_.display(img)
            
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()