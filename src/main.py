# ----------------------------------------------------------------------------
# Example program for nav-button + slider.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pcb-pico-nav-button
#
# ----------------------------------------------------------------------------

# Note: revision 1.0 has a wrong pin-to-pad mapping and therefore does
#       not support "push"
REVISION = "1.0"

import board
import time
import keypad
import digitalio

# --- pin configuration   ---------------------------------------------------

PIN_SLIDER = board.GP16
if REVISION == "1.0":
  PIN_SE     = board.GP17
  PIN_NE     = board.GP18
  PIN_SW     = board.GP15
  PIN_COMMON = board.GP14
  PIN_NW     = board.GP13
else:
  PIN_SE     = board.GP18
  PIN_NE     = board.GP16
  PIN_SW     = board.GP13
  PIN_DOWN   = board.GP14
  PIN_NW     = board.GP15

# --- objects   -------------------------------------------------------------

if REVISION == "1.0":
  # common plays role of GND
  common = digitalio.DigitalInOut(PIN_COMMON)
  common.direction = digitalio.Direction.OUTPUT
  common.value = False
  keys  = [PIN_SE,PIN_NE,PIN_SW,PIN_NW]
  names = ["SE","NE","SW","NW"]
else:
  keys  = [PIN_SE,PIN_NE,PIN_SW,PIN_NW,PIN_DOWN]
  names = ["SE","NE","SW","NW","DOWN"]

nav = keypad.Keys(keys,
                  value_when_pressed=False,pull=True,
                  interval=0.1,max_events=4)

slider = digitalio.DigitalInOut(PIN_SLIDER)
slider.direction = digitalio.Direction.INPUT
slider.pull      = digitalio.Pull.UP

# --- query keys and slider   -----------------------------------------------

slider_old = slider.value
print(f"current slider setting: {slider_old}")

while True:
  slider_new = slider.value
  if slider_new != slider_old:
    print(f"slider changed from {slider_old} to {slider_new}")
    slider_old = slider_new

  event = nav.events.get()
  if event and event.pressed:
    print(f"navigation with key: {names[event.key_number]}")

  time.sleep(0.1)
