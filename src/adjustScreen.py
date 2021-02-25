import win32gui
import win32con
import threading
import time

# input boxes for x, y, width, height set up 
# by default: screenwidth, screenheight used for width height
# dropdown for selectin app

signal_foreground = threading.Event()

def waitOnSignal(hwnd, x,y,width,height):
	# TODO: fix wait till WM protocol arrives
	# while it's active window (foreground), pretty bad wait as it's a busy waiting
	while (win32gui.GetForegroundWindow() == hwnd):		
		print('Sleeping...')
		time.sleep(1)
	print('Woke up!')
	print('off state')

	win32gui.SetWindowPos(hwnd, -2, x, y, width, height, 1)
	return

def adjust(title, x,y,width,height, st):
	#  up only active
	hwnd = win32gui.FindWindow(None, title)
	print(title)
	print(hwnd)
	if (hwnd != 0): 
		print('on state')
		win32gui.MoveWindow(hwnd, x,y,width,height,1)
		win32gui.SetWindowPos(hwnd, -1, x,y,width,height, 1)
	
	# Thread join wait
	# TODO: fix	
	if (st == 1):
		print('got here')
		t1 = threading.Thread(target=waitOnSignal, args=(hwnd, x,y,width,height,))
		t1.start()
	
	#print('signal arrived')
	
	return

def off(title, x,y,width,height):
	print('off state')
	hwnd = win32gui.FindWindow(None, title)
	win32gui.SetWindowPos(hwnd, -2,x,y,width,height,1)
	return
