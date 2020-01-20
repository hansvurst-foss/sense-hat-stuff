'''
Setting variables available in all modules
'''

from sense_hat import SenseHat
try:
    from sense_emu import SenseHat
except ImportError: pass


sense = SenseHat()

R = (100,0,0)
G = (0,100,0)
B = (0,0,100)

bl = (0,0,0)
wh = (100,100,100)
