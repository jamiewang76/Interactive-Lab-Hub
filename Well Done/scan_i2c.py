import smbus

# Create an smbus object for the I2C bus (use 1 for Raspberry Pi 3, 4; use 0 for Raspberry Pi 1, 2)
bus = smbus.SMBus(1)

def scan_i2c():
    devices = []
    for address in range(0x03, 0x78):
        try:
            bus.read_byte(address)
            devices.append(hex(address))
        except:
            pass
    return devices

# Scan for I2C devices
found_devices = scan_i2c()

# Print the results
if found_devices:
    print("I2C devices found:")
    for device in found_devices:
        print(device)
else:
    print("No I2C devices found.")