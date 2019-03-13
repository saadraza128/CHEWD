import chimera
from chimera import runCommand as rc

def togglelabelws(label,index,lig,zone):
    if(label):
        rc("rlabel #"+index+ ":" + lig + " za<" + zone)
    else:
        rc("~rlabel #"+index+ ":" + lig + " za<" + zone)
        
def togglelabells(label,index,lig,zone,hlig):
    if(label):
        rc("rlabel #"+index+ ":" + lig + " za<" + zone)
        rc("~rlabel  #"+index +":"+hlig)
    else:
        rc("~rlabel #"+index+ ":" + lig + " za<" + zone)

def togglesurface(sur):
    if(sur):
        rc("surface")
        rc("transparency 70,s")
    else:
        rc("~surface")
        
def loadresults(out):
    rc("defattr " + out+ "/temp.txt raiseTool false")
    
def wslistdisplay(lig,zone,prev,cur,index,label):
    rc("represent stick #"+index+ ":" + str(prev))
    rc("~display #"+index+ ":" + str(prev))
    rc("~rlabel #"+index+ ":" + str(prev))
    rc("display #"+index+ ":" + lig + " za<" +zone)
    rc("~display #"+index+ ":SWT,BWT,SWP")
    togglelabelws(label,index,lig,zone)
    rc("display #"+index+ ":" + str(cur))
    rc("represent bs #"+index+ ":" + str(cur))
    rc("rlabel #"+index+ ":" + str(cur))
    
def wsloadallpdb(pdblist,path):
    for x in pdblist:
        chimera.openModels.open(path +"/"+ x)
    rc("~modeldisplay")
def mmloadpdb(path):
    chimera.openModels.open(path)
    rc("~modeldisplay")
def wsvisualizer(index,out,lig,zone,min,max,label):
    rc("~longbond")    
    rc("color white,s,r")    
    rc("defattr " + out+ "/temp.txt raiseTool false")
    rc("modeldisplay #"+index)
    rc("~display #"+index)
    rc("display #"+index +":"+lig)
    rc("rangecolor sireEnergy " + min + " blue 0 white " + max + " red")
    rc("color byatom #"+index+":" +lig)
    rc("colorkey 0.05,0.15 0.15,0.2 " + min + " blue 0 white " + max + " red")
    rc("display #"+index+ ":" + lig + " za<" +zone)
    rc("~display #"+index+ ":SWT,BWT,SWP")
    togglelabelws(label,index,lig,zone)
def wsupdateview(lig,zone,min,max,prev,index,label):
    rc("~modeldisplay")
    rc("modeldisplay #"+index)
    rc("~display")
    rc("~rlabel #"+index+ ":" + lig + " za<" + prev)
    rc("display #"+index+ ":"+lig)
    rc("rangecolor sireEnergy " + min + " blue 0 white " + max + " red")
    rc("color byatom #"+index+ ":" +lig)
    rc("colorkey 0.05,0.15 0.15,0.2 " + min + " blue 0 white " + max + " red")
    rc("display #"+index+ ":" + lig + " za<" +zone)
    rc("~display #"+index+ ":SWT,BWT,SWP")
    togglelabelws(label,index,lig,zone)
    
def lsvisualizer(index,out,lig,zone,min,max,hlig,label):
    rc("~longbond")    
    rc("color white,s,r")    
    rc("defattr " + out+ "/temp.txt raiseTool false")
    rc("modeldisplay #"+index)
    rc("~display #"+index)
    rc("display #"+index +":"+lig)
    rc("rangecolor sireEnergy " + min + " blue 0 white " + max + " red")
    rc("color byatom #"+index+":" +lig)
    rc("colorkey 0.05,0.15 0.15,0.2 " + min + " blue 0 white " + max + " red")
    rc("display #"+index+ ":" + lig + " za<" +zone)
    rc("~display #"+index+ ":SWT,BWT,SWP")
    rc("~display #"+index +":"+hlig)
    togglelabells(label,index,lig,zone,hlig)
def clear(out):
    rc("defattr " + out+ "/clear.txt raiseTool false")
