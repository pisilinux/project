import os
filelist=os.listdir(".")
print filelist
imglist=[]


for obj in filelist:
    if obj.endswith(".png"):
        imglist.append(obj)
print imglist
for img in imglist:
    cmd="convert -strip %s %s" % (img, img)
    os.popen2(cmd)