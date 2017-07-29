
# from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter.font import Font
import ctypes

G_COLOR_GRAY = "#404040"
G_COLOR_GRAY_DARK1 = "#303030"
G_COLOR_ORANGE = "#FFAA00"
G_COLOR_ORANGE_LIGHT = "#00D0FF"

myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class ConsoleLog(Text):
	def __init__(self, a_master=None):
		super().__init__(a_master, relief='flat', wrap=NONE)
		# Execute by "break" when the key is not an arrow or ctrl+c BEFORE to process the key by the widget

		self.bind("<Key>", lambda event: "pass" if event.keysym in ['Up', 'Down', 'Left', 'Right'] or (event.char == '\x03') else "break")

		# Configure the scrollbars
		self.m_scroll = Scrollbar(a_master)
		self.m_scroll.pack(side=RIGHT, fill=Y)
		# Text Widget
		self["yscrollcommand"] = self.m_scroll.set
		self.m_scroll.config(command=self.yview)

		self.applyStyle()

		self.m_consoleEntry = None

	def applyStyle(self):
		self["height"] = 1
		self["background"] = G_COLOR_GRAY
		self["foreground"] = G_COLOR_ORANGE  # MenuFontColor
		self["insertbackground"] = G_COLOR_ORANGE_LIGHT
		self["highlightbackground"] = G_COLOR_GRAY_DARK1
		self["highlightcolor"] = G_COLOR_GRAY_DARK1
		self["highlightthickness"] = 3  # Active MenuFontColor
		self["padx"] = 3 # Active MenuColor
		self["font"] = Font(family="Consolas", size=11)
		self["selectbackground"] = G_COLOR_ORANGE_LIGHT

	def append(self, a_message):
		self.insert(END, a_message+'\n')

	def appendCommand(self, a_command):
		presentTextLen = len(self.get(1.0, END).rstrip())
		self.insert(END, a_command+'\n')
		# self.tag_add("last_added", presentTextLen - len(a_command), len(a_command))
		# self.tag_config("last_added", background="yellow", foreground="blue")

	def delete(self):
		super().delete(1.0,END)

	def referenceConsoleEntry(self, a_consoleEntry):
		self.m_consoleEntry = a_consoleEntry

class ConsoleEntry(Text):
	def __init__(self, a_master=None, a_consoleLog=None):
		super().__init__(a_master, relief='solid')
		self.m_consoleLog = a_consoleLog
		self.bind("<Key>", lambda event: self.keyInput(event))
		self.bind("<Up>", lambda event: self.previousCommand())
		self.bind("<Return>", lambda event: self.sendCommand())
		self.bind("<Tab>", lambda event: self.autocomplete())
		self.bind("<Shift-D>", lambda event: self.m_consoleLog.delete())

		self.applyStyle()

		self.m_commands = []
		self.m_commandSelector = 0

		# self.minsize(10, 10)
		# self.maxsize(10, 10)

	def _getCleanInput(self):
		cleanedCommand = self.get(1.0, END).replace('\n','')
		cleanedCommand = cleanedCommand.replace('\t', '')
		return cleanedCommand

	def _cleanInput(self):
		cleanInput = self._getCleanInput()
		self.delete(1.0, END)
		self.insert(1.0, cleanInput)

	def _splitCommand(self):
		command = self._getCleanInput()
		commandSize = 8 * len(command)
		maxCommandSizePerLine = self.winfo_width() - 20
		rest = maxCommandSizePerLine - commandSize
		while rest < 0:
			splitIndex = int((commandSize+rest)/8)
			command = command[:splitIndex]+"--\n--"+command[splitIndex+1:]
			rest = rest + maxCommandSizePerLine
		return command

	def applyStyle(self):
		self["height"] = 1
		self["background"] = G_COLOR_GRAY
		self["foreground"] = G_COLOR_ORANGE  # MenuFontColor
		self["insertbackground"] = G_COLOR_ORANGE_LIGHT
		self["highlightbackground"] = G_COLOR_GRAY_DARK1
		self["highlightcolor"] = G_COLOR_ORANGE_LIGHT
		self["highlightthickness"] = 3  # Active MenuFontColor
		self["padx"] = 3 # Active MenuColor
		self["font"] = Font(family="Consolas", size=11)
		self["selectbackground"] = G_COLOR_ORANGE_LIGHT

	def append(self, a_message):
		# self['state'] = 'normal'
		self.insert(END, a_message+'\n')
		# self['state'] = 'disabled'

	def autocomplete(self):
		self.after(1, self._cleanInput)
		command = self._getCleanInput()
		self.delete(1.0, END)
		self.insert(1.0, command)
		self.m_consoleLog.yview_moveto(1.0)

	def previousCommand(self):
		self.delete(1.0, END)
		if len(self.m_commands):
			self.insert(1.0, self.m_commands[self.m_commandSelector])
		self.m_commandSelector -= 1
		if self.m_commandSelector == -1:
			self.m_commandSelector = len(self.m_commands) - 1
		self.m_consoleLog.yview_moveto(1.0)
		print(self.m_commandSelector)

	def keyInput(self,event):
		# self.m_consoleLog.yview_moveto(1.0)
		# self._cleanInput()
		pass

	def sendCommand(self):
		command = self._getCleanInput()
		if command not in self.m_commands:
			self.m_commands.append(command)
		else:
			self.m_commands.remove(command)
			self.m_commands.append(command)
		self.m_consoleLog.appendCommand(self._splitCommand())
		self.delete(1.0, END)
		self.m_consoleLog.yview_moveto(1.0)
		self.m_commandSelector = len(self.m_commands) - 1
		print(self.m_commands)


