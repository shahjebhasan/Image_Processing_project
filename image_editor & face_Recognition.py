#***********************************************IMPORT THE REQUIRED LIBRARIES*****************************************************************************************
from tkinter import *
import tkinter
import random
import time
import datetime
from tkinter import messagebox
import numpy as np
import cv2
from tkinter import filedialog
from PIL import Image,ImageTk

file=None
file_save=None
file_crr=None


root=Tk()
root.geometry("1600x800+0+0")
root.title("Photo Editor")
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
import os
import smtplib
import imghdr
from email.message import EmailMessage

#***********************************************************************DEFINE CLASS AND FUNCTIONS************************************************************************************************

class Tar_Img:
		
	def display(self):
		global file
		global file_crr
		file=filedialog.askopenfilename(initialdir="/",title='select file to open',filetypes=(('all files','.*'),('text files','*.txt')))
		self.imgtk=ImageTk.PhotoImage(Image.open(file))
		canvas1.create_image(20,20,anchor=NW,image=self.imgtk)

	def resize(self):
		global file
		global file_save
		global file_crr
		canvas2.delete(file_crr)
		self.temp=cv2.imread(file)
		self.re_size =cv2.resize(self.temp,(200,300),interpolation=cv2.INTER_LINEAR)
		self.imgtk_re=ImageTk.PhotoImage(Image.fromarray(self.re_size))
		file_crr=canvas2.create_image(20,20,anchor=NW,image=self.imgtk_re)
		file_save=self.re_size

	def cnv_to_gray(self):
		global file
		global file_crr
		global file_save
		canvas2.delete(file_crr)
		self.temp=cv2.imread(file)
		self.img_gray=cv2.cvtColor(self.temp, cv2.COLOR_RGB2GRAY)
		self.imgtk_gray=ImageTk.PhotoImage(Image.fromarray(self.img_gray))
		file_crr=canvas2.create_image(20,20,anchor=NW,image=self.imgtk_gray)
		file_save=self.img_gray

	def cnv_to_hsv(self):
		global file
		global file_save
		global file_crr
		canvas2.delete(file_crr)
		self.temp=cv2.imread(file)
		self.img_hsv=cv2.cvtColor(self.temp,cv2.COLOR_BGR2HSV)
		self.imgtk_hsv=ImageTk.PhotoImage(Image.fromarray(self.img_hsv))
		file_crr=canvas2.create_image(20,20,anchor=NW,image=self.imgtk_hsv)
		file_save=self.img_hsv
		
	def img_translation(self,x,y):
		global file
		global file_save
		global file_crr
		canvas2.delete(file_crr)
		self.temp=cv2.imread(file)
		self.rows,self.cols=self.temp.shape[:2]
		self.M = np.float32([[1,0,-x],[0,1,-y]]) 
		self.dst = cv2.warpAffine(self.temp,self.M,(self.cols,self.rows)) 
		self.imgtk_trans=ImageTk.PhotoImage(Image.fromarray(self.dst))
		file_crr=canvas2.create_image(20,20,anchor=NW,image=self.imgtk_trans)
		file_save=self.dst

	def threshold(self):
		global file
		global file_save
		self.temp=cv2.imread(file)
		self.img_gray=cv2.cvtColor(self.temp,cv2.COLOR_BGR2GRAY)
		ret,thresh1=cv2.threshold(self.temp,127,255,cv2.THRESH_BINARY)
		ret,thresh2=cv2.threshold(self.temp,127,255,cv2.THRESH_BINARY_INV)
		ret,thresh3=cv2.threshold(self.temp,127,255,cv2.THRESH_TRUNC)
		ret,thresh4=cv2.threshold(self.temp,127,255,cv2.THRESH_TOZERO)
		ret,thresh5=cv2.threshold(self.temp,127,255,cv2.THRESH_TOZERO_INV)
		titles=['ORIGINAL IMAGE','Bianry Image','BINARY_INV IMAGE','TRUNC','TOZERO','TOZERO_INV']
		self.images=self.img_gray,thresh1,thresh2,thresh3,thresh4,thresh5
		for i in range(6):
    			plt.subplot(2,3,i+1),plt.imshow(self.images[i],cmap='gray')
    			plt.title(titles[i])
    			plt.xticks([]),plt.yticks([])
		plt.show()

	def edge_detection(self):
		global file
		global file_save
		global file_crr
		canvas2.delete(file_crr)
		self.temp=cv2.imread(file)
		self.edges=cv2.Canny(self.temp,100,200)
		self.imgtk_edges=ImageTk.PhotoImage(Image.fromarray(self.edges))
		file_crr=canvas2.create_image(20,20,anchor=NW,image=self.imgtk_edges)
		file_save=self.edges

	def blur_img(self):
		global file
		global file_save
		global file_crr
		canvas2.delete(file_crr)
		self.temp=cv2.imread(file)
		self.blur=cv2.blur(self.temp,(10,10))
		self.imgtk_blur=ImageTk.PhotoImage(Image.fromarray(self.blur))
		file_crr=canvas2.create_image(20,20,anchor=NW,image=self.imgtk_blur)
		file_save=self.blur

	
	
