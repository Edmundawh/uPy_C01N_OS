from badge import oled, btn
from machine import Pin
from time import sleep_ms, ticks_ms
import framebuf as fb
import urequests
from ubinascii import hexlify

def draw_letter_C(fbuf, x, y):
    thickness = 5  # Choose the thickness of the "C" shape
    for i in range(thickness):
        # Top line
        fbuf.line(x + 40 + i, y + 10, x + i, y + 10, 1)
        # Left line
        fbuf.line(x + i, y + 10, x + i, y + 50, 1)
        # Bottom line
        fbuf.line(x + i, y + 50, x + 40 + i, y + 50, 1)

def draw_letter_S(fbuf, x, y):
    thickness = 5  # Choose the thickness of the "S" shape
    for i in range(thickness):
        # Top horizontal line
        fbuf.line(x + 10, y + i, x + 50, y + i, 1)
        # Top left vertical line
        fbuf.line(x + i, y, x + i, y + 30, 1)
        # Middle horizontal line
        fbuf.line(x + 10, y + 30 + i, x + 50, y + 30 + i, 1)
        # Bottom right vertical line
        fbuf.line(x + 50 - i, y + 30, x + 50 - i, y + 50, 1)
        # Bottom horizontal line
        fbuf.line(x + 10, y + 50 - i, x + 50, y + 50 - i, 1)

def draw_letter_G(fbuf, x, y):
    thickness = 5  # Choose the thickness of the "G" shape
    for i in range(thickness):
        # Top line
        fbuf.line(x + 10 + i, y + 10, x + 50, y + 10, 1)
        # Left vertical line
        fbuf.line(x + 10, y + 10 + i, x + 10, y + 50, 1)
        # Bottom line
        fbuf.line(x + 10, y + 50, x + 50 - i, y + 50, 1)
        # Bottom right vertical line
        fbuf.line(x + 50, y + 50 - i, x + 50, y + 30, 1)
        # Bottom right horizontal line
        fbuf.line(x + 50 - i, y + 30, x + 30, y + 30, 1)



# def draw_letter_C(fbuf, x, y):
#     thickness = 5  # Choose the thickness of the "C" shape
#     for i in range(thickness):
#         # Top line
#         fbuf.line(x + 40 + i, y + 10, x + i, y + 10, 1)
#         # Left line
#         fbuf.line(x + i, y + 10, x + i, y + 50, 1)
#         # Bottom line
#         fbuf.line(x + i, y + 50, x + 40 + i, y + 50, 1)

# def draw_letter_S(fbuf, x, y):
#     fbuf.line(x + 10, y + 10, x + 50, y + 10, 1)  # Top horizontal line
#     fbuf.line(x + 10, y + 10, x + 10, y + 30, 1)  # Top left vertical line
#     fbuf.line(x + 10, y + 30, x + 50, y + 30, 1)  # Middle horizontal line
#     fbuf.line(x + 50, y + 30, x + 50, y + 50, 1)  # Bottom right vertical line
#     fbuf.line(x + 50, y + 50, x + 10, y + 50, 1)  # Bottom horizontal line

# def draw_letter_G(fbuf, x, y):
#     fbuf.line(x + 10, y + 10, x + 50, y + 10, 1)   # Top line
#     fbuf.line(x + 10, y + 10, x + 10, y + 50, 1)  # Left vertical line
#     fbuf.line(x + 10, y + 50, x + 50, y + 50, 1)  # Bottom line
#     fbuf.line(x + 50, y + 50, x + 50, y + 30, 1)  # Bottom right vertical line
#     fbuf.line(x + 50, y + 30, x + 30, y + 30, 1)  # Bottom right horizontal line


def app_start():
    px = 64
    py = 32
    oled.fill(0)
    oled.show()
    fbuf = fb.FrameBuffer(bytearray(1024),128,64,fb.MONO_HLSB)
    sleep_ms(200)
    
    # Drawing Animation
    draw_letter_C(fbuf, 3, 5)
    draw_letter_S(fbuf, 43, 5)
    draw_letter_G(fbuf, 73, 5)
    oled.blit(fbuf, 0, 0)
    oled.show()
    sleep_ms(1000)

    fbuf.fill(0)

    while True:
        oled.blit(fbuf,0,0)
        if(btn.A.value() == 0):
            fbuf.fill_rect(px,py,3,3,1)
        else:
            oled.fill_rect(px,py,3,3,int(ticks_ms()/100)%2)
        if(btn.B.value() == 0): 
            return 0
        if(btn.U.value() == 0): py=(py-1)%64
        if(btn.D.value() == 0): py=(py+1)%64
        if(btn.L.value() == 0): px=(px-1)%128
        if(btn.R.value() == 0): px=(px+1)%128
        oled.show()

app_start()



# from badge import oled, btn
# from machine import Pin
# from time import sleep_ms, ticks_ms
# import framebuf as fb
# import urequests
# from ubinascii import hexlify

# def app_start():
# 	px = 64
# 	py = 32
# 	oled.fill(0)
# 	oled.show()
# 	fbuf = fb.FrameBuffer(bytearray(1024),128,64,fb.MONO_HLSB)
# 	sleep_ms(200)
# 	while True:
# 		oled.blit(fbuf,0,0)
# 		if(btn.A.value() == 0):
# 			fbuf.fill_rect(px,py,3,3,1)
# 		else:
# 			oled.fill_rect(px,py,3,3,int(ticks_ms()/100)%2)
# 		if(btn.B.value() == 0): 
# 			return 0
# 		if(btn.U.value() == 0): py=(py-1)%64
# 		if(btn.D.value() == 0): py=(py+1)%64
# 		if(btn.L.value() == 0): px=(px-1)%128
# 		if(btn.R.value() == 0): px=(px+1)%128
# 		oled.show()