#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 10:01:54 2020

@author: vikash
"""
import tkinter.ttk as ttk
from tkinter import *
from tkcalendar import *
import datetime
import time
from tkinter.ttk import Progressbar
import xlrd
from tkinter import filedialog

#mysql connection
import mysql.connector

global x
mydb = mysql.connector.connect(user='root', database='hiit',passwd='Root@123', auth_plugin='mysql_native_password')
x=mydb.cursor()
global mnWin

#Add Attandace file
class addAtand:
    def __init__(self,root,path):
        self.root=root
        
        self.root.geometry("750x200+450+400")
        self.win=Frame(self.root,background='red')
        self.win.pack(expand=True,fill=BOTH)
        l=Label(self.win,text="Storing Attandance",padx=210,pady=20,font='Arial 24 bold',bg='#352712',fg='white')
        l.grid(row=0,column=0,columnspan=7)
        self.frm=Frame(self.win,background='red')
        self.frm.grid(row=1,column=0,columnspan=7,pady=40,padx=40)
        self.prog=Progressbar(self.frm,orient=HORIZONTAL,length=500,mode='determinate')
        self.prog.pack(padx=20,pady=20)
        if path=="":
            self.bckWin()
         
        self.mydb = mysql.connector.connect(user='root', database='hiit',passwd='Root@123', auth_plugin='mysql_native_password')
        self.x=self.mydb.cursor()
        
        self.workbook=xlrd.open_workbook(path)
        sheet=self.workbook.sheet_by_index(0)
        self.timeTable=['None','7:00AM-8:00AM','8:00AM-9:OOAM','9:00AM-10:00PM','10:00AM-11:00AM','11:00AM-12:00PM','12:00PM-1:00PM','1:00PM-2:00PM','2:00PM-3:00PM','3:00PM-4:00PM','4:00PM-5:00PM','5:00PM-6:00PM']
        self.progval(0,10)
      
        for i in range(1, sheet.nrows):
            ids=int(sheet.cell_value(i,0))
            tim=sheet.cell_value(i,1)
            t=""
            chk="F"
            PA="A"
            if tim!="":
               # PA=PrAbs(tim) 
                a='select batch from members where id = {}'.format(ids)
                self.x.execute(a)
                t=datetime.timedelta(tim)
                for j in self.x:
                    PA=self.PrAbs(tim,j[0])
                    if PA=='P':
                        chk='T'
                    break
            else:
                PA="A"
            dt=sheet.cell_value(i,2)
            dt=xlrd.xldate_as_tuple(dt, 0)
            d=datetime.datetime(*dt)
           
            try:
               
                a='select count(*) from attandance where id = %s and dates = %s'
                b=(ids,d)
                self.x.execute(a,b)
                result=self.x.fetchone()
               
                if(result[0]==0):
                    a='insert into attandance values (%s,%s,%s,%s,%s)'
                    b=(ids,t,d,PA,chk)
                    self.x.execute(a,b)
                    self.mydb.commit()
            except:
               pass
               
        self. progval(0,10)
        messagebox.showinfo(title='information WINDOW', message='Attandance File Add sucessfully')
        self.bckWin()
        self.root.mainloop()
    def bckWin(self):
        self.win.destroy()
        mnWin.show()
    def progval(self,i,n):
        while(i<n):
             self.prog['value']+=5
             self.frm.update_idletasks()
             time.sleep(0.1)
             i+=1
    def PrAbs(self,t,bch):
        
        t=datetime.timedelta(t)
        t=str(t)
        t=t.split(":")
        h=t[0]
        m=t[1]
        s=t[2]
        t=datetime.time(int(h),int(m),int(s))
        tim=-1
        for i in range(6,18):
            ts=datetime.time(i,30,0)
            te=datetime.time(i+1,30,0)
            if(t>=ts and t<=te):
                tim=i-5
                break
                 
        idx=self.timeTable.index(bch)
        if idx==0:
            return "P"
        if(idx==tim):
            return "P"
        
        
        return "A"

#Absent amount fee and data 
class absentFee:
    def __init__(self,root):
         self.mydb = mysql.connector.connect(user='root', database='hiit',passwd='Root@123', auth_plugin='mysql_native_password')
         self.x=self.mydb.cursor()
        
        
         self.newStdWin=root
         self.newStdWin.geometry("750x800+450+100")
         self.newStdWin.title('Main Screen')
         
         self.frm=Frame( self.newStdWin,background='red')
         self.frm.pack()
         self.lbl=Label( self.frm,text='Absent member information ',padx=115,pady=20,font='Arial 24 bold',bg='#352712',fg='white')
         self.lbl.grid(row=0,column=0,columnspan=5)
        
         
        
         self.idL=Label( self.frm,text='Reg ID:',padx=20,pady=5,font='Arial 18 bold',width=5)
         self.idL.grid(row=1,column=0)
         self.idE=Entry( self.frm,font='Arial 24 bold',width=10)
         self.idE.grid(row=1,column=1,pady=20)
        
         self.amtL=Label( self.frm,text='Amount',padx=30,pady=5,font='Arial 18 bold',width=5)
         self.amtL.grid(row=1,column=2)
         self.amtE=Entry( self.frm,font='Arial 24 bold',width=10)
         self.amtE.grid(row=1,column=3,pady=20)
         
         self.fromL=Label( self.frm,text='FROM',padx=20,pady=5,font='Arial 18 bold',width=5)
         self.fromL.grid(row=2,column=0)
         self.fromE=Entry( self.frm,font='Arial 24 bold',width=10)
         self.fromE.grid(row=2,column=1,pady=20)
        
         self.toL=Label( self.frm,text='TO',padx=30,pady=5,font='Arial 18 bold',width=5)
         self.toL.grid(row=2,column=2)
         self.toE=Entry( self.frm,font='Arial 24 bold',width=10)
         self.toE.grid(row=2,column=3,pady=20)
         
         self.clickfrom=Button(self.frm,text='Choose Date',padx=15,pady=15,font='Arial 14 bold',width=10,bg='#6ECF73',fg='white',command=self.calFrom)
         self.clickfrom.grid(row=3,column=0,columnspan=2)
         
         self.clickto=Button(self.frm,text='Choose Date',padx=15,pady=15,font='Arial 14 bold',width=10,bg='#6ECF73',fg='white',command=self.calTo)
         self.clickto.grid(row=3,column=2,columnspan=2)
         
         self.clickCal=Button(self.frm,text='Calculate',padx=30,pady=15,font='Arial 18 bold',width=10,bg='#6ECF73',fg='white',command=self.clickWin)
         self.clickCal.grid(row=4,column=0,columnspan=4,pady=100)
         
         self.f=Frame( self.newStdWin,background='red')
         self.f.pack()
         
         self.paid=Button(self.f,text='Paid',padx=30,pady=15,font='Arial 18 bold',width=10,bg='#6ECF73',fg='white',command=self.paids)
         self.paid.grid(row=0,column=0,pady=100,padx=20)
         
         self.delt=Button(self.f,text='Delete',padx=30,pady=15,font='Arial 18 bold',width=10,bg='#6ECF73',fg='white',command=self.delrec)
         self.delt.grid(row=0,column=1,pady=100,padx=20)
         
         self.bck=Button(self.f,text='Back',padx=30,pady=15,font='Arial 18 bold',width=10,bg='#6ECF73',fg='white',command=self.bckWin)
         self.bck.grid(row=0,column=2,pady=100,padx=20)
         
         
    def delrec(self):
        try:
            a=self.toE.get()
            a=a.split('/')
            d2=datetime.date(int(a[2]), int(a[0]), int(a[1]))
            a=self.fromE.get()
            a=a.split('/')
            d1=datetime.date(int(a[2]), int(a[0]), int(a[1]))
            t=messagebox.askyesno(title='CONFIRM TO DELETE ', message='Are you Sure want to delete the record')
            if t:
                if self.idE.get() !="":
                    a='delete from attandance where dates>=%s and dates<=%s and id=%s'
                    b=(d1,d2,self.idE.get())
                else:
                     a='delete from attandance where dates>=%s and dates<=%s'
                     b=(d1,d2)
               
                k=self.x.execute(a,b)
                self.mydb.commit()
             
                messagebox.showinfo(title='information WINDOW', message='delete record sucessfully')
        except:
            messagebox.showwarning(title='Warning WINDOW', message='Enter dates or id correctly ')
 
    # update amount that are paid
    
    def paids(self):
        try:
            a=self.toE.get()
            a=a.split('/')
            d2=datetime.date(int(a[2]), int(a[0]), int(a[1]))
            a=self.fromE.get()
            a=a.split('/')
            d1=datetime.date(int(a[2]), int(a[0]), int(a[1]))
           
            if id != "":
             
                a='update attandance set chks="T" where dates>%s and dates<%s  and id=%s or id=%s and dates=%s'
                b=(d1,d2,self.idE.get(),self.idE.get(),d2)
           
            self.x.execute(a,b)
            self.mydb.commit()
            messagebox.showinfo(title='information WINDOW', message='payment done sucessfully')
        except:
            messagebox.showwarning(title='Warning WINDOW', message='Enter dates or id correctly ')
        
 # absent window information
  
    def clickWin(self):
        self.abc=Toplevel()
        self.abc.title('absent details')
        self.abc.geometry("670x630+120+150")
        self.swin=Frame(self.abc,background='red')
        self.swin.pack(fill=BOTH,expand=True)
        self.lbl=Label( self.swin,text='Absent informations',padx=200,pady=20,font='Arial 24 bold',bg='#352712',fg='white')
        self.lbl.grid(row=0,column=0,columnspan=3)
        self.idaL=Label( self.swin,text='Reg ID:',padx=20,pady=5,font='Arial 18 bold',width=10)
        self.idaL.grid(row=1,column=0)
        self.idaE=Entry( self.swin,font='Arial 24 bold',width=5)
        self.idaE.grid(row=1,column=1,pady=20)
        
        self.nameL=Label( self.swin,text='Name:',padx=20,pady=5,font='Arial 18 bold')
        self.nameL.grid(row=2,column=0)
        self.nameE=Entry( self.swin,font='Arial 24 bold',width=20)
        self.nameE.grid(row=2,column=1,pady=20)
        
        self.pL=Label( self.swin,text='Total paresent:',padx=20,pady=5,font='Arial 18 bold',width=12)
        self.pL.grid(row=3,column=0)
        self.pE=Entry( self.swin,font='Arial 24 bold',width=5)
        self.pE.grid(row=3,column=1,pady=20)
        
        self.aL=Label( self.swin,text='Total Absent',padx=20,pady=5,font='Arial 18 bold',width=10)
        self.aL.grid(row=4,column=0)
        self.aE=Entry( self.swin,font='Arial 24 bold',width=5)
        self.aE.grid(row=4,column=1,pady=20)
        
        self.abfL=Label( self.swin,text='Absent Amount',padx=20,pady=5,font='Arial 18 bold',width=10)
        self.abfL.grid(row=5,column=0)
        self.abfE=Entry( self.swin,font='Arial 24 bold',width=5)
        self.abfE.grid(row=5,column=1,pady=20)
        
        self.delt=Button(self.swin,text='OK',padx=30,pady=15,font='Arial 18 bold',width=10,bg='#6ECF73',fg='white',command=self.ok)
        self.delt.grid(row=6,column=0,columnspan=2 ,pady=100,padx=20)
        
        
        #insertion coding
        self.idaE.insert(0, self.idE.get())
        a='select name from members where id=%s'
        b=(self.idE.get(),)
        self.x.execute(a,b)
        b=self.x.fetchone()
        self.nameE.insert(0,b[0])
        a=self.toE.get()
        a=a.split('/')
        d2=datetime.date(int(a[2]), int(a[0]), int(a[1]))
        a=self.fromE.get()
        a=a.split('/')
        d1=datetime.date(int(a[2]), int(a[0]), int(a[1]))
        idt=self.idE.get()
        
        
        a='select count(*) from attandance where dates>=%s and dates<=%s and pa= "P" and id=%s  '
        b=(d1,d2,idt)
        self.x.execute(a,b)
        pres=self.x.fetchone()
        self.pE.insert(0,pres[0])
        
        
        a='select count(*) from attandance where dates>=%s and dates<=%s and pa= "A" and id=%s '
        b=(d1,d2,idt)
        self.x.execute(a,b)
        absent=self.x.fetchone()
        self.aE.insert(0,absent[0])
        
        a='select count(*) from attandance where dates>=%s and dates<=%s and chks= "F" and id=%s '
        b=(d1,d2,idt)
        self.x.execute(a,b)
        absent=self.x.fetchone()
        m=self.amtE.get()
        if m=="":
            m=0
        else:
            m=int(m)
        z=m * int(absent[0])
        self.abfE.insert(0,z)
    
    def ok(self):
        self.abc.destroy()
    
    def bckWin(self):
        self.frm.destroy()
        self.f.destroy()  
        mnWin.show()
   
    def calFrom(self):
        self.tp=Toplevel()
        d=datetime.datetime.now()
        self.y=d.year
        self.m=d.month
        self.d=d.day
        self.tp.geometry("230x230+790+250")
        self.cal= Calendar(self.tp, selectmode="day",year=self.y,month=self.m,day=self.d,padx=20,pady=20)
        self.cal.pack(pady=20)

        btn=Button(self.tp, text='OK',command=self.Dateget)
        btn.pack()
   
    def Dateget(self):
        self.fromE.insert(0, self.cal.get_date())
        self.tp.destroy()

    def calTo(self):
        self.tp=Toplevel()
        d=datetime.datetime.now()
        self.y=d.year
        self.m=d.month
        self.d=d.day
        self.tp.geometry("230x230+790+250")
        self.cal= Calendar(self.tp, selectmode="day",year=self.y,month=self.m,day=self.d,padx=20,pady=20)
        self.cal.pack(pady=20)

        btn=Button(self.tp, text='OK',command=self.ToDateget)
        btn.pack()
   
#g et date for To
   
    def ToDateget(self):
        self.toE.insert(0, self.cal.get_date())
        self.tp.destroy()
        

#View Attandace page

class attandaceWin:
    def __init__(self,root):
        self.mydb = mysql.connector.connect(user='root', database='hiit',passwd='Root@123', auth_plugin='mysql_native_password')
        self.x=self.mydb.cursor()
        self.typeVal=StringVar()
        self.typeVal.set('All')
        self.dateVal=StringVar()
        self.dateVal.set('All')
        self.batchVal=StringVar()
        self.timeTable=['All','None','7:00AM-8:00AM','8:00AM-9:OOAM','9:00AM-10:00PM','10:00AM-11:00AM','11:00AM-12:00PM','12:00PM-1:00PM','1:00PM-2:00PM','2:00PM-3:00PM','3:00PM-4:00PM','4:00PM-5:00PM','5:00PM-6:00PM']
        self.batchVal.set(self.timeTable[0])
        self.top=root
        self.top.geometry("750x700+450+100")
        self.top.title('Attandace')
        self.f=ttk.Label(self.top,background='red')
        self.f.pack(fill=BOTH,expand=True)
        self.lbl=Label(self.f,text='View Attandace ',padx=250,pady=20,font='Arial 24 bold',bg='#352712',fg='white')
        self.lbl.grid(row=0,column=0,columnspan=3)
       
        self.typeL=Label( self.f,text='Type:',pady=10,font='Arial 18 bold',width=10)
        self.typeL.grid(row=1,column=0,pady=10)
        self.typeE=OptionMenu( self.f,self.typeVal,'All','Student','Teacher','Staff',command=self.typeCheck)
        
        
        self.batchL=Label( self.f,text='Batch:',pady=10,font='Arial 18 bold',width=10)
        self.batchL.grid(row=1,column=1,pady=10)
        self.batchL=Label( self.f,text='Date:',pady=10,font='Arial 18 bold',width=10)
        self.batchL.grid(row=1,column=2,pady=10)
        
        #typeE.config(width=5)
        self.typeE.config(font='Arial 16 bold')
        self.typeE.grid(row=2,column=0,pady=20,padx=20,sticky = 'w')
        self.batchE=OptionMenu( self.f,self.batchVal, *self.timeTable,command=self.batchCheck)
        self.batchE.config(font='Arial 16 bold')
        self.batchE.grid(row=2,column=1,pady=20,padx=20,sticky='w')
        
        #date choose
        
        self.dateE=OptionMenu( self.f,self.dateVal,'All','Choose',command=self.dateCheck)
        self.dateE.config(font='Arial 16 bold')
        self.dateE.grid(row=2,column=2,pady=20,padx=20,sticky='w')
        
        self.srch=Button(self.f,text='Search',font='Arial 16 bold',command=self.srchStd)
        self.srch.grid(row=3,column=0,columnspan=3, pady=10,padx=20)
        
        #tree formate
        self.tfm=Frame(self.top,background='red')
        self.tfm.pack(expand=True)
        
         #treeScroll bar
        tree_scroll=Scrollbar(self.tfm)
        tree_scroll.pack(side=RIGHT,fill=Y)
        
        self.tree=ttk.Treeview(self.tfm,yscrollcommand=tree_scroll.set)
        
        #cong fscrollbar
        tree_scroll.config(command=self.tree.yview)
        
        #tree Style
        style=ttk.Style()
        style.configure('Treeview' ,font='Arial 12',rowheight=20 )
        
       
        
        #define colums of tree
        self.tree['columns']=('ID','NAME','TYPES','ARRIVAL','P/A','DATE')
        self.tree.column('#0',width=0,stretch=NO)
        self.tree.column('ID',width=80, anchor='center')
        self.tree.column('NAME',width=150,anchor='center')
        self.tree.column('TYPES',width=150,anchor='center')
        self.tree.column('ARRIVAL',width=150,anchor='center')
        self.tree.column('P/A',width=80,anchor='center')
        self.tree.column('DATE',width=150,anchor='center')
        
        #CREATE HEADING
        self.tree.heading('#0', text='',anchor='center')
        self.tree.heading('ID', text='ID',anchor='center')
        self.tree.heading('NAME', text='NAME',anchor='center')
        self.tree.heading('TYPES',text='TYPES',anchor='center')
        self.tree.heading('ARRIVAL', text='ARRIVAL',anchor='center')
        self.tree.heading('P/A', text='P/A',anchor='center')
        self.tree.heading('DATE', text='DATE',anchor='center')
        self.tree.pack()
        # Back Button
        self.abc=Frame(self.top,background='red')
        self.abc.pack(fill=BOTH,expand=True)
        self.bck=Button(self.abc,text="BACK",padx=5,pady=15,font='Arial 18 bold',width=10,bg='#6ECF73',fg='white',command=self.bckWin)
        self.bck.pack(pady=40)
      
    def bckWin(self):
        self.f.destroy()
        self.tfm.destroy()  
        self.bck.destroy()
        self.abc.destroy()
        mnWin.show()
        
    def typeCheck(self,event):
        self.typeVal.set(event)
        
    def batchCheck(self,event):
        self.batchVal.set(event)
   
    def Dateget(self):
        self.dateval=self.cal.get_date()

        self.tp.destroy()
   
    def dateCheck(self,event):
        if(event=='All'):
            self.dateVal.set(event)
        else:
            global tp,cal
            self.tp=Toplevel()
            d=datetime.datetime.now()
            self.y=d.year
            self.m=d.month
            self.d=d.day
            self.tp.geometry("230x230+790+250")
            self.cal= Calendar(self.tp, selectmode="day",year=self.y,month=self.m,day=self.d,padx=20,pady=20)
            self.cal.pack(pady=20)

            btn=Button(self.tp, text='OK',command=self.Dateget)
            btn.pack()
    def srchStd(self):
        if self.dateVal.get()=="All":

            if self.batchVal.get()=='All' and self.typeVal.get()=='All':
                a='select attandance.id, members.name,members.type, time,pa,dates from attandance join members on attandance.id=members.id order by attandance.dates desc'
                self.x.execute(a)
            elif self.typeVal.get()=='All':
                a='select attandance.id, members.name,members.type, time,pa,dates from attandance join members on attandance.id=members.id where members.batch=%s order by attandance.dates desc'
                b=(self.batchVal.get(),)
                self.x.execute(a,b)
            elif self.batchVal.get()=='All':
                a='select attandance.id, members.name,members.type, time,pa,dates from attandance join members on attandance.id=members.id where members.type=%s order by attandance.dates desc'
                b=(self.typeVal.get(),)
                self.x.execute(a,b)
            else:
                a='select attandance.id, members.name,members.type, time,pa,dates from attandance join members on attandance.id=members.id where members.type=%s and members.batch=%s order by attandance.dates desc'
                b=(self.typeVal.get(),self.batchVal.get())
                self.x.execute(a,b)
            
        else:

            s=self.cal.get_date()
            a=s.split('/')
            m=a[0]
            d=a[1]
            y=a[2]
            d=datetime.datetime(int(y), int(m), int(d))
            #self.srchdate=d.strftime('%Y-%d-%m')

            if self.batchVal.get()=='All' and self.typeVal.get()=='All':                
                a='select attandance.id, members.name,members.type, time,pa,dates from attandance join members on attandance.id=members.id where attandance.dates=%s order by attandance.dates'
                b=(d,)
            elif self.batchVal.get()=='All':                
                a='select attandance.id, members.name,members.type, time,pa,dates from attandance join members on attandance.id=members.id where attandance.dates=%s and members.type=%s order by attandance.dates'
                b=(d,self.typeVal.get())
            elif self.typeVal.get()=='All':                
                a='select attandance.id, members.name,members.type, time,pa,dates from attandance join members on attandance.id=members.id where attandance.dates=%s and members.batch=%s  order by attandance.dates'
                b=(d,self.batchVal.get())
            else:                
                a='select attandance.id, members.name,members.type, time,pa,dates from attandance join members on attandance.id=members.id where attandance.dates=%s and members.batch=%s and members.type=%s order by attandance.dates'
                b=(d,self.batchVal.get(), self.typeVal.get())
            self.x.execute(a,b)

        self.tree.delete(*self.tree.get_children())
        j=0
        for i in self.x:
            self.tree.insert(parent='', index='end', iid=j,text='',values=(i[0],i[1],i[2],i[3],i[4],i[5]))
            j=j+1


#Student input update delete class

class newStdWin:
    def __init__(self,root):
    
         self.mydb = mysql.connector.connect(user='root', database='hiit',passwd='Root@123', auth_plugin='mysql_native_password')
         self.x=self.mydb.cursor()
    
         self.typeVal=StringVar()
         self.typeVal.set('Student')
         self.batchVal=StringVar()
         self.timeTable=['None','7:00AM-8:00AM','8:00AM-9:OOAM','9:00AM-10:00PM','10:00AM-11:00AM','11:00AM-12:00PM','12:00PM-1:00PM','1:00PM-2:00PM','2:00PM-3:00PM','3:00PM-4:00PM','4:00PM-5:00PM','5:00PM-6:00PM']
         self.batchVal.set(self.timeTable[0])
         self.newStdWin=root
         self.newStdWin.geometry("750x800+450+100")
         self.newStdWin.title('Main Screen')
         
         self.frm=Frame( self.newStdWin,background='red')
         self.frm.pack(fill=Y,expand=True)
         self.lbl=Label( self.frm,text='Students informations',padx=200,pady=20,font='Arial 24 bold',bg='#352712',fg='white')
         self.lbl.grid(row=0,column=0,columnspan=3)
        
         self.idL=Label( self.frm,text='Reg ID:',padx=20,pady=5,font='Arial 18 bold',width=10)
         self.idL.grid(row=1,column=0)
         self.idE=Entry( self.frm,font='Arial 24 bold')
         self.idE.grid(row=1,column=1,pady=20)
        
         self.nameL=Label( self.frm,text='Name:',padx=20,pady=5,font='Arial 18 bold',width=10)
         self.nameL.grid(row=2,column=0)
         self.nameE=Entry( self.frm,font='Arial 24 bold')
         self.nameE.grid(row=2,column=1,pady=20)
        
         self.typeL=Label( self.frm,text='Type:',padx=20,pady=5,font='Arial 18 bold',width=10)
         self.typeL.grid(row=3,column=0)
         self.typeE=OptionMenu( self.frm,self.typeVal,'Student','Teacher','Staff',command=self.typeCheck)
        #typeE.config(width=5)
         self.typeE.config(font='Arial 16 bold')
         self.typeE.grid(row=3,column=1,pady=20,sticky = 'w')
        
         self.batchL=Label( self.frm,text='Batch:',padx=20,pady=5,font='Arial 18 bold',width=10)
         self.batchL.grid(row=4,column=0)
         self.batchE=OptionMenu( self.frm,self.batchVal, *self.timeTable,command=self.batchCheck)
         self.batchE.config(font='Arial 16 bold')
         self.batchE.grid(row=4,column=1,pady=20,sticky='w')
        
         self.clasL=Label( self.frm,text='Class:',padx=20,pady=5,font='Arial 18 bold',width=10)
         self.clasL.grid(row=5,column=0)
         self.clasE=Entry( self.frm,font='Arial 24 bold',width=20)
         self.clasE.grid(row=5,column=1,pady=20)
        
         self.addL=Label( self.frm,text='Address:',padx=20,pady=5,font='Arial 18 bold',width=10)
         self.addL.grid(row=6,column=0)
         self.addE=Text( self.frm,font='Arial 24 bold',width=20,height=2)
         self.addE.grid(row=6,column=1,pady=20)
         
         self.sub=Button( self.frm,text="Submit",padx=10,pady=5,font='Arial 18 bold',width=10,bg='#6ECF73',fg='white',command=self.subStd)
         self.sub.grid(row=7,column=0,columnspan=3,pady=20)
        
         self.btn=Frame(self.newStdWin,background='#282776')
         self.btn.pack(fill=BOTH)
         self.add=Button(self.btn,text="ADD",padx=5,pady=15,font='Arial 18 bold',width=10,bg='#6ECF73',fg='white',command=self.addStd)
         self.add.grid(row=0,column=0,padx=15,pady=40)
        
         self.updates=Button(self.btn,text="UPDATE",padx=5,pady=15,font='Arial 18 bold',width=10,bg='#6ECF73',fg='white',command=self.upStd)
         self.updates.grid(row=0,column=1,padx=10,pady=40)
    
         self.deletes=Button(self.btn,text="DELETE",padx=5,pady=15,font='Arial 18 bold',width=10,bg='#6ECF73',fg='white',command=self.delStd)
         self.deletes.grid(row=0,column=2,padx=10,pady=40)
         
         self.bck=Button(self.btn,text="BACK",padx=5,pady=15,font='Arial 18 bold',width=8,bg='#6ECF73',fg='white',command=self.bckWin)
         self.bck.grid(row=0,column=3,padx=15,pady=40)
        
    def typeCheck(self,event):
        self.typeVal.set(event)
        
    def batchCheck(self,event):
        self.batchVal.set(event)
    def bckWin(self):
        self.frm.destroy()
        self.btn.destroy()
        mnWin.show()
    
    def addStd(self):
        self.x.execute('select max(id) from members')
        self.idE.config(state='normal')
        a=101
        for i in self.x:
            a=i[0]
        if a==None:
            a=200
        self.idE.delete(0,END)
        self.idE.insert(0,a+1)  
        self.idE.config(state='disabled')
        self.nameE.delete(0,END)
        self.clasE.delete(0,END)
        self.addE.delete(1.0,END)
  
    def delStd(self):
        ids = simpledialog.askstring(title="Delete Record Windows",prompt="Enter Reg ID which you want to delete: ")    
    
        try:
            a='delete from members where id='+ids
            self.x.execute(a)
            self.mydb.commit()
            if self.x.rowcount==1:
                b=messagebox.showinfo(title='information WINDOW', message='delete record sucessfully')
            else:
                 b=messagebox.showinfo(title='information WINDOW', message='Record not found')
        except:
            messagebox.showwarning(title='WARNING WINDOW', message='this ID is not match please enter valid id')
        self.idE.delete(0,END)
        self.nameE.delete(0,END)
        self.clasE.delete(0,END)
        self.addE.delete(1.0,END)
 
    def subStd(self):
        ids=self.idE.get()
        name=self.nameE.get()
        clas=self.clasE.get()
        types=self.typeVal.get()
        add=self.addE.get(1.0,END)
        batch=self.batchVal.get()
 
        try:
            a='select count(*) from members where id='+ids
            self.x.execute(a)
            result=self.x.fetchone()
     
            if result[0]==1:
                a='update members set name=%s,type=%s,clas=%s,batch=%s,ads=%s where id=%s'
                b=(name,types,clas,batch,add,ids) 
        
                self.x.execute(a,b)
                self.mydb.commit()
                messagebox.showinfo(title='information WINDOW', message='Record Updated sucessfully')
               
            else:
                a='insert into members values (%s,%s,%s,%s,%s,%s)'
                b=(ids,name,types,clas,batch,add)
              
                self.x.execute(a,b)
                self.mydb.commit()
                messagebox.showinfo(title='information WINDOW', message='Record inserted sucessfully')
        except:
            messagebox.showwarning(title='warning WINDOW', message='check properly something went wrong')
  
    def upStd(self):
        ids = simpledialog.askstring(title="Update Windows",prompt="Enter Reg ID: ")    
        ids=int(ids)
        try:
            a='select * from members where id = {}'.format(ids)
            self.x.execute(a) 
            a=()
            for i in self.x:
                a=i
                break
      
            self.idE.config(state='normal')
            self.idE.delete(0,END)
            self.idE.insert(0, str(a[0]))
            self.idE.config(state='disabled')
            self.nameE.delete(0,END)
            self.nameE.insert(0, str(a[1]))
            self.clasE.delete(0,END)
            self.clasE.insert(0, a[3])
            self.typeVal.set(a[2])
            self.batchVal.set(a[4])
            self.addE.delete(1.0,END)
            self.addE.insert(1.0,a[5])
        except:
            messagebox.showwarning(title='WARNING WINDOW', message='this ID is not match please enter valid id')
            self.idE.delete(0,END)
            self.nameE.delete(0,END)
            self.clasE.delete(0,END)
            self.addE.delete(1.0,END)


# Main Window dashbord class

class mainWin:  
    def __init__(self,root):
    
        self.top=root
    def show(self):
        self.top.geometry("750x700+450+100")
        self.top.title('Main Screen')
        self.f=ttk.Label(self.top,background='red')
        self.f.pack(fill=BOTH,expand=True)
        self.lbl=Label(self.f,text='Attandace Managment System',padx=150,pady=20,font='Arial 24 bold',bg='#352712',fg='white')
        self.lbl.grid(row=0,column=0,columnspan=3)
        self.addAttend=Button(self.f,text='Add Attandace',padx=20,pady=20,font='Arial 18 bold',bg='#6ECF73',fg='white',command=self.addFile)
        self.addAttend.grid(row=1,column=0,padx=40,pady=80)
        
        self.attandace=Button(self.f,text='view Attandace',padx=20,pady=20,font='Arial 18 bold',bg='#6ECF73',fg='white',command=self.atndnce)
        self.attandace.grid(row=1,column=1,padx=40,pady=80)
        
        self.newStd=Button(self.f,text='Add New Student',padx=20,pady=20,font='Arial 18 bold',bg='#6ECF73',fg='white',command=self.newStds)
        self.newStd.grid(row=2,column=0,columnspan=3,pady=2)
        
        self.absentfee=Button(self.f,text='Check Absent Amount',padx=20,pady=20,font='Arial 25 bold',bg='#6ECF73',fg='white',command=self.abfee)
        self.absentfee.grid(row=3,column=0,columnspan=3,padx=60,pady=80)
        self.top.mainloop()
    def abfee(self):
        self.f.destroy()
        x=absentFee(self.top)
    def atndnce(self):
        self.f.destroy()
        x=attandaceWin(self.top)
    def newStds(self):
        self.f.destroy()
        x=newStdWin(self.top)
    def addFile(self):
        path= filedialog.askopenfilename(title = "Select file",filetypes = (("Excel 2007 onword","*.xlsx"),("Excel 2003","*.xls")))
        if path!="":
            self.f.destroy()
            x=addAtand(self.top,path)

#login page class

class login:
    def __init__(self,root):
        self.root=root
        self.root.geometry("750x700+450+100")
        self.root.title("LogIn Page")
        self.frm=Frame(self.root)
        self.frm.pack(fill=BOTH,expand=True)
        self.bgimg=PhotoImage(file='2.png')
        
        self.login=ttk.Label(self.frm, image=self.bgimg)
        self.login.pack(fill=BOTH,expand=True)
        
        self.Form=Frame(self.login,bg='white')
        self.Form.pack(padx=0,pady=180)
        self.lable=Label(self.Form, text="Enter Username:", fg='black',bg="white", font='Arial 18 bold')
        self.lable.grid(row=0,column=0,pady=50,padx=10)
        self.unE=Entry(self.Form, font='Arial 22 bold')
        self.unE.grid(row=0,column=1,padx=20,pady=50)
        self.pasL=Label(self.Form,text="Enter Password: ", fg='black',bg="white", font='Arial 18 bold')
        self.pasL.grid(row=1,column=0,padx=10,pady=30)
        self.passE=Entry(self.Form,show="*", font='Arial 22 bold')
        self.passE.grid(row=1,column=1,padx=20,pady=30)
        self.sub=Button(self.Form,text="LogIn",font='Arial 22 bold',bg='#6ECF73',fg='white',padx=10,pady=10,command=self.validuser)
        self.sub.grid(row=2,column=0,columnspan=2,padx=10,pady=20)
        self.root.mainloop()
    def validuser(self):
        global mnWin
        u=self.unE.get()
        p=self.passE.get()
        x.execute('select * from login')
        
        ch=0
        for i,j,k in x:
            if u==j and k==p:
                ch=1
                self.frm.destroy()
                mnWin=mainWin(self.root)
                mnWin.show()
          
               
               
        if ch==0:
           messagebox.showwarning(title='WARNING WINDOW', message='Invalid Username or password please Enter valid username or password ')
        

global root
root=Tk()
a=login(root)