#****************************************************************DETECT THE FACE ******************************************************************************************************	

	def detect_face(self):
		self.face_cascade=cv2.CascadeClassifier('C:/Users/DELL/Desktop/webskitters/Haarcascades/haarcascade_frontalface_default.xml')
		self.eye_cascade=cv2.CascadeClassifier('C:/Users/DELL/Desktop/webskitters/Haarcascades/haarcascade_Eye.xml')
		global file
		global file_save
		self.img=cv2.imread(file)
		self.img=cv2.resize(self.img,(700,600))
		self.face_img=self.img.copy()
		self.gray=cv2.cvtColor(self.face_img,cv2.COLOR_BGR2GRAY)
		self.faces=self.face_cascade.detectMultiScale(self.gray,1.05,5)
		for (x,y,w,h) in self.faces:
    		   self.image=cv2.rectangle(self.face_img,(x,y),(x+w,y+h),(0,0,255),2)
		  
		self.face_img=ImageTk.PhotoImage(Image.fromarray(self.face_img))
		canvas2.create_image(20,20,anchor=NW,image=self.face_img)
		file_save=self.img
		

	def save_img(self):
		global file_save
		cv2.imwrite('C:\\Users\\DELL\\Desktop\\Image_editor\\Edited.jpg',file_save)

    
	def quitapp(self):
    		self.answer=messagebox.askquestion("Exit","Do You really want to exit")
    		if self.answer=="yes":
        		root.quit()
	
	def about(self):
    		showinfo("Photo Editor","code with shahjeb")

def share_img():
	
	EMAIL_ADDR = 'mlusingpython0@gmail.com'     #sender
	EMAIL_PASS = 'qwerty029'     #password

	msg = EmailMessage()
	msg['Subject'] = 'DETECTED FACES'
	msg['From'] = EMAIL_ADDR
	msg['To'] = 'hasan.shahjeb26@gmail.com'    #receiver
	msg.set_content('Image Attached!!!')

	with open('C:\\Users\\DELL\\Desktop\\Image_editor\\Edited.jpg','rb') as fl:    #enter the full path of the image
  		file_data = fl.read()
  		file_type = imghdr.what(fl.name)
  		file_name = fl.name
  
	msg.add_attachment(file_data, maintype='image',subtype=file_type,filename=file_name)
   
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

  		smtp.login(EMAIL_ADDR, EMAIL_PASS)

  		smtp.send_message(msg)

#***************************************************DEFINE THE FRAMES AND LABELS********************************************************************************************

main_frame=Frame(root,width=1600,height=800,bg='gray16')

localtime=time.asctime(time.localtime(time.time()))

frame1=Frame(main_frame,width=1600,height=800,bg='gray16')
frame1.pack()

lblinfo1=Label(frame1,font=('arial',20,'bold'),text='PHOTO EDITOR',fg='white',bg='gray16',bd=5,relief=SUNKEN,justify=CENTER)
lblinfo1.grid(row=0,columnspan=3)
lblinfo2=Label(frame1,font=('arial',20,'bold'),text=localtime,fg='white',bg='gray16',bd=5,relief=SUNKEN,justify=CENTER)
lblinfo2.grid(row=1,columnspan=3)


canvas1=Canvas(frame1,width=700,height=500,bg='light slate blue',relief=RAISED)
canvas1.grid(row=2,column=0)

canvas2=Canvas(frame1,width=700,height=500,bg='light slate blue',relief=RAISED)
canvas2.grid(row=2,column=1)

frame4=Frame(main_frame,width=1500,height=130,relief=RAISED,bg='gray16')
frame4.pack(side=BOTTOM)

mainmenu=Menu(root)
root.config(menu=mainmenu)
root.title("PHOTO EDITOR")
root.grid_rowconfigure(0,weight=1)
root.grid_columnconfigure(0,weight=1)
root.wm_iconbitmap("")

#********************************************DEFINE THE OBJECT OF CLASS*************************************************************************************************

obj=Tar_Img()

#**************************************************************MENU BAR*************************************************************************************************


filemenu=Menu(mainmenu,tearoff=0)
mainmenu.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label="Open",command=obj.display)
filemenu.add_command(label="Save as",command=obj.save_img)
filemenu.add_command(label="Exit",command=obj.quitapp)

editmenu=Menu(mainmenu,tearoff=0)
mainmenu.add_cascade(label="Edit",menu=editmenu)
editmenu.add_command(label="Resize",command=obj.resize)
editmenu.add_command(label="Gray",command=obj.cnv_to_gray)
editmenu.add_command(label="HSV",command=obj.cnv_to_hsv)
editmenu.add_command(label="Translation",command=lambda: obj.img_translation(-100,-100))
editmenu.add_command(label="Threshold",command=obj.threshold)
editmenu.add_command(label="Edge Detection",command=obj.edge_detection)
editmenu.add_command(label="Blur",command=obj.blur_img)

helpmenu=Menu(mainmenu,tearoff=0)
mainmenu.add_cascade(label="Help",menu=helpmenu)
helpmenu.add_command(label="About",command=obj.about)

#*******************************************************************BUTTON*******************************************************************************************

btn1=Button(frame4,text='Browse',font=('arial',15,'bold'),padx=10,pady=10,bg='gray16',fg='white',justify='right',bd=4,command= obj.display,relief=RAISED)
btn1.grid(row=0,column=0)
btn2=Button(frame4,text='Detect Face',font=('arial',15,'bold'),padx=10,pady=10,bg='gray16',fg='white',justify='right',bd=4,command= obj.detect_face,relief=RAISED)
btn2.grid(row=0,column=2)
btn3=Button(frame4,text='Share',font=('arial',15,'bold'),padx=10,pady=10,bg='gray16',fg='white',justify='right',bd=4,relief=RAISED,command=share_img)
btn3.grid(row=0,column=4)

main_frame.pack(expand=True,fill=BOTH)

#***************************************************************STATUS BAR***********************************************************************************************

status=Label(root,text="Preparing to do nothing....",font="lucida 13 bold",bd=1,relief=SUNKEN,anchor=W)
status.pack(side=BOTTOM,fill=X)
root.mainloop()