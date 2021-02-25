from tkinter import *
import win32gui

import subprocess

import adjustScreen

class App():
	# class var
	x=y=0
	width= 100
	height= 100
	hwnd = win32gui.GetForegroundWindow()
	lst = ['Click to see App List']
	state = 1

	# constructor
	def __init__(self):
		self.root = Tk()
		self.root.overrideredirect(1)
		#title
		self.root.title('Adjust Screen')
		#ico
		self.root.iconbitmap('SCR.ico')
		#preset
		self.root.attributes('-topmost', True)
		#geometry
		self.root.geometry(f"+{500}+{500}")
		#transparency
		self.root.wm_attributes('-transparentcolor', "blue")
		
		#drag and move
		self.grip = Label(self.root, bitmap="gray25",bg='#282a2e')	
		self.grip.pack(side="top", fill="both")
		self.grip.bind("<ButtonPress-1>", self.start_move)
		self.grip.bind("<ButtonRelease-1>", self.stop_move)
		self.grip.bind("<B1-Motion>", self.do_move)
		self.grip.bind("<ButtonPress-3>", self.show_ui)
		
		self.frame = Frame(self.root, width=480, height=850, borderwidth=10, relief=RAISED)
		self.frame.configure(background='#1b2940')
		self.frame.pack_propagate(False)
		self.frame.pack()
		
	
		self.width= self.root.winfo_screenwidth()
		self.height= self.root.winfo_screenheight()
		
		# input boxes for x, y, width, height -> for width height, pre determined for you
		self.eCoord1 = Entry(self.frame, width=10)
		self.eCoord1.insert(0, self.x)
		self.eCoord2 = Entry(self.frame, width=10)
		self.eCoord2.insert(0, self.y)
		self.eWidth = Entry(self.frame, width=10)
		self.eWidth.insert(0, self.width)
		self.eHeight = Entry(self.frame, width=10)
		self.eHeight.insert(0,self.height)
		
		self.eCoord1.bind('<Return>', lambda x=None: adjustScreen.adjust(str(self.oApps_var.get()), int(self.eCoord1.get()), int(self.eCoord2.get()), int(self.eWidth.get()), int(self.eHeight.get())))
		self.eWidth.bind('<Return>', lambda x=None: adjustScreen.adjust(str(self.oApps_var.get()), int(self.eCoord1.get()), int(self.eCoord2.get()), int(self.eWidth.get()), int(self.eHeight.get())))
		self.eCoord2.bind('<Return>', lambda x=None: adjustScreen.adjust(str(self.oApps_var.get()), int(self.eCoord1.get()), int(self.eCoord2.get()), int(self.eWidth.get()), int(self.eHeight.get())))
		self.eHeight.bind('<Return>', lambda x=None: adjustScreen.adjust(str(self.oApps_var.get()), int(self.eCoord1.get()), int(self.eCoord2.get()), int(self.eWidth.get()), int(self.eHeight.get())))

		# Buttons
		self.bGetApps = Button(self.frame, text="Refresh App List", command=self.getApps)
		self.bSubmit =Button(self.frame, text="Apply", command=lambda: adjustScreen.adjust(str(self.oApps_var.get()), int(self.eCoord1.get()), int(self.eCoord2.get()), int(self.eWidth.get()), int(self.eHeight.get())))

		# OptionMenu to get the list of active/inactive apps
		self.oApps_var = StringVar(self.frame)	
		self.oApps_var.set(self.lst[0])

		self.oApps = OptionMenu(self.frame, self.oApps_var, *self.lst)

		self.getApps()
		self.bQuit = Button(self.frame, text="Quit", command=self.root.quit)

		# keybinds for hotkeys
		# showSCR bind to a keyboard, TODO: remove this 
		self.root.bind("<Key-F9>", lambda x: self.show_ui())

		self.tCoord1=Label(self.frame,text='x', bg='#1b2940', fg='white')
		self.tCoord2=Label(self.frame, text='y', bg='#1b2940', fg='white')
		self.tWidth=Label(self.frame, text='width', bg='#1b2940', fg='white')
		self.tHeight=Label(self.frame, text='height',bg='#1b2940', fg='white')
		
		self.tCoord1.grid(row=0, column=0)
		self.tCoord2.grid(row=0, column=1)
		self.tWidth.grid(row=0, column=2)
		self.tHeight.grid(row=0, column=3)
		self.eCoord1.grid(row=1, column=0)
		self.eCoord2.grid(row=1, column=1)
		self.eWidth.grid(row=1, column=2)
		self.eHeight.grid(row=1, column=3)
		self.bGetApps.grid(row=0,column=4)
		self.oApps.grid(row=1, column=4)
		self.bSubmit.grid(row=0, column=5)
		self.bQuit.grid(row=1, column=5)

		# explanation of each button (Label area)
		
		# Clock for elapsed time (TODO: to be more sophisticated later)
		

	# instance methods
	def start_move(self, event):
		self.root.x = event.x
		self.root.y = event.y
	def stop_move(self, event):
		self.root.x = None
		self.root.y = None
	def do_move(self, event):
		deltax = event.x - self.root.x
		deltay = event.y - self.root.y
		x = self.root.winfo_x() + deltax
		y = self.root.winfo_y() + deltay
		self.root.geometry(f"+{x}+{y}")
	def show_ui(self):
		if (self.state == 0):
			self.state = 1
			self.root.deiconify()
		else:
			self.state = 0
			self.root.withdraw()
	
	def getApps(self):
		self.oApps["menu"].delete(0, 'end')
		self.lst.clear()
		# use subprocess of powershell to retrieve the list of running apps

		cmd = 'powershell "gps | where {$_.MainWindowTitle} | select MainWindowTitle'
		proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		
		for line in proc.stdout:
			#TODO: encoding doesn't support UTF-8
			#self.lst.append(line.decode(encoding='UTF-8',errors='ignore'))
			if line.rstrip():
				self.lst.append(line.decode(encoding='UTF-8', errors='ignore').rstrip())

#		if (len(self.lst) != 0):
#			del self.lst[0]
		#print(self.lst)
		
		for string in self.lst:
			self.oApps["menu"].add_command(label=string, command = lambda value=string: self.oApps_var.set(value))
		
		return


def main():
	app = App()
	app.root.mainloop()
	exit(0)
if __name__ == "__main__": main()
	
