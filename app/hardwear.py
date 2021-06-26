import ubinascii
import machine
from machine import Pin, PWM


client_id = ubinascii.hexlify(machine.unique_id())


