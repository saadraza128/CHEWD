from pymol import cmd, plugins, CmdException, stored
import pymol
import sys
if sys.version_info[0] < 3:
    import Tkinter
    from Tkinter import LEFT, RIGHT
    from Tkinter import *
    import tkMessageBox
else:
    import tkinter as Tkinter
    from tkinter import LEFT, RIGHT
    from tkinter import *
    from tkinter import messagebox as tkMessageBox
import os
import re
from ttk import Frame, Button, Style, Label, Entry
import tkFileDialog
import subprocess
import tempfile
from time import time, localtime, strftime
import platform



load=0
prev="1"
prevz="5.0"
dr1=1
dr2=1
dr3=1


def __init_plugin__(self=None):
    plugins.addmenuitem('CHEWD', mainDialog)
#def __init__(self):
 #   self.menuBar.addmenuitem('Plugin', 'command','CHEWD', label = 'CHEWD',command = lambda : mainDialog())
    #plugins.addmenuitem('CHEWD',mainDialog)

class ToolTip( Toplevel ):

    def __init__( self, wdgt, msg):
   
        self.wdgt = wdgt
        self.parent = self.wdgt.master                                          # The parent of the ToolTip is the parent of the ToolTips widget
        Toplevel.__init__( self, self.parent, bg='black', padx=1, pady=1 )      # Initalise the Toplevel
        self.withdraw()                                                         # Hide initially
        self.overrideredirect( True )                                           # The ToolTip Toplevel should have no frame or title bar
        self.msgVar = StringVar()                                               # The msgVar will contain the text displayed by the ToolTip        
        self.msgVar.set( msg )
        self.delay = 1.5
        self.follow = True
        self.visible = 0
        self.lastMotion = 0
        Message( self, textvariable=self.msgVar, bg='#FFFFDD',
                 aspect=1000 ).grid()                                           # The test of the ToolTip is displayed in a Message widget
        self.wdgt.bind( '<Enter>', self.spawn, '+' )                            # Add bindings to the widget.  This will NOT override bindings that the widget already has
        self.wdgt.bind( '<Leave>', self.hide, '+' )
        self.wdgt.bind( '<Motion>', self.move, '+' )
        
    def spawn( self, event=None ):

        self.visible = 1
        self.after( int( self.delay * 1000 ), self.show )                       # The after function takes a time argument in miliseconds
        
    def show( self ):

        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()
            
    def move( self, event ):

        self.lastMotion = time()
        if self.follow == False:                                                # If the follow flag is not set, motion within the widget will make the ToolTip dissapear
            self.withdraw()
            self.visible = 1
        self.geometry( '+%i+%i' % ( event.x_root+10, event.y_root+10 ) )        # Offset the ToolTip 10x10 pixes southwest of the pointer
        try:
            self.msgVar.set( self.msgFunc() )                                   # Try to call the message function.  Will not change the message if the message function is None or the message function fails
        except:
            pass
        self.after( int( self.delay * 1000 ), self.show )
            
    def hide( self, event=None ):

        self.visible = 0
        self.withdraw()

