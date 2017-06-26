from breezypythongui import EasyFrame
from math import log
from tkFileDialog import askopenfilename
from PIL import Image
from os.path import basename
from Tkinter import Entry,StringVar

import struct
import wave as W
import time

# This are the GUI descriptors
class Encryptor(EasyFrame):
	def __init__(self):
		EasyFrame.__init__(self,title='Encryptor',width = 900,height=300,resizable=False)
		self.addLabel(text = "Welcome to the Encryptor", row = 0, column = 0, columnspan = 2)
		self.addLabel(text = "Enter the message : ", row=1, column=0)
		self.message=self.addTextArea('',row=1,column=1,height=2, width=20,wrap='word')
                self.addLabel(text="Enter the Password : (max size is 5)", row=2, column=0)
		
		self.Password = StringVar() #Password variable
		passEntry = Entry(self, textvariable=self.Password, show='*').grid(row=2,column=1)

		self.addLabel(text="Select the File : ", row=3, column=0)
		self.filename=self.addLabel(text="", row=3, column=1)
		self.browse=self.addButton(text="Browse",row=4, column=1,command=self.Browse)
		self.encrypt=self.addButton(text='Encrypt',row=5,column=0,state='disabled',command=self.Encrypt)
		self.hint=self.addLabel(text="Awaiting input.......", row=5,column=1)	
	
	# Function to browse in memory and select file for encryption
	def Browse(self):
	
		filetypes = [("Image files", "*.png"),("Image files", "*.bmp"),("WAVE files", "*.wav")]
		# only files with above extensions will be visible
		fileName =askopenfilename(parent = self,filetypes = filetypes)
		self.filename['text']=fileName
		self.hint['text']='Awaiting input.......'
		self.encrypt['state']='normal'

	def Encrypt(self):
		
		#First we declare a few functions which we shall use repeatedly.
		
		# Function which converts a number i.e. linear form to (x,y) coordinates i.e. 2D form using the Hilbert curve.
		def dtoxy(n, d):
			t = d 
			rx = ry = x = y = 0
			s = 1
			while (s < n):
				rx = 1 & (t/2)
				ry = 1 & (t ^ rx)
				x,y = rot(s,x,y,rx,ry)
				x+=s*rx
				y+=s*ry
				t/=4
				s*=2
			return x,y
	 	
		# Helping function to dtoxy(), it is needed as the Hilbert curve's individual parts are rotated 
		# with respect to each other.  
		def rot(n,x,y,rx,ry):
			if ry == 0:
				if rx == 1:
					x = n-1 - x
					y = n-1 - y
				
				x,y = y,x
			return x,y
		
		# Function which generates a key using the password, which is used to determine the starting point
		# of encoding.		
		def keygen(n):
			key = 0		
			for i in range(len(password)):
				ch=password[i]
				asc=ord(ch)
				key += key + asc*(pow(33,i))
				key = key%(n*n)
			return key
			
		# Function which changes the least significant bit of a number.	
		def change (integer, bit):
			return ((integer & ~1) | bit)
	
		self.encrypt['state']='disabled'
		self.hint['text']='Encrypting........'
		path=self.filename['text']
		
		if path[-3:]=='bmp' or path[-3:]=='png':
		#This is when an image file is selected
			image_path=self.filename['text']
			message=self.message.getText()
			password=self.Password.get()
			if len(password)>5:
				self.messageBox("ERROR ALERT", "The max password size is 5")
				self.encrypt['state']='normal'
				return
			if len(message)>500:
				self.messageBox("ERROR ALERT", "The max message length is 500")
				self.encrypt['state']='normal'
				return
			
			# opening image using Image module and obtaining dimensions.			
			im=Image.open(image_path)
			pix=im.load()
			width,height=im.size
			
			# checking if dimensions are sufficient to encode message
			if len(message)>(width*height)/3:
				self.messageBox("ERROR ALERT", "You have exceeded the maximum message size supported by the current image, which is "+str((width*height)/3))
				self.encrypt['state']='normal'
				return
			n = 2**min(int(log(width,2)),int(log(height,2)))
			
			# generating starting point for encoding.
			key = keygen(n)

			# This function returns the next location to encode. Here it uses 'ct' which is incremented after each character.
			def traverse2(ct):
				return dtoxy(n,ct)
				
			x,y = dtoxy(n,key)
			# The rem variable records the last location where encryption was done.
			rem = key
			
			# Iterating through message and encoding it.
			for index in range(len(message)):
				ch=message[index]
				asc=ord(ch)
				# asc_bin is a 9-digit binary number which is encoded in 9 pixels. The last digit 
				# tells if the message is over. It represents one character in total.
				asc_bin="%08d0" % int(bin(asc)[2:])
				t=0
				for i in range(0,3):
					for j in range(0,3):
						tostore=int(asc_bin[t])
						pixel=list(pix[x,y])
						# changing the least significant bit of an RGB value in one pixel.
						pixel[j]=change(pixel[j],tostore)
						pix[x,y]=tuple(pixel)
						t+=1
						# moving to next location
						x,y = traverse2(9*index+3*i+j+1 + key)
						rem = 9*index+3*i+j+1 + key
			
			# changing last location encoded to represent message is over.
			x,y=traverse2(rem-1)
			pixel=list(pix[x,y])
			pixel[2]|=1
			pix[x,y]=tuple(pixel)
			
			# saving image
			s=basename(image_path)
			im.save('en'+s)
			self.hint['text']='Image file generated'
			self.filename['text']=''

		else:
		#This is the case when file selected is an audio file
			audio_path=self.filename['text']
			message=self.message.getText()
			password=self.Password.get()
			if len(password)>5:
				self.messageBox("ERROR ALERT", "The max password size is 5")
				self.encrypt['state']='normal'
				return
			if len(message)>500:
				self.messageBox("ERROR ALERT", "The max message length is 500")
				self.encrypt['state']='normal'
				return
			
			# opening audio file using wave module (here W)			
			au=W.open(audio_path, 'rb')
			ln=au.getnframes()-44
			data=au.readframes(ln)
			
			# extracting data from file into a list
			dataT=[ord(byte) for byte in data]
			n=2**int(float(log(ln,2))/2)
			
			# checking if audio file is large enough to encode message
			if len(message)>(ln)/8:
				self.messageBox("ERROR ALERT", "You have exceeded the maximum message size supported by the current audio file")
				self.encrypt['state']='normal'
				return
			
			# generating initial location to begin encoding
			key = keygen(n)

			# this traverse function is a one-to-one mapping from (0,n*n) to (0, n*n) using the Hilbert curve.
			def traverse2(ct):
				x,y=dtoxy(n,ct)
				return n*x+y
			
			ct=traverse2(key)+44
			# modifying file's data in list according to message
			for index in range(len(message)):
				ch=message[index]
				asc=ord(ch)
				
				# asc_bin is a string containing binary value of the character.
				asc_bin="%08d" % int(bin(asc)[2:])
				for i in range(8):
					dataT[ct]=change(dataT[ct],int(asc_bin[i]))
					key=(key+1)%n
					# moving to next location
					ct=traverse2(key)+44

			# creating a new file and storing modified data
			s='en'+basename(audio_path)
			out = W.open(s, "wb")
			out.setparams(au.getparams())
			
			# data in an audio file is in hexadecimal in terms of frames.
			dataT=[struct.pack('h',a)[0] for a in dataT]
			out.writeframes("".join(dataT))
			self.hint['text']='Audio file generated'
			self.filename['text']=''
			au.close()
			out.close()

			au.close()
		
if __name__ == "__main__":
	Encryptor().mainloop()