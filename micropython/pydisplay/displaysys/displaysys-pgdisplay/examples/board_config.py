"""
Board configuration for PyGame.
"""

from displaysys.pgdisplay import PGDisplay as DTDisplay, poll
from eventsys import devices
import sys


width = 320
height = 480
rotation = 0
scale = 2.0

display_drv = DTDisplay(
    width=width,
    height=height,
    rotation=rotation,
    title=f"{sys.implementation.name} on {sys.platform}",
    scale=scale,
)

broker = devices.Broker()

events_dev = broker.create_device(
    type=devices.types.QUEUE,
    read=poll,
    data=display_drv,
    # data2=events.filter,
)

display_drv.fill(0)