class CHEWD(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)            
        self.parent = parent
        self.initUI()
        self.selection=""
        self.pdb=""
    
    def initUI(self):
        self.parent.title("CHemical Energy Wise Decomposition")
        frame4 = Frame(self.parent)
        frame4.grid(row=0, column=0,sticky="nsew")
        self.wat=IntVar()
        self.wat.set(1)
        self.waterswap = Checkbutton(frame4, text="Water Swap",  command=self.optionws,variable=self.wat)
        self.waterswap.grid(row=0,column=0)
        self.lig=IntVar()
        self.lig.set(0)
        self.ligandswap = Checkbutton(frame4, text="Ligand Swap",  command=self.optionls,variable=self.lig)
        self.ligandswap.grid(row=0,column=1)
        self.mm=IntVar()
        self.mm.set(0)
        self.mmpbsa = Checkbutton(frame4, text="MMPBSA",  command=self.optionmm,variable=self.mm)
        self.mmpbsa.grid(row=0,column=2)
        
        frame1 = Frame(self.parent)
        frame1.grid(row=1, column=0,sticky="nsew")         
        lbl1 = Label(frame1, text="Log file folder", width=12)
        lbl1.grid(row=0,column=0)       
        self.entry1 = Entry(frame1)
        self.entry1.grid(row=0,column=1,columnspan=4, sticky=W+E)
        self.browserButton = Button(frame1, text = "Browser", command=self.onOpen)
        self.browserButton.grid(row=0,column=5,sticky="e")          
        
        lbl2 = Label(frame1, text="MMPBSA log file", width=12)
        lbl2.grid(row=1,column=0)       
        self.entry2 = Entry(frame1,state=DISABLED)
        self.entry2.grid(row=1,column=1,columnspan=4, sticky=W+E)
        self.browserButtonMM = Button(frame1, text = "Browser", command=self.onOpenMM,state=DISABLED)
        self.browserButtonMM.grid(row=1,column=5,sticky="e")
        
        lbl3 = Label(frame1, text="MMPBSA PDB file", width=12)
        lbl3.grid(row=2,column=0)       
        self.entry3 = Entry(frame1,state=DISABLED)
        self.entry3.grid(row=2,column=1,columnspan=4, sticky=W+E)
        self.browserButtonPDB = Button(frame1, text = "Browser", command=self.onOpenPDB,state=DISABLED)
        self.browserButtonPDB.grid(row=2,column=5,sticky="e")
        
        lbl4 = Label(frame1, text="Ligand Name", width=12)
        lbl4.grid(row=3,column=0)       
        self.entry4 = Entry(frame1)
        self.entry4.grid(row=3,column=1)
        self.lblswap = Label(frame1, text="Swap Ligand", width=12,state=DISABLED)
        self.lblswap.grid(row=3,column=2)       
        self.swapentry = Entry(frame1,state=DISABLED)
        self.swapentry.grid(row=3,column=3)
        self.l1v=IntVar()
        self.l1v.set(1)
        self.lig1ck= Checkbutton(frame1, text="Ligand 1",  command=self.changelig1,state=DISABLED,variable=self.l1v)
        self.lig1ck.grid(row=4,column=0)
        self.l2v=IntVar()
        self.l2v.set(0)
        self.lig2ck= Checkbutton(frame1, text="Ligand 2",  command=self.changelig2,state=DISABLED,variable=self.l2v)
        self.lig2ck.grid(row=4,column=2)
        lbl5 = Label(frame1, text="Display Radius", width=12)
        lbl5.grid(row=5,column=0)       
        self.entry5 = Entry(frame1)
        self.entry5.grid(row=5,column=1)
        self.entry5.insert(0,"5.0")
        self.sv=IntVar()
        self.sv.set(0)
        self.surface = Checkbutton(frame1, text="View Surface",  command=self.viewsurface,variable=self.sv)
        self.surface.grid(row=5,column=2)
        self.vl=IntVar()
        self.vl.set(1)
        self.label = Checkbutton(frame1, text="View Label",  command=self.viewlabel,variable=self.vl)
        self.label.grid(row=5,column=3)
        
        lbl6 = Label(frame1, text="Min Value", width=12)
        lbl6.grid(row=6,column=0)       
        self.entry6 = Entry(frame1)
        self.entry6.grid(row=6,column=1)
        self.entry6.insert(0,"-5")
        lbl7 = Label(frame1, text="Max Value", width=12)
        lbl7.grid(row=6,column=2)      
        self.entry7 = Entry(frame1)
        self.entry7.grid(row=6,column=3)
        self.entry7.insert(0,"+5")
        
        lbl8 = Label(frame1, text="Starting log file", width=12)
        lbl8.grid(row=7,column=0)       
        self.entry8 = Entry(frame1)
        self.entry8.grid(row=7,column=1)
        self.entry8.insert(0,"400")
        lbl9 = Label(frame1, text="Ending log file", width=12)
        lbl9.grid(row=7,column=2)      
        self.entry9 = Entry(frame1)
        self.entry9.grid(row=7,column=3)
        self.entry9.insert(0,"1000")
        
        frame2 = Frame(self.parent)
        frame2.grid(row=2, column=0,sticky="nsew")
        self.vsb = Scrollbar(frame2,orient="vertical", command=self.OnVsb)
        self.vsb.grid(row=1,column=3,sticky="ns")
        self.lb1 = Listbox(frame2,yscrollcommand=self.vsb.set)
        self.lb1.grid(row=1,column=0)
        self.lb2 = Listbox(frame2,yscrollcommand=self.vsb.set)
        self.lb2.grid(row=1,column=1)
        self.lb3 = Listbox(frame2,yscrollcommand=self.vsb.set)
        self.lb3.grid(row=1,column=2)
        
        self.b1 = Button(frame2, text="Residue Number",state=DISABLED,command=lambda: self.sortdata(0))
        self.b1.grid(row=0,column=0,sticky=W+E)
        self.b2 = Button(frame2, text="Residue Name",state=DISABLED,command=lambda: self.sortdata(1))
        self.b2.grid(row=0,column=1,sticky=W+E)
        self.b3 = Button(frame2, text="Energy Value",state=DISABLED,command=lambda: self.sortdata(2))
        self.b3.grid(row=0,column=2,sticky=W+E)
        
        OS = platform.system()       
        if(OS== "Linux"):
            self.lb1.bind("<<ListboxSelect>>", self.OnSelect)
            self.lb1.bind("<4>", self.OnMouseWheel)
            self.lb1.bind("<5>", self.OnMouseWheel)
            self.lb2.bind("<<ListboxSelect>>", self.OnSelect)
            self.lb2.bind("<4>", self.OnMouseWheel)
            self.lb2.bind("<5>", self.OnMouseWheel)
            self.lb3.bind("<<ListboxSelect>>", self.OnSelect)
            self.lb3.bind("<4>", self.OnMouseWheel)
            self.lb3.bind("<5>", self.OnMouseWheel)
        else:
            self.lb1.bind("<<ListboxSelect>>", self.OnSelect)
            self.lb1.bind("<MouseWheel>", self.OnMouseWheel)
            self.lb2.bind("<<ListboxSelect>>", self.OnSelect)
            self.lb2.bind("<MouseWheel>", self.OnMouseWheel)
            self.lb3.bind("<<ListboxSelect>>", self.OnSelect)
            self.lb3.bind("<MouseWheel>", self.OnMouseWheel)
        
        frame3 = Frame(self.parent)
        frame3.grid(row=3, column=0,sticky="nsew")
        
        self.previous = Button(frame3, text="Previous Frame",state=DISABLED,command=self.prevframe)
        self.previous.grid(row=0,column=0,sticky=W+E)
        self.scale = Scale(frame3,command=self.onScale,state=DISABLED,orient=HORIZONTAL,length=320,showvalue=0)
        self.scale.grid(row=0,column=1, sticky=W+E)
        self.next = Button(frame3, text="Next Frame",state=DISABLED,command=self.nextframe)
        self.next.grid(row=0,column=2,sticky=W+E)

        self.var = IntVar()
        v = 000
        self.var.set( v)
        self.label = Label(frame3, text=0, textvariable=self.var)        
        self.label.grid(row=0,column=3)
        self.ApplyButton = Button(frame3, text = "Apply", command=self.Apply)
        self.ApplyButton.grid(row=1,column=3,sticky="e")
        

            
        ToolTip( lbl1, "Load the result directory of Sire Analysis")
        ToolTip( self.browserButton, "Load the result directory of Sire Analysis")
        ToolTip(lbl4,"Enter the name of the Ligand in your coordinate file")
        ToolTip(lbl5,"The radially distributed zone around ligand you want to be displayed")
        ToolTip(lbl6, "Minimum scale value for the color distribution and it will be treated as blue")
        ToolTip(lbl7, "Maximum scale value for the color distribution and it will be treated as red")    
   
    def wsvisualizer(self,index,lig,zone,min,max,label):
        cmd.hide("all")
        x=cmd.get_names("all")
        cmd.show("cartoon","bo. "+ x[index])
        cmd.show("sticks",x[index]+" and r. "+ lig)
        cmd.color("white",x[index] +" and pol.")
        fp=open(tempfile.gettempdir()+"/temp.txt", "r")
        #tt=0
        stored.bfact=[]
        for line in fp:
            stored.bfact.append(line)
            #print(stored.bfact[tt]+"\t"+line+"\t"+str(tt))
            #tt=tt+1
        #print(tt)
        fp.close()
        cmd.alter(x[index],"b=stored.bfact.pop(0)")
        cmd.spectrum("b","blue_white_red",x[index],minimum=min,maximum=max)
        cmd.ramp_new("ramp_obj",x[index],range=[min,0,max],color="[blue, white, red ]")
        cmd.util.cbaw(x[index] + " and r. " +lig)
        cmd.show("licorice","( " +x[index] +" and (r. "+lig+" a. "+zone+") ) and (not ("+ x[index] +" and (r. SWT or r. BWT or r. SWP))) ")
        self.togglelabelws(label,index,lig,zone)
    def lsvisualizer(self,index,lig,zone,min,max,hlig,label):
        cmd.hide("all")
        x=cmd.get_names("all")
        cmd.show("cartoon","bo. "+ x[index])
        cmd.show("sticks",x[index]+" and r. "+ lig)
        cmd.color("white",x[index] +" and pol.")
        fp=open(tempfile.gettempdir()+"/temp.txt", "r")
        stored.bfact=[]
        for line in fp:
            stored.bfact.append(line)
        fp.close()
        cmd.alter(x[index],"b=stored.bfact.pop(0)")
        cmd.spectrum("b","blue_white_red",x[index],minimum=min,maximum=max)
        cmd.ramp_new("ramp_obj",x[index],range=[min,0,max],color="[blue, white, red ]")
        cmd.util.cbaw(x[index] + " and r. " +lig)
        cmd.show("licorice","( " +x[index] +" and (r. "+lig+" a. "+zone+") ) and (not ("+ x[index] +" and (r. SWT or r. BWT or r. SWP))) ")
        cmd.hide("licorice",x[index]+" and r. "+ hlig)
        self.togglelabells(label,index,lig,zone,hlig)

 
        
    def wsupdateview(self,lig,zone,min,max,prev,index,label):
        cmd.hide("all")
        x=cmd.get_names("all")
        cmd.label("( " +x[index] +" and (r. "+lig+" a. "+prev+") ) and (not ("+ x[index] +" and (r. SWT or r. BWT or r. SWP))) " +" and name CA","\" \"")
        cmd.show("cartoon","bo. "+ x[index])
        cmd.show("sticks",x[index]+" and r. "+ lig)
        cmd.color("white",x[index] +" and pol.")
        fp=open(tempfile.gettempdir()+"/temp.txt", "r")
        #tt=0
        stored.bfact=[]
        for line in fp:
            stored.bfact.append(line)
            #print(stored.bfact[tt]+"\t"+line+"\t"+str(tt))
            #tt=tt+1
        #print(tt)
        fp.close()
        cmd.alter(x[index],"b=stored.bfact.pop(0)")
        cmd.spectrum("b","blue_white_red",x[index],minimum=min,maximum=max)
        cmd.ramp_new("ramp_obj",x[index],range=[min,0,max],color="[blue, white, red ]")
        cmd.util.cbaw(x[index] + " and r. " +lig)
        cmd.show("licorice","( " +x[index] +" and (r. "+lig+" a. "+zone+") ) and (not ("+ x[index] +" and (r. SWT or r. BWT or r. SWP))) ")
        self.togglelabelws(label,index,lig,zone)
    def lsupdateview(self,lig,zone,min,max,prev,index,hlig,label):
        cmd.hide("all")
        x=cmd.get_names("all")
        cmd.label("( " +x[index] +" and (r. "+lig+" a. "+prev+") ) and (not ("+ x[index] +" and (r. SWT or r. BWT or r. SWP))) " +" and name CA","\" \"")
        cmd.show("cartoon","bo. "+ x[index])
        cmd.show("sticks",x[index]+" and r. "+ lig)
        cmd.color("white",x[index] +" and pol.")
        fp=open(tempfile.gettempdir()+"/temp.txt", "r")
        
        stored.bfact=[]
        for line in fp:
            stored.bfact.append(line)
        
        fp.close()
        cmd.alter(x[index],"b=stored.bfact.pop(0)")
        cmd.spectrum("b","blue_white_red",x[index],minimum=min,maximum=max)
        cmd.ramp_new("ramp_obj",x[index],range=[min,0,max],color="[blue, white, red ]")
        cmd.util.cbaw(x[index] + " and r. " +lig)
        cmd.show("licorice","( " +x[index] +" and (r. "+lig+" a. "+zone+") ) and (not ("+ x[index] +" and (r. SWT or r. BWT or r. SWP))) ")
        cmd.hide("licorice",x[index]+" and r. "+ hlig)
        self.togglelabells(label,index,lig,zone,hlig)
        
    
    def wsloadallpdb(self,pdblist,path):
        for x in pdblist:
            cmd.load(path +"/"+ x)
            #print(path +"/"+ x)
        cmd.hide("all")
    def mmloadpdb(self,path):
        cmd.load(path)
    def togglesurface(self,sur):
        x=cmd.get_names("all")
        if(sur):
            cmd.show("surf",x[int(self.scale.get())])
            cmd.set("transparency","0.7")
        else:
            cmd.hide("surf",x[int(self.scale.get())])
    def wslistdisplay(self,prev,cur,index):
        x=cmd.get_names("all")
        cmd.hide("sticks",x[index]+" and i. "+ prev)
        cmd.label(x[index] +" and i. " +prev +" and name CA", "\" \"")
        cmd.show("sticks",x[index]+" and i. "+ cur)
        cmd.label(x[index] +" and i. " +cur +" and name CA", "\"%s %s\"%(resn,resi)")
    
    def togglelabelws(self,label,index,lig,zone):
        global prevz
        x=cmd.get_names("all")
        if(label):
            cmd.label("( " +x[index] +" and (r. "+lig+" a. "+zone+") ) and (not ("+ x[index] +" and (r. SWT or r. BWT or r. SWP))) " +" and name CA","\"%s %s\"%(resn,resi)")
            prevz=self.entry5.get()
        else:
            cmd.label("( " +x[index] +" and (r. "+lig+" a. "+prevz+") ) and (not ("+ x[index] +" and (r. SWT or r. BWT or r. SWP))) " +" and name CA","\" \"")
    def togglelabells(self,label,index,lig,zone,hlig):
        global prevz
        x=cmd.get_names("all")
        if(label):
            cmd.label("( " +x[index] +" and (r. "+lig+" a. "+zone+") ) and (not ("+ x[index] +" and (r. SWT or r. BWT or r. SWP))) " +" and name CA","\"%s %s\"%(resn,resi)")
            cmd.label(x[index]+" and r. "+ hlig +" and name CA","\" \"")
            prevz=self.entry5.get()
        else:
            cmd.label("( " +x[index] +" and (r. "+lig+" a. "+prevz+") ) and (not ("+ x[index] +" and (r. SWT or r. BWT or r. SWP))) " +" and name CA","\" \"")
    def viewlabel(self):
        if(load>0):
            if(self.wat.get()==1):
                self.togglelabelws(self.vl.get(),int(self.scale.get()),self.entry4.get(),self.entry5.get())
            elif(self.lig.get()==1):
                if(self.l1v.get()==1):
                    vl = self.entry4.get()
                    hl = self.swapentry.get()
                if(self.l2v.get()==1):
                    vl = self.swapentry.get()
                    hl = self.entry4.get()
                self.togglelabells(self.vl.get(),int(self.scale.get()),vl,self.entry5.get(),hl)
            elif(self.mm.get()==1):
                self.togglelabelws(self.vl.get(),0,self.entry4.get(),self.entry5.get())
    def viewsurface(self):##
        if(load>0):
            self.togglesurface(self.sv.get())
    def optionws(self):
        if(self.wat.get()==1):
            self.lig.set(0)
            self.mm.set(0)
            self.entry1.config(state="normal")
            self.browserButton.config(state="normal")
            self.swapentry.config(state=DISABLED)
            self.lig1ck.config(state=DISABLED)
            self.lig2ck.config(state=DISABLED)
            self.lblswap.config(state=DISABLED) 
            self.entry2.config(state=DISABLED)
            self.entry3.config(state=DISABLED)
            self.browserButtonMM.config(state=DISABLED)
            self.browserButtonPDB.config(state=DISABLED)           
        else:
            self.wat.set(0)
            self.lig.set(1)
            self.mm.set(0)
            self.swapentry.config(state="normal")
            self.lig1ck.config(state="normal")
            self.lig2ck.config(state="normal")
            self.lblswap.config(state="normal")
            self.entry1.config(state="normal")
            self.browserButton.config(state="normal")
            self.entry2.config(state=DISABLED)
            self.entry3.config(state=DISABLED)
            self.browserButtonMM.config(state=DISABLED)
            self.browserButtonPDB.config(state=DISABLED)
            
    def optionls(self):
        if(self.lig.get()==1):
            self.wat.set(0)
            self.mm.set(0)
            self.swapentry.config(state="normal")
            self.lig1ck.config(state="normal")
            self.lig2ck.config(state="normal")
            self.lblswap.config(state="normal")
            self.entry1.config(state="normal")
            self.browserButton.config(state="normal")
            self.entry2.config(state=DISABLED)
            self.entry3.config(state=DISABLED)
            self.browserButtonMM.config(state=DISABLED)
            self.browserButtonPDB.config(state=DISABLED)
        else:
            self.lig.set(0)
            self.mm.set(0)
            self.wat.set(1)
            self.entry1.config(state="normal")
            self.browserButton.config(state="normal")
            self.swapentry.config(state=DISABLED)
            self.lig1ck.config(state=DISABLED)
            self.lig2ck.config(state=DISABLED)
            self.lblswap.config(state=DISABLED)
            self.entry2.config(state=DISABLED)
            self.entry3.config(state=DISABLED)
            self.browserButtonMM.config(state=DISABLED)
            self.browserButtonPDB.config(state=DISABLED)
    def optionmm(self):
        if(self.mm.get()==1):
            self.lig.set(0)
            self.wat.set(0)
            self.swapentry.config(state=DISABLED)            
            self.lig1ck.config(state=DISABLED)
            self.lig2ck.config(state=DISABLED)
            self.lblswap.config(state=DISABLED)
            self.entry8.config(state=DISABLED)
            self.entry9.config(state=DISABLED)
            self.entry1.config(state=DISABLED)
            self.browserButton.config(state=DISABLED)
            self.entry2.config(state="normal")
            self.entry3.config(state="normal")
            self.browserButtonMM.config(state="normal")
            self.browserButtonPDB.config(state="normal")
        else:
            self.wat.set(1)
            self.lig.set(0)
            self.mm.set(0)
            self.entry8.config(state="normal")
            self.entry9.config(state="normal")
            self.entry1.config(state="normal")
            self.browserButton.config(state="normal")
            self.entry2.config(state=DISABLED)
            self.entry3.config(state=DISABLED)
            self.browserButtonMM.config(state=DISABLED)
            self.browserButtonPDB.config(state=DISABLED)
    def changelig1(self):##
        if(self.l1v.get()==1):
            self.l2v.set(0)
        else:
            self.l2v.set(1)
        if(load>0):
            if(self.l1v.get()==1):
                vl = self.entry4.get()
                hl = self.swapentry.get()
            if(self.l2v.get()==1):
                vl = self.swapentry.get()
                hl = self.entry4.get()
            self.lsupdateview(vl,self.entry5.get(),self.entry6.get(),self.entry7.get(),prevz,int(self.scale.get()),hl,self.vl.get())
            
    def changelig2(self):##
        if(self.l2v.get()==1):
            self.l1v.set(0)
        else:
            self.l1v.set(1)
        if(load>0):
            if(self.l1v.get()==1):
                vl = self.entry4.get()
                hl = self.swapentry.get()
            if(self.l2v.get()==1):
                vl = self.swapentry.get()
                hl = self.entry4.get()
            self.lsupdateview(vl,self.entry5.get(),self.entry6.get(),self.entry7.get(),prevz,int(self.scale.get()),hl,self.vl.get())
    def loadmmpbsaresults(self):
        fp=open(self.entry3.get(),"r")
        e=0
        atomcount=0
        resnew=0
        rescount=0
        resnum=list()
        residuename=list()
        resv=list()
        atomnum=list()
        atomnums=list()
        score=list()
        r=""
        rn=""
        for line in fp:
            if e == 2:
                atomnum.append(atomnums)
                break
            t = line.split()
            if line.find('TER') != -1:       
                e = e+1
            if line.find('ATOM')!= -1:
                if(resnew==0):
                    r=t[4]
                    rn=t[3]
                    resnew=1
                    resnum.append(r)
                    residuename.append(rn)
                    score.append(0)
                elif(r!=t[4]):
                    r=t[4]
                    rn=t[3]
                    atomnum.append(atomnums)
                    resnum.append(r)
                    residuename.append(rn)
                    score.append(0)
                    atomnums=list()
                atomnums.append(atomcount)
                atomcount=atomcount+1
        fp.close()
        ll=len(score)
        print(ll)
        resv=list()
        fp = open(self.entry2.get(),"r")
        for line in fp:
            t = line.split(',')
            t2=t[0].split()
            if(len(t)==20 and len(t2)==2 and t2[0]!="LIG"):
                for xx in range (ll):
                    if(int(resnum[xx])==int(t2[1])):
                        #print(str(ll)+"\t"+str(len(t)))
                        score[xx]=float(t[17])
            matchObj = re.match( r'Sidechain Energy Decomposition:', line, re.M|re.I)
            if matchObj:
                break
        fp.close()
        x =len(score)
        data=list()
        for i in range (x):
            data.append([resnum[i],score[i],residuename[i],atomnum[i]])
        data.sort(key = lambda s:(int(s[0])))
        scores=list()
        for i in range(len(data)):
            for j in range(len(data[i][3])):
                scores.append("{0:.3f}".format(data[i][1]))
        fp=open(tempfile.gettempdir()+"/temp.txt", "w")
        xs=len(scores)
        for i in range(xs):
            fp.write(str(scores[i])+"\n")
        fp.close()
        self.lb1.delete(0,END)
        self.lb2.delete(0,END)
        self.lb3.delete(0,END)

        for i in range(x):
            self.lb1.insert(END,data[i][0])
            self.lb2.insert(END,data[i][2])
            self.lb3.insert(END,round(data[i][1],3))
                

        self.b1.config(state="normal")
        self.b2.config(state="normal")
        self.b3.config(state="normal")
 
    def changestate(self):##
        fp=open(self.entry1.get()+"/bound_mobile_000100_0.00500.pdb")
        lend=0
        if(self.wat.get()==1):
            lend=2
        elif(self.lig.get()==1):
            lend=4
        e=0
        atomcount=0
        resnew=0
        rescount=0
        resnum=list()
        residuename=list()
        resv=list()
        atomnum=list()
        atomnums=list()
        score=list()
        r=""
        rn=""
        for line in fp:
            if e == lend:
                atomnum.append(atomnums)
                break
            t = line.split()
            if line.find('TER') != -1:       
                e = e+1
            if line.find('ATOM')!= -1:
                if(resnew==0):
                    r=t[4]
                    rn=t[3]
                    resnew=1
                    resnum.append(r)
                    residuename.append(rn)
                    score.append(0)
                elif(r!=t[4]):
                    r=t[4]
                    rn=t[3]
                    atomnum.append(atomnums)
                    resnum.append(r)
                    residuename.append(rn)
                    score.append(0)
                    atomnums=list()
                atomnums.append(atomcount)
                atomcount=atomcount+1
        fp.close()
        x=list()
        tempx=list()
        ll=len(score)
        base=os.listdir(self.entry1.get())
        for a in base:
            if a.endswith(".log"):
                tempx.append(a)
        tempx.sort()
        tlen=len(tempx)
        ia=int(self.entry8.get())
        while ( ia <= int(self.entry9.get()) and ia < tlen ):
            x.append(tempx[ia])
            ia+=1                
        c=0
        i=0
        for fn in x:
            fp=open(self.entry1.get() + "/" + fn, "r")
            if(c==0):
                for line in fp:
                    t = line.split()
                    if( len(t) == 8):
                        if(t[0] == "Residue("):
                            for xx in range (ll):
                                if(int(resnum[xx])==int(t[3])):
                                    score[xx]=float(t[5])
                    if(line == "PROTEIN BOX WATER FREE ENERGY COMPONENTS\n"):
                        c=c+1
                        i=0
                        break
            else:
                for line in fp:
                    t = line.split()
                    if( len(t) == 8):
                        if(t[0] == "Residue("):
                            for xx in range (ll):
                                if(int(t[3])==int(resnum[xx])):
                                    score[xx]=score[xx] +  float(t[5])
                                i=i+1
                    if(line == "PROTEIN BOX WATER FREE ENERGY COMPONENTS\n"):
                        c=c+1
                        i=0
                        break 
            fp.close()
        x =len(score)
        data=list()
        for i in range (x):
            data.append([resnum[i],score[i],residuename[i],atomnum[i]])
        data.sort(key = lambda s:(int(s[0])))
        for i in range(x) :
            data[i][1]=data[i][1]/c
        scores=list()
        for i in range(len(data)):
            for j in range(len(data[i][3])):
                scores.append("{0:.3f}".format(data[i][1]))
        self.lb1.delete(0,END)
        self.lb2.delete(0,END)
        self.lb3.delete(0,END)

        for i in range(x):
            self.lb1.insert(END,data[i][0])
            self.lb2.insert(END,data[i][2])
            self.lb3.insert(END,round(data[i][1],3))
                
        fp=open(tempfile.gettempdir()+"/temp.txt", "w")
        lx=len(scores)
        for i in range(lx):
            fp.write(str(scores[i])+"\n")
        fp.close()
        self.b1.config(state="normal")
        self.b2.config(state="normal")
        self.b3.config(state="normal")
    
    def prevframe(self):
        global prevz,load
        if(load>0):
            self.scale.set(self.scale.get()-1)
            
    def nextframe(self):
        global prevz,load
        if(load>0):
            self.scale.set(self.scale.get()+1)
            
    def onScale(self, val):
        global prevz,load
        if (load>0):                
            v = self.lig1pdb[int(float(val))][14:19]
            self.var.set( v)
            if(self.scale.get()==0):
                self.previous.config(state=DISABLED)
            if(self.scale.get()==len(self.lig1pdb)-2):
                self.next.config(state="normal")
            if(self.scale.get()==1):
                self.previous.config(state="normal")
            if(self.scale.get()==len(self.lig1pdb)-1):
                self.next.config(state=DISABLED)
            if(self.wat.get()==1):
                self.wsupdateview(self.entry4.get(),self.entry5.get(),self.entry6.get(),self.entry7.get(),prevz,int(self.scale.get()),self.vl.get())
            elif(self.lig.get()==1):
                if(self.l1v.get()==1):
                    vl = self.entry4.get()
                    hl = self.swapentry.get()
                if(self.l2v.get()==1):
                    vl = self.swapentry.get()
                    hl = self.entry4.get()
                self.lsupdateview(vl,self.entry5.get(),self.entry6.get(),self.entry7.get(),prevz,int(self.scale.get()),hl,self.vl.get())
    def OnSelect(self,val):
        global prev
        sender = val.widget
        idx = sender.curselection()
        if(idx!=()):
            dis = self.lb1.get(idx)
            if(self.wat.get()==1 or self.lig.get()==1):
                self.wslistdisplay(prev,dis,int(self.scale.get()))
            elif(self.mm.get()==1):
                self.wslistdisplay(prev,dis,0)
            prev=dis
    
    def sortdata(self,sc):
        global dr1,dr2,dr3
        tableData1 = self.lb1.get(0,END)
        tableData2 = self.lb2.get(0,END)
        tableData3 = self.lb3.get(0,END)
        
        data = list()        
        nv = len(tableData1)                        
        for x in range(nv):
            data.append([tableData1[x],tableData2[x],tableData3[x]])
        
        if(sc==0):
            lab = self.b1.cget('text')
            if lab[0]=='[': self.b1.config(text=lab[4:])
            lab = self.b2.cget('text')
            if lab[0]=='[': self.b2.config(text=lab[4:])
            lab = self.b3.cget('text')
            if lab[0]=='[': self.b3.config(text=lab[4:])
            lab = self.b1.cget('text')
            if dr1==1: self.b1.config(text='[+] ' + lab) 
            else: self.b1.config(text='[-] ' + lab)
            data.sort(key = lambda s: ( int(s[sc])),reverse=dr1==1)
            dr1=dr1*-1
        if(sc==1):
            lab = self.b1.cget('text')
            if lab[0]=='[': self.b1.config(text=lab[4:])
            lab = self.b2.cget('text')
            if lab[0]=='[': self.b2.config(text=lab[4:])
            lab = self.b3.cget('text')
            if lab[0]=='[': self.b3.config(text=lab[4:])
            lab = self.b2.cget('text')
            if dr2==1: self.b2.config(text='[+] ' + lab) 
            else: self.b2.config(text='[-] ' + lab)
            data.sort(key = lambda s: ( s[sc]),reverse=dr2==1)
            dr2=dr2*-1
        if(sc==2):
            lab = self.b1.cget('text')
            if lab[0]=='[': self.b1.config(text=lab[4:])
            lab = self.b2.cget('text')
            if lab[0]=='[': self.b2.config(text=lab[4:])
            lab = self.b3.cget('text')
            if lab[0]=='[': self.b3.config(text=lab[4:])
            lab = self.b3.cget('text')
            if dr3==1: self.b3.config(text='[+] ' + lab) 
            else: self.b3.config(text='[-] ' + lab)
            data.sort(key = lambda s: ( float(s[sc])),reverse=dr3==1)
            dr3=dr3*-1
        nv = len(data)
        self.lb1.delete(0,'end')
        self.lb2.delete(0,'end')
        self.lb3.delete(0,'end')
        for x in range(nv):
            self.lb1.insert(END,data[x][0])
            self.lb2.insert(END,data[x][1])
            self.lb3.insert(END,data[x][2])
            
                 
    def onOpen(self):
        global load
        fold = tkFileDialog.askdirectory()
        self.entry1.delete(0, 'end')
        self.entry1.insert(0,fold)
        load=0
    def onOpenMM(self):
        global load
        fold = tkFileDialog.askopenfilename()
        self.entry2.delete(0, 'end')
        self.entry2.insert(0,fold)
        load=0
    def onOpenPDB(self):
        global load
        fold = tkFileDialog.askopenfilename()
        self.entry3.delete(0, 'end')
        self.entry3.insert(0,fold)
        load=0
    def OnVsb(self, *args):
        self.lb1.yview(*args)
        self.lb2.yview(*args)
        self.lb3.yview(*args)
 
    def OnMouseWheel(self, event):
        self.lb1.yview("scroll",event.delta,"units")
        self.lb2.yview("scroll",event.delta,"units")
        self.lb3.yview("scroll",event.delta,"units")     
        return "break"
    def Apply(self):
        global load,prevz
        if(load==0):
                            
            if(self.wat.get()==1 or self.lig.get()==1):
                self.changestate()
                self.base=os.listdir(self.entry1.get())
                pdb1=list()
                for a in self.base:
                    matchObj = re.match( r'bound_mobile_\d{6}_0\.\d{5}\.pdb', a, re.M|re.I)
                    if matchObj:
                        pdb1.append(a)
                self.lig1pdb=list()    
                self.lig2pdb=list()
                x = pdb1[1][22:27]
                 
                for a in pdb1:
                   
                    matchObj = re.match( r'bound_mobile_\d{6}_0\.'+x+'.pdb', a, re.M|re.I)
                    if matchObj:
                        self.lig1pdb.append(a)
                    else:
                        self.lig2pdb.append(a)
                self.lig1pdb.sort()
                self.lig2pdb.sort()
                self.scale.configure(from_=0,to=len(self.lig1pdb) -1)
                self.scale.config(state="normal")
                
            elif(self.mm.get()==1):
                self.loadmmpbsaresults()
                self.mmloadpdb(self.entry3.get())
                self.wsvisualizer(0, self.entry4.get(),self.entry5.get(),self.entry6.get(),self.entry7.get(),self.vl.get())
            
            if(self.wat.get()==1):
                self.wsloadallpdb(self.lig1pdb,self.entry1.get())
                self.next.config(state="normal")
                v = self.lig1pdb[0][14:19]
                self.var.set( v)
                self.wsvisualizer(int(self.scale.get()),self.entry4.get(),self.entry5.get(),self.entry6.get(),self.entry7.get(),self.vl.get())
            elif(self.lig.get()==1):
                if(self.l1v.get()==1):
                    vl = self.entry4.get()
                    hl = self.swapentry.get()
                if(self.l2v.get()==1):
                    vl = self.swapentry.get()
                    hl = self.entry4.get()
                self.wsloadallpdb(self.lig1pdb,self.entry1.get())
                self.next.config(state="normal")
                v = self.lig1pdb[0][14:19]
                self.var.set(v)
                self.lsvisualizer(int(self.scale.get()),vl,self.entry5.get(),self.entry6.get(),self.entry7.get(),hl,self.vl.get())
            load=1
            
        else: #old code "else:"
            
            if(self.wat.get()==1):
                self.wsupdateview(self.entry4.get(),self.entry5.get(),self.entry6.get(),self.entry7.get(),prevz,int(self.scale.get()),self.vl.get())
            elif(self.lig.get()==1):
                if(self.l1v.get()==1):
                    vl = self.entry4.get()
                    hl = self.swapentry.get()
                if(self.l2v.get()==1):
                    vl = self.swapentry.get()
                    hl = self.entry4.get()
                
                self.lsupdateview(vl,self.entry5.get(),self.entry6.get(),self.entry7.get(),prevz,int(self.scale.get()),hl,self.vl.get())
            elif(self.mm.get()==1):
                self.wsupdateview(self.entry4.get(),self.entry5.get(),self.entry6.get(),self.entry7.get(),prevz,0,self.vl.get())
        prevz=self.entry5.get()
def mainDialog():
    app = plugins.get_pmgapp()
    root = plugins.get_tk_root()
    self = Tkinter.Toplevel(root)
    self.title('CHemical Energy Wise Decomposition')
    self.minsize(250, 0)
    self.resizable(0,0)
    CHEWD(self)
    #self.mainloop()  

   