class MenuBar(tk.Menu):
	def __init__(self, a_master=None):
		super().__init__(a_master, relief='flat')

		# create a pulldown menu, and add it to the menu bar
		self.m_filemenu = Menu(self, tearoff=0, bd=0)
		self.m_filemenu.add_command(label="Open", command="pass")
		self.m_filemenu.add_command(label="Save", command="pass")
		self.m_filemenu.add_separator()
		self.m_filemenu.add_command(label="Exit", command=self.quit)
		self.add_cascade(label="File", menu=self.m_filemenu)

		# create more pulldown menus
		self.m_editmenu = Menu(self, tearoff=0)
		self.m_editmenu.add_command(label="Cut", command="pass")
		self.m_editmenu.add_command(label="Copy", command="pass")
		self.m_editmenu.add_command(label="Paste", command="pass")
		self.add_cascade(label="Edit", menu=self.m_editmenu)

		self.m_helpmenu = Menu(self, tearoff=0)
		self.m_helpmenu.add_command(label="About", command="pass")
		self.add_cascade(label="Help", menu=self.m_helpmenu)

		# self.applyStyle()

	def applyStyle(self):
		self["bg"] = G_COLOR_GRAY

		self.m_filemenu["background"] = G_COLOR_GRAY  # MenuColor
		self.m_filemenu["foreground"] = G_COLOR_ORANGE  # MenuFontColor
		self.m_filemenu["activeforeground"] = G_COLOR_ORANGE_LIGHT  # Active MenuFontColor
		self.m_filemenu["activebackground"] = G_COLOR_GRAY_DARK1 # Active MenuColor

		self.m_editmenu["bg"] = G_COLOR_GRAY  # MenuColor
		self.m_editmenu["fg"] = G_COLOR_ORANGE  # MenuFontColor
		self.m_editmenu["activebackground"] = G_COLOR_GRAY_DARK1

		self.m_helpmenu["bg"] = G_COLOR_GRAY  # MenuColor
		self.m_helpmenu["fg"] = G_COLOR_ORANGE  # MenuFontColor
		self.m_helpmenu["activebackground"] = G_COLOR_GRAY_DARK1

class MainApplication(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		# self.pack()

		self.master.title("DendyShell - for PixPhetamine Engine")
		self.master.minsize(400, 300)

		self.master["cursor"] = "dot"

		# openImage = PhotoImage(file="openIcon.png")

		img = PhotoImage(file='dphetamine_logo.png')
		# img = PhotoImage(file='icon.png')
		self.master.wm_iconphoto(self.master._w, img)

		# display the menu
		self.m_menuBar = MenuBar(self)
		self.master["menu"] = self.m_menuBar


		self.m_menu = Menu(self.master, tearoff=0)
		self.m_menu.add_command(label="Beep", command="pass")
		self.m_menu.add_command(label="Exit", command=self.quit)
		self.master.bind("<Button-3>", self.showMenu)

		# richTextBox1 = Text(font='{MS Sans Serif} 10')
		# richTextBox1.place(relx=0.05, rely=0.07, relwidth=0.89, relheight=0.59)


		self.m_consoleLog = ConsoleLog(self.master)
		self.m_consoleLog.pack(fill=BOTH, expand=True)

		self.m_consoleEntry = ConsoleEntry(self.master, self.m_consoleLog)
		self.m_consoleEntry.pack(fill=X, expand=False)

		self.m_consoleLog.referenceConsoleEntry(self.m_consoleEntry)

	def showMenu(self, e):
		self.m_menu.post(e.x_root, e.y_root)

def main():
	# create the application
	root = MainApplication()
	# start the program
	root.mainloop()


main()