def changestate(index,out,lig,zone,min,max,hlig,label):    
    rc("~modeldisplay")
    rc("color white,s,r")    
    rc("defattr " + out+ "/temp.txt raiseTool false")
    rc("modeldisplay #"+index)
    rc("~display #"+index)
    rc("display #"+index +":"+lig)
    rc("rangecolor sireEnergy " + min + " blue 0 white " + max + " red")
    rc("color byatom #"+index+":" +lig)
    rc("colorkey 0.05,0.15 0.15,0.2 " + min + " blue 0 white " + max + " red")
    rc("display #"+index+ ":" + lig + " za<" +zone)
    rc("~display #"+index+ ":SWT,BWT,SWP")
    rc("~display #"+index +":"+hlig)
    togglelabells(label,index,lig,zone,hlig)
def lsupdateview(lig,zone,min,max,prev,index,hlig,label):
    rc("~modeldisplay")
    rc("modeldisplay #"+index)
    rc("~display")
    rc("~rlabel #"+index+ ":" + lig + " za<" + prev)
    rc("display #"+index+ ":"+lig)
    rc("rangecolor sireEnergy " + min + " blue 0 white " + max + " red")
    rc("color byatom #"+index+ ":" +lig)
    rc("colorkey 0.05,0.15 0.15,0.2 " + min + " blue 0 white " + max + " red")
    rc("display #"+index+ ":" + lig + " za<" +zone)
    rc("~display #"+index+ ":SWT,BWT,SWP")
    rc("~display #"+index +":"+hlig)
    togglelabells(label,index,lig,zone,hlig)

def lslistdisplay(lig,zone,prev,cur,index,hlig,label):
    rc("represent stick #"+index+ ":" + str(prev))
    rc("~display #"+index+ ":" + str(prev))
    rc("~rlabel #"+index+ ":" + str(prev))
    rc("display #"+index+ ":" + lig + " za<" +zone)
    rc("~display #"+index+ ":SWT,BWT,SWP")
    rc("~display #"+index +":"+hlig)
    togglelabells(label,index,lig,zone,hlig)
    rc("display #"+index+ ":" + str(cur))
    rc("represent bs #"+index+ ":" + str(cur))
    rc("rlabel #"+index+ ":" + str(cur))
def mmvisualizer(index,out,lig,zone,min,max,label):
    rc("~longbond")    
    rc("color white,s,r")    
    rc("defattr " + out+ "/temp.txt raiseTool false")
    rc("modeldisplay #"+index)
    rc("~display #"+index)
    rc("display #"+index +":"+lig)
    rc("rangecolor sireEnergy " + min + " blue 0 white " + max + " red")
    rc("color byatom #"+index+":" +lig)
    rc("colorkey 0.05,0.15 0.15,0.2 " + min + " blue 0 white " + max + " red")
    rc("display #"+index+ ":" + lig + " za<" +zone)
    togglelabelws(label,index,lig,zone)
def mmupdateview(lig,zone,min,max,prev,index,label):
    rc("~modeldisplay")
    rc("modeldisplay #"+index)
    rc("~display")
    rc("~rlabel #"+index+ ":" + lig + " za<" + prev)
    rc("display #"+index+ ":"+lig)
    rc("rangecolor sireEnergy " + min + " blue 0 white " + max + " red")
    rc("color byatom #"+index+ ":" +lig)
    rc("colorkey 0.05,0.15 0.15,0.2 " + min + " blue 0 white " + max + " red")
    rc("display #"+index+ ":" + lig + " za<" +zone)
    togglelabelws(label,index,lig,zone)
def mmlistdisplay(lig,zone,prev,cur,index,label):
    rc("represent stick #"+index+ ":" + str(prev))
    rc("~display #"+index+ ":" + str(prev))
    rc("~rlabel #"+index+ ":" + str(prev))
    rc("display #"+index+ ":" + lig + " za<" +zone)
    togglelabelws(label,index,lig,zone)
    rc("display #"+index+ ":" + str(cur))
    rc("represent bs #"+index+ ":" + str(cur))
    rc("rlabel #"+index+ ":" + str(cur))
