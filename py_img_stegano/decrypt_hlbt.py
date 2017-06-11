from breezypythongui import EasyFrame
from breezypythongui import EasyDialog
from math import log
from tkFileDialog import askopenfilename
from PIL import Image
from Tkinter import Entry,StringVar
from random import randint

#in YES store some questions whose answer is a yes
YES=["Does the sun rise in the east?","Do two and two make four?","Is water a five lettered word?","Are there twenty four hours in a day?","Can sunlight generate energy?"]
#in NO store some questions whose answer is a no
NO=["Do we humans have sixteen hands?","Is light a three lettered word?","Is b the first letter of english alphabets?","Do all trees hate sunlight?","Can we drink fire?"]


class Decryptor(EasyFrame):
	def __init__(self):
		EasyFrame.__init__(self,title='Decryptor',width = 1200,height=300,resizable=False)
		self.addLabel(text = "Welcome to the Decryptor", row = 0, column = 0, columnspan = 2)
		self.addLabel(text="Decrypted message : ", row=1, column=0)
		self.message=self.addLabel(text='',row=1,column=1)
		self.addLabel(text="Enter the Password : ", row=2, column=0)
		#self.Password=self.addTextField('',row=2,column=0, width=20)

		self.Password = StringVar() #Password variable
		passEntry = Entry(self, textvariable=self.Password, show='*').grid(row=2,column=1) 
		
		self.addLabel(text="Select the Image : ", row=3, column=0)
		self.filename=self.addLabel(text="", row=3, column=1)
		self.browse=self.addButton(text="Browse",row=4, column=1,command=self.Browse)
		self.decrypt=self.addButton(text='Decrypt',row=5,column=0,state='disabled',command=self.Decrypt)
		self.hint=self.addLabel(text="Awaiting input.......", row=5,column=1)
		self.captcha_ans=["0"]

	def Browse(self):
		filetypes = [("Image files", "*.png"),("Image files", "*.bmp"),]
        	fileName =askopenfilename(parent = self,filetypes = filetypes)
		self.filename['text']=fileName
		self.hint['text']='Awaiting input.......'
		self.decrypt['state']='normal'
		self.message['text']=''

	def Decrypt(self):
		dialog = Captcha(self, self.captcha_ans)
		if dialog.modified()==False or self.captcha_ans[0]=="0":
			self.message['text']="error in captcha"
			return
		self.decrypt['state']='disabled'
		#password = self.Password.getText()
		password=self.Password.get()
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
		self.hint['text']='Program status: Done'
		self.filename['text']=''
		self.message['text']=mess
		self.captcha_ans=["0"]

#For captcha Dialog Box
class Captcha(EasyDialog):
	
	"""Opens a dialog for captcha"""
	def __init__(self, parent,captcha_ans):
		"""Sets up the window."""
		self.gamble=randint(0,1)		
		self.captcha_ans=captcha_ans
		EasyDialog.__init__(self, parent, "Captcha")
    
	def body(self, master):
		#self.question=self.addLabel(master,text = "Select Red", row = 0, column = 0)
		ques=""
		if self.gamble==0:
			ques="No"
		else:
			ques="Yes"
		self.addLabel(master,text = "Select the question whose answer is "+ques, row = 0, column = 0)
		# Add the button group
		self.correct_pos=randint(0,len(YES)-1)
		self.group = self.addRadiobuttonGroup(master,row = 1, column = 0, rowspan = len(YES))
		if self.gamble==0:
			for i in range(0,len(YES)):
				if i==self.correct_pos:
					self.group.addRadiobutton(NO[i])
				else:
					self.group.addRadiobutton(YES[i])
		else:
			for i in range(0,len(YES)):
				if i==self.correct_pos:
					self.group.addRadiobutton(YES[i])
				else:
					self.group.addRadiobutton(NO[i])





		

		# Add the radio buttons to the group
		#self.group.addRadiobutton('Red')
		#self.group.addRadiobutton("Blue")
		#self.group.addRadiobutton("Yellow")
		#self.group.addRadiobutton("Green")

        

	def apply(self):
		"""Transfers data from the fields to the CD."""
		selectedButton = self.group.getSelectedButton()
		if (self.gamble==0 and selectedButton["text"]==NO[self.correct_pos]) or (self.gamble==1 and selectedButton["text"]==YES[self.correct_pos]) :
			self.captcha_ans[0]="1"
		self.setModified()


if __name__ == "__main__":
	Decryptor().mainloop()
