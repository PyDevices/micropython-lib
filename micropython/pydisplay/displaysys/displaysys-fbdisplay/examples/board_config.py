"""Qualia S3 RGB-666 with TL040HDS20 4.0" 720x720 Square Display"""
# Similar configs may be available for RGBMatrix, is31fl3741 and picodvi

from rgbframebuffer import RGBFrameBuffer  # type: ignore
from machine import I2C, Pin # type: ignore
from pca9554 import PCA9554 # type: ignore
from ft6x36 import FT6x36 # type: ignore
from displaysys.fbdisplay import FBDisplay
import eventsys.device as device


def send_init_sequence(init_sequence, mosi, sck, cs):
    cs(0)
    for byte in init_sequence:
        for _ in range(8):
            mosi(byte & 0x80)
            sck(1)
            byte <<= 1
            sck(0)
    cs(1)


tft_pins = {
    "de": 17,
    "vsync": 3,
    "hsync": 46,
    "dclk": 9,
    "red": (1, 2, 42, 41, 40),
    "green": (21, 47, 48, 45, 38, 39),
    "blue": (10, 11, 12, 13, 14),
}

tft_timings = {
    "frequency": 16_000_000,
    "width": 720,
    "height": 720,
    "hsync_pulse_width": 2,
    "hsync_front_porch": 46,
    "hsync_back_porch": 44,
    "vsync_pulse_width": 2,
    "vsync_front_porch": 16,
    "vsync_back_porch": 18,
    "hsync_idle_low": False,
    "vsync_idle_low": False,
    "de_idle_high": False,
    "pclk_active_high": False,
    "pclk_idle_high": False,
}

init_sequence = bytes()

i2c = I2C(0, sda=Pin(8), scl=Pin(18), freq=100000)
iox = PCA9554(i2c, address=0x38)
btn_down = iox.Pin(6, Pin.IN)
btn_up = iox.Pin(5, Pin.IN)
reset = iox.Pin(2, Pin.OUT, value=1)
backlight = iox.Pin(4, Pin.OUT, value=1)

send_init_sequence(init_sequence, mosi=iox.Pin(7, Pin.OUT),
                   sck=iox.Pin(0, Pin.OUT, value=0), cs=iox.Pin(1, Pin.OUT, value=1))


fb = RGBFrameBuffer(**tft_pins, **tft_timings)
mv = memoryview(fb)
mv[:] = b'\xFF' * len(mv)
fb.refresh()

touch_drv = FT6x36(i2c, address=0x48)  #, irq = iox.Pin(3, Pin.OUT))

def touch_read_func():
    touches = touch_drv.touches
    if len(touches):
        return touches[0]['x'], touches[0]['y']
    return None


# Typical board_config.py setup from here on out

display_drv = FBDisplay(fb)

touch_rotation_table=(0, 0, 0, 0)

broker = device.Broker()

touch_dev = broker.create_device(
    type=device.Types.TOUCH,
    read=touch_read_func,
    data=display_drv,
    data2=touch_rotation_table,
)
