
import tkinter
import numpy as np
import time
import win32gui, win32ui, win32con,win32api
from PIL import Image, ImageTk

hwnd_title = dict()
def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})

win32gui.EnumWindows(get_all_hwnd, 0)



hWnd = 0
for k,v in hwnd_title.items():
    if 'Phone-STS' in v:
        hWnd=k
#获取句柄窗口的大小信息
left, top, right, bot = win32gui.GetWindowRect(hWnd)
width = int((right - left)*1.4)
height = int((bot - top)*1.4)
#返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
hWndDC = win32gui.GetWindowDC(hWnd)
#创建设备描述表
mfcDC = win32ui.CreateDCFromHandle(hWndDC)
#创建内存设备描述表
saveDC = mfcDC.CreateCompatibleDC()


def getWinImg():

    #创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    #为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
    #将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    #保存bitmap到内存设备描述表
    saveDC.BitBlt((0,0), (width,height), mfcDC, (10, 50), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    ###生成图像
    im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
    return im_PIL









 
root = tkinter.Tk()
root.title('uncle1bo')        #窗口标题
root.resizable(True, True)    #固定窗口大小
windowWidth = 200               #获得当前窗口宽
windowHeight = 430              #获得当前窗口高
screenWidth,screenHeight = root.maxsize()     #获得屏幕宽和高
geometryParam = '%dx%d+%d+%d'%(windowWidth, windowHeight, (screenWidth-windowWidth)/2, (screenHeight - windowHeight)/2)
root.geometry(geometryParam)    #设置窗口大小及偏移坐标
root.wm_attributes('-topmost',1)#窗口置顶
root.overrideredirect(True)     #窗口无边框

TRANSCOLOUR = '#3a3530'
root.wm_attributes("-transparentcolor", TRANSCOLOUR)  #设置'gray'为透明色
root.attributes("-alpha", 0.8)
#label图片
img=getWinImg().resize((windowWidth,windowHeight))
img_gif = ImageTk.PhotoImage(image = img)



label_img = tkinter.Label(root,image=img_gif,bg=TRANSCOLOUR)
label_img.pack(fill=tkinter.BOTH, expand=True)

def getImg():
    
    img=getWinImg().resize((windowWidth,windowHeight))
    img_array=img.load()
    
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if img_array[x, y][0] < 100 and img_array[x, y][1] <100 and img_array[x, y][2] <100:
                img_array[x, y] = (58, 53, 48)

    img_gif = ImageTk.PhotoImage(image = img)
    label_img.config(image=img_gif)
    label_img.image = img_gif
    
bx,by=0,0

def onClick(e):
    global bx,by
    bx,by=e.x,e.y
    x=10
    print(e,windowWidth)
    if e.y>50:
        if e.x>windowWidth/2:
            x=200
        long_position = win32api.MAKELONG(x, 10)#模拟鼠标指针 传送到指定坐标
        win32api.SendMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下
        win32api.SendMessage(hWnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起
        time.sleep(0.5)
        getImg()
label_img.bind("<Button-1>",onClick)
label_img.bind("<Button-3>",lambda e: root.destroy())

def on_resize(evt):
    global windowWidth,windowHeight
    windowWidth=evt.width
    windowHeight=evt.height
root.bind('<Configure>', on_resize)


def move(event):
    new_x = (event.x - bx) + root.winfo_x()
    new_y = (event.y - by) + root.winfo_y()
    s = f"{windowWidth}x{windowHeight}+{new_x}+{new_y}"
    root.geometry(s)
root.bind("<B1-Motion>", move)  
def onKeyPress(e):
    e.y=52
    if e.char=='z':
        e.x=10
        onClick(e)
    elif e.char=='x':
        e.x=windowWidth/2+10
        onClick(e)
    elif e.char=='c':
        root.destroy()




root.bind('<KeyPress-z>',onKeyPress)
root.bind('<KeyPress-x>',onKeyPress)
root.bind('<KeyPress-c>',onKeyPress)
getImg()
root.mainloop()


