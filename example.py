# Demo ==>
# THIS FILE IS NOT INTENDED TO RUN! ALL OF THE CODE BELOW IS MERE PSEUDOCODE!

from gwenClient import *

obj = gwenClient('localhost', 8888)
if obj is not None:
    obj.play()
    obj.stop()
    obj.increaseVolume()
    obj.replay()
    # and so on ...


# For Hand Gesture control, simply pass a string like this-->
obj.autoHandler('play')
obj.autoHandler('stop')
obj.autoHandler('increaseVolume')

