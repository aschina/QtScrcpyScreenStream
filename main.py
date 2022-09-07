
from transparentWindow import TransparentWindow
import time
import win32gui
import win32ui
import win32con
import win32api
from PIL import Image

hwnd_title = dict()


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)


hWnd = 0
for k, v in hwnd_title.items():
    if 'Phone-STS' in v:
        hWnd = k
# 获取句柄窗口的大小信息
left, top, right, bot = win32gui.GetWindowRect(hWnd)
width = int((right - left)*1.4)
height = int((bot - top)*1.4)-10
# 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
hWndDC = win32gui.GetWindowDC(hWnd)
# 创建设备描述表
mfcDC = win32ui.CreateDCFromHandle(hWndDC)
# 创建内存设备描述表
saveDC = mfcDC.CreateCompatibleDC()


def getWinImg():

    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (15, 50), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    # 生成图像
    im_PIL = Image.frombuffer(
        'RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    return im_PIL


root = TransparentWindow()

# label图片
img = getWinImg().resize((root.windowWidth, root.windowHeight))
root.updateImage(img)


def getImg():

    img = getWinImg().resize((root.windowWidth, root.windowHeight))
    img = img.convert('RGBA')
    img_array = img.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if img_array[x, y][0] < 100 and img_array[x, y][1] < 100 and img_array[x, y][2] < 100:
                img_array[x, y] = (255, 255, 255, 0)
    root.updateImage(img)


def onClick(e):
    x = 10
    print(e, root.windowWidth)
    if e.y > 50:
        if e.x > root.windowWidth/2:
            x = 200
        long_position = win32api.MAKELONG(x, 10)  # 模拟鼠标指针 传送到指定坐标
        win32api.SendMessage(hWnd, win32con.WM_LBUTTONDOWN,
                             win32con.MK_LBUTTON, long_position)  # 模拟鼠标按下
        win32api.SendMessage(hWnd, win32con.WM_LBUTTONUP,
                             win32con.MK_LBUTTON, long_position)  # 模拟鼠标弹起
        time.sleep(0.5)
        getImg()


root.onClick = onClick


getImg()
root.mainloop()
