from breezypythongui import EasyFrame
from math import log
from tkFileDialog import askopenfilename
from PIL import Image
from os.path import basename
from Tkinter import Entry,StringVar
class Encryptor(EasyFrame):
	def __init__(self):
		EasyFrame.__init__(self,title='Encryptor',width = 600,height=300,resizable=False)
		self.addLabel(text = "Welcome to the Encryptor", row = 0, column = 0, columnspan = 2)
		self.addLabel(text = "Enter the message : ", row=1, column=0)
		self.message=self.addTextArea('',row=1,column=1,height=2, width=20,wrap='word')
                self.addLabel(text="Enter the Password : (max size is 10)", row=2, column=0)
		#self.Password=self.addTextField('',row=2,column=0, width=20)
		
		self.Password = StringVar() #Password variable
		passEntry = Entry(self, textvariable=self.Password, show='*').grid(row=2,column=1)
		#self.Password.set(self.Password.get()[:10])

		self.addLabel(text="Select the Image : ", row=3, column=0)
		self.filename=self.addLabel(text="", row=3, column=1)
		self.browse=self.addButton(text="Browse",row=4, column=1,command=self.Browse)
		self.encrypt=self.addButton(text='Encrypt',row=5,column=0,state='disabled',command=self.Encrypt)
		self.hint=self.addLabel(text="Awaiting input.......", row=5,column=1)

		
			

	def Browse(self):
		filetypes = [("Image files", "*.png"),("Image files", "*.bmp")]
        	fileName =askopenfilename(parent = self,filetypes = filetypes)
		self.filename['text']=fileName
		self.hint['text']='Awaiting input.......'
		self.encrypt['state']='normal'

	def Encrypt(self):
		self.encrypt['state']='disabled'
		#write the code for image processing
		
		
		image_path=self.filename['text']
		message=self.message.getText()
		#password = self.Password.getText()
		password=self.Password.get()
		if len(password)>10:
			self.messageBox("ERROR ALERT", "The max password size is 10")
			self.encrypt['state']='normal'
			return
###############################################################
	
		""" assume that image size is sufficient"""
		im=Image.open(image_path)

		pix=im.load()
		width,height=im.size
		if len(message)>(width*height)/3:
			self.messageBox("ERROR ALERT", "You have exceeded the maximum message size supported by the current image, which is "+str((width*height)/3))
			self.encrypt['state']='normal'
			return
		key = 0		
		for i in range(len(password)):
			ch=password[i]
			asc=ord(ch)
			key += key + asc*(pow(33,i))
			key = key%(width * height)
		key = key%(width*height)		
		ct=key
		n=2**min(int(log(width,2)),int(log(height,2)))

		def traverse2(ct):
			return dtoxy(n,ct)
		
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
			
		def rot(n,x,y,rx,ry):
			if ry == 0:
				if rx == 1:
					x = n-1 - x
					y = n-1 - y
					
				x,y = y,x
			return x,y
		
		def traverse(x,y):
			if y<width-1:
				y+=1
			else:
				y=0
				x+=1
			return x,y
		x,y = dtoxy(n,key)
		for index in range(len(message)):
			ch=message[index]
			asc=ord(ch)
			asc_bin="%08d" % int(bin(asc)[2:])
	
			t=0
			for i in range(0,3):
				for j in range(0,3):
					if i==2 and j==2:
						if index==len(message)-1:
							pixel=pix[x,y]
							pix[x,y]=(pixel[0],pixel[1],pixel[2]|1)
						else:
							pixel=pix[x,y]
							if pixel[2]%2==0:
								pix[x,y]=(pixel[0],pixel[1],pixel[2])
							else:
								pix[x,y]=(pixel[0],pixel[1],pixel[2]-1)
					else:
						tostore=int(asc_bin[t])
						if tostore==0:
							pixel=list(pix[x,y])
							if pixel[j]%2==0:
								pixel[j]=pixel[j]
							else:
								pixel[j]=pixel[j]-1
							pix[x,y]=tuple(pixel)
						else:
							pixel=list(pix[x,y])
							pixel[j]=pixel[j]|1
							pix[x,y]=tuple(pixel)
					t+=1
					#x,y=traverse(x,y)
					x,y = traverse2(9*index+3*i+j+1 + key)
		s=basename(image_path)
		im.save('en'+s)
		self.hint['text']='Image file generated'
###############################################################
		self.filename['text']=''
if __name__ == "__main__":
	Encryptor().mainloop()
