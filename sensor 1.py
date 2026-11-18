from machine import I2C, Pin
import time

# MAX30100 default I2C address
MAX30100_I2C_ADDRESS = 0x57

# Initialize I2C0 on Raspberry Pi Pico
# GP4 is SDA, GP5 is SCL
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

print("Scanning I2C bus...")
devices = i2c.scan()
if MAX30100_I2C_ADDRESS in devices:
    print("MAX30100 found on I2C address 0x57!")
else:
    print("MAX30100 not found! Please check your wiring.")

def init_max30100():
    try:
        # 1. Reset sensor mode register (0x06)
        i2c.writemem(MAX30100_I2C_ADDRESS, 0x06, b'\x40')
        time.sleep(0.1)
        
        # 2. Set mode to SpO2 (HR + Red LED active) -> 0x03
        i2c.writemem(MAX30100_I2C_ADDRESS, 0x06, b'\x03')
        
        # 3. Set LED current configuration register (0x09) (adjust current if needed)
        i2c.writemem(MAX30100_I2C_ADDRESS, 0x09, b'\x24')
        
        print("MAX30100 initialized successfully.")
    except Exception as e:
        print("Initialization error:", e)

# Run initialization
init_max30100()

def read_fifo():
    try:
        # Read 4 bytes from FIFO data register (0x05): 2 bytes IR, 2 bytes Red
        data = i2c.readfrom_mem(MAX30100_I2C_ADDRESS, 0x05, 4)
        ir = (data[0] << 8) | data[1]
        red = (data[2] << 8) | data[3]
        return ir, red
    except Exception:
        return 0, 0

print("Reading sensor data... Place your finger lightly on the sensor.")

# Main monitoring loop
while True:
    ir, red = read_fifo()
    if ir > 0 or red > 0:
        print(f"IR Value: {ir} | Red Value: {red}")
    time.sleep(0.05)