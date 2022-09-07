import tkinter
from PIL import ImageTk
class TransparentWindow(tkinter.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title('uncle1bo')        #窗口标题
        self.resizable(True, True)    #固定窗口大小
        self.windowWidth = 200               #获得当前窗口宽
        self.windowHeight = 430              #获得当前窗口高
        screenWidth,screenHeight = self.maxsize()     #获得屏幕宽和高
        geometryParam = '%dx%d+%d+%d'%(self.windowWidth, self.windowHeight, (screenWidth-self.windowWidth)/2, (screenHeight - self.windowHeight)/2)
        self.geometry(geometryParam)    #设置窗口大小及偏移坐标
        self.wm_attributes('-topmost',1)#窗口置顶
        self.wm_attributes('-toolwindow',1)

        TRANSCOLOUR = '#3a3530'
        self.wm_attributes("-transparentcolor", TRANSCOLOUR)  #设置'gray'为透明色
        self.attributes("-alpha", 0.9)
        self.label_img = tkinter.Label(self,bg=TRANSCOLOUR)
        self.label_img.pack(fill=tkinter.BOTH, expand=True)
        self.label_img.bind("<Button-1>",self._onClick)
        self.label_img.bind("<Button-3>",lambda e: self.destroy())
        self._X=0
        self._Y=0
        self.bind('<Configure>', self._on_resize)
        self.bind("<B1-Motion>", self._move)  

        self.bind('<KeyPress-z>',self._onKeyPress)
        self.bind('<KeyPress-x>',self._onKeyPress)
        self.bind('<KeyPress-c>',self._onKeyPress)
        self.bind('<KeyPress-v>',self._onKeyPress)
        self.onClick=None
        self._hasCloseButton=False
        self.overrideredirect(self._hasCloseButton)     #窗口无边框

    def updateImage(self,image):
        img_gif = ImageTk.PhotoImage(image = image)
        self.label_img.config(image=img_gif)
        self.label_img.image = img_gif
       

    def _on_resize(self,evt):
        self.windowWidth=evt.width
        self.windowHeight=evt.height

    def _onClick(self,e):
        self._X,self._Y=e.x,e.y
        print('111')
        if self.onClick!=None:
            print('110')
            self.onClick(e)
    def _move(self,event):
        new_x = (event.x - self._X) + self.winfo_x()
        new_y = (event.y - self._Y) + self.winfo_y()
        s = f"{self.windowWidth}x{self.windowHeight}+{new_x}+{new_y}"
        self.geometry(s)
        
    def _onKeyPress(self,e):
        e.y=52
        if e.char=='z':
            e.x=10
            self._onClick(e)
        elif e.char=='x':
            e.x=self.windowWidth/2+10
            self._onClick(e)
        elif e.char=='c':
            self.destroy()
        elif e.char=='v':
            self._hasCloseButton=not self._hasCloseButton
            self.overrideredirect(self._hasCloseButton) 