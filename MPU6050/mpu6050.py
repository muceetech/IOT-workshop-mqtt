# mpu6050.py
class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        i2c.writeto_mem(addr, 0x6B, b'\x00')  # Wake up sensor

    def read_raw_data(self, reg):
        high, low = self.i2c.readfrom_mem(self.addr, reg, 2)
        value = high << 8 | low
        if value > 32768:
            value -= 65536
        return value

    def get_values(self):
        return {
            "AcX": self.read_raw_data(0x3B),
            "AcY": self.read_raw_data(0x3D),
            "AcZ": self.read_raw_data(0x3F),
            "GyX": self.read_raw_data(0x43),
            "GyY": self.read_raw_data(0x45),
            "GyZ": self.read_raw_data(0x47),
        }
