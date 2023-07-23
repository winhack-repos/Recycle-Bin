import os
try:
	__import__("winsound")
except ModuleNotFoundError:
	print("Recycle Hacker only works in Windows.")
	os._exit(1)
import tkinter as tk
import tkinter.messagebox as msgBox
import tkinter.simpledialog as simplePops
import tkinter.filedialog as simpleFilPops
import subprocess
from glob import glob
import base64
import winreg

def btsToInt(bts):
	count = 0
	out = 0
	for btVal in list(bts):
		out += btVal << (count * 8)
		count += 1
	return out

def copyStr(str):
	res = ""
	if type(str) == bytes:
		res = b""
	for ch in str:
		if type(ch) != int:
			ch = ord(ch)
		res += chr(ch).encode("utf-8")
	return res

def openSel():
	selFile = os.path.join(binPath, uiFiles[listbox.curselection()[0]][3])
	try:
		os.startfile(selFile, "open")
	except:
		subprocess.Popen("rundll32.exe shell32.dll,OpenAs_RunDLL " + selFile)

def renSel():
	selFile = os.path.join(binPath, uiFiles[listbox.curselection()[0]][2])
	with open(selFile, "rb") as filIO:
		print(filIO.read())

def onSelect(e):
	selM.entryconfig(0, state="normal")
	selM.entryconfig(1, state="normal")

def aboutPop():
	msgBox.showinfo("Recycle Hacker", f"Version: {ver}\nRunning on {winVer}\n\nRecycle Hacker is a program from the Winhack series\nMore info on https://winhack.rixthetyrunt.repl.co/")

winVer = "Unknown"
try:
	key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", 0, winreg.KEY_READ)
	winVer = winreg.QueryValueEx(key, "ProductName")[0]
	winreg.CloseKey(key)
	del globals()["key"]
except:
	pass
ver = "2023.21.7.0"
sid = None
out = subprocess.Popen("wmic useraccount get name, sid", stdout=subprocess.PIPE)
out = out.communicate()[0].decode().replace("\r", "")
for line in out.split("\n"):
	if line.startswith(os.getlogin()):
		sid = line.replace(os.getlogin(), "").strip()
		break
binPath = os.path.join("C:\\$Recycle.Bin\\", sid)
currDir = os.getcwd()
os.chdir(binPath)
binFiles = glob("*")
os.chdir(currDir)
uiFiles = []
for file in binFiles:
	if file.startswith("$I") and os.path.exists(os.path.join(binPath, "$R" + file[2:])):
		with open(os.path.join(binPath, "$I" + file[2:]), "rb") as metaIO:
			""" TODO: Fix this crap
				bts = copyStr(metaIO.read())[24:28]
				print(repr(bts))
				bts = btsToInt(bts)
				print(bts, metaIO.read())
			"""
			fileDir = copyStr(metaIO.read())[28:-3] # For now, I'm going to use -3 as the end...
			uiFiles.append([b"".join(fileDir.split(b"\x00")).decode().split("\\")[-1], b"".join(fileDir.split(b"\x00")).decode(), file, "$R" + file[2:]])
app = tk.Tk()
app.resizable(False, False)
app.iconphoto(True, tk.PhotoImage(data=base64.b64decode(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAMNJREFUOE9jZKAQMGLT77D//39s4gccGTHUowjANB5whAj/56gH04w/GsG0w36IucgGwQ0Aad7v2YCiAd0AGN9xewPcEBQDcNmMzSUwV6AYAPM3LpeAbIYBrAbU60OkGy9ijxpkebwGoGt3nKTIsD/vPlwYZAGGAdBQ/g+zBaYaphlGI2sGxxCybaCYQDcA3TUkGYDudBDfwf4+9nRAFS/gMgTmDXTnY4QBTCEsSaNHK8G8gB5gSHkDa6bD6QLsyQi7KABV73sRnkoBhQAAAABJRU5ErkJggg==")))
app.title("Recycle Hacker")
app.geometry("600x375")
listbox = tk.Listbox(app, font=("Arial", 11), activestyle="none")
for fileDat in uiFiles:
	listbox.insert(tk.END, fileDat[0])
listbox.bind("<<ListboxSelect>>", onSelect)
listbox.pack(fill=tk.BOTH, expand=True)
menu = tk.Menu(app)
selM = tk.Menu(menu, tearoff=False)
selM.add_command(label="Preview with default program...", command=openSel, state="disabled")
selM.add_command(label="Rename...", command=renSel, state="disabled")
menu.add_cascade(label="Selection", menu=selM)
menu.add_command(label="About", command=aboutPop)
app.config(menu=menu)
app.mainloop()