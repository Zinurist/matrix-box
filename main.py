
import display, imu
from sand-sim import SandSim
import sys, time

def main():
    sleep_ms = 10
    size = (64,64)

    #display = display.RGBMatrixDisplay()
    display = display.PILDisplay(size)
    
    #imu = imu.RTIMU()
    imu = imu.DummyIMU(random=True)
    
    sandsim = SandSim(size)
    
    try:
        print("Press CTRL-C to stop sample")
        
        start_time = time.time()
        while True:
            time.sleep(sleep_ms)
            end_time = time.time()
            deltatime = end_time-start_time
            start_time = end_time
            
            data = imu.get_data()
            sandsim.step(deltatime, data)
            img = sandsim.render()
            display.display(img)
            
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__init__':
    main()
