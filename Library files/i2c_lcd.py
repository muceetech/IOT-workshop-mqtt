from lcd_api import LcdApi
import time

class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = 0x08
        self.en = 0x04
        self.rs = 0x01
        self.data_mask = 0xF0
        self.init_lcd()
        super().__init__(num_lines, num_columns)

    def init_lcd(self):
        time.sleep_ms(50)
        self.send(0x33, 0)
        self.send(0x32, 0)
        self.send(0x28, 0)
        self.send(0x0C, 0)
        self.send(0x06, 0)
        self.clear()

    def send(self, data, mode):
        upper = data & 0xF0
        lower = (data << 4) & 0xF0
        self.write4bits(upper | mode)
        self.write4bits(lower | mode)

    def write4bits(self, data):
        self.i2c.writeto(self.i2c_addr, bytes([data | self.backlight | self.en]))
        time.sleep_us(500)
        self.i2c.writeto(self.i2c_addr, bytes([data | self.backlight]))
        time.sleep_us(100)

    def clear(self):
        self.send(0x01, 0)
        time.sleep_ms(2)
        self.cursor_x = 0
        self.cursor_y = 0

    def putchar(self, char):
        self.send(ord(char), self.rs)
