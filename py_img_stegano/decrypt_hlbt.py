from breezypythongui import EasyFrame
from math import log
from tkFileDialog import askopenfilename
from PIL import Image
class Decryptor(EasyFrame):
	def __init__(self):
		EasyFrame.__init__(self,title='Decryptor',width = 600,height=300,resizable=False)
		self.addLabel(text = "Welcome to the Decryptor", row = 0, column = 0, columnspan = 2)
		self.addLabel(text="Decrypted message : ", row=1, column=0)
		self.message=self.addLabel(text='',row=1,column=1)
		self.addLabel(text="Enter the Password : ", row=2, column=0)
		self.Password=self.addTextField('',row=2,column=0, width=20)
		self.addLabel(text="Select the Image : ", row=3, column=0)
		self.filename=self.addLabel(text="", row=3, column=1)
		self.browse=self.addButton(text="Browse",row=4, column=1,command=self.Browse)
		self.decrypt=self.addButton(text='Decrypt',row=5,column=0,state='disabled',command=self.Decrypt)
		self.hint=self.addLabel(text="Awaiting input.......", row=5,column=1)

	def Browse(self):
		filetypes = [("Image files", "*.png")]
        	fileName =askopenfilename(parent = self,filetypes = filetypes)
		self.filename['text']=fileName
		self.hint['text']='Awaiting input.......'
		self.decrypt['state']='normal'
		self.message['text']=''

	def Decrypt(self):
		self.decrypt['state']='disabled'
		password = self.Password.getText()
		#write the code for image processing#######################

		im=Image.open(self.filename['text'])
		pix=im.load()
		width,height=im.size
		
		key = 0		
		for i in range(len(password)):
			ch=password[i]
			asc=ord(ch)
			key += key + asc*(pow(33,i))
			key = key% (width*height)
		key = key%(width*height)
		#print(key)
		ctr=0
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
		flag=1
		mess=''
		while flag==1:
			ascii=''
			for i in range(0,3):
				for j in range(0,3):
					pixel=pix[x,y]
					if i==2 and j==2:
						if pixel[2]%2==1:
							flag=0
							break
					else:
						if pixel[j]%2==0:
							ascii+='0'
						else:
							ascii+='1'
					#x,y=traverse(x,y)
					ctr+=1
					x,y=traverse2(ctr+key)
					
			ascii_int=int(ascii,2)
			mess+=chr(ascii_int)

		###########################################################		
		self.hint['text']='Image file decrypted'
		self.filename['text']=''
		self.message['text']=mess
if __name__ == "__main__":
	Decryptor().mainloop()
