import time
import win32gui
import win32ui
import win32con
import win32api
import ctypes
from ctypes import wintypes


from PIL import Image


class TargetWindow():

    def __init__(self, name='YAL-') -> None:
        self.setName(name)
        assert self.hWnd != 0
        self.pycwnd = win32ui.CreateWindowFromHandle(self.hWnd)
        # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        self.hWndDC = win32gui.GetWindowDC(self.hWnd)
        # 创建设备描述表
        self.mfcDC = win32ui.CreateDCFromHandle(self.hWndDC)
        # 创建内存设备描述表
        self.saveDC = self.mfcDC.CreateCompatibleDC()

    def setName(self, name):
        hwnd_title = dict()

        def get_all_hwnd(hwnd, mouse):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
        win32gui.EnumWindows(get_all_hwnd, 0)
        self.hWnd = 0
        for k, v in hwnd_title.items():
            if name in v:
                self.hWnd = k
        self.name = name

    def get_window_rect(self):
        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            f = None
        if f:
            rect = wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(wintypes.HWND(self.hWnd),
              wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
              ctypes.byref(rect),
              ctypes.sizeof(rect)
              )
            return rect.left, rect.top, rect.right, rect.bottom

    def size(self):
        left, top, right, botton = self.get_window_rect()
        width = int((right - left))
        height = int((botton - top))
        return width, height

    def screenshot(self):
        width, height = self.size()

        # 创建位图对象准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        # 为bitmap开辟存储空间
        saveBitMap.CreateCompatibleBitmap(self.mfcDC, width, height)
        # 将截图保存到saveBitMap中
        self.saveDC.SelectObject(saveBitMap)
        # 保存bitmap到内存设备描述表
        self.saveDC.BitBlt((0, 0), (width, height),
                           self.mfcDC, (20, 50), win32con.SRCCOPY)
        # result = ctypes.windll.user32.PrintWindow(
        #     self.hWnd, self.saveDC.GetSafeHdc(), 1)
        # print(result)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        # 生成图像
        im_PIL = Image.frombuffer(
            'RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        return im_PIL

    def click(self,x,y):
        lParam = y << 16 | x

        self.pycwnd.SendMessage(win32con.WM_SETCURSOR,
                                win32con.WM_MOUSEMOVE, lParam)
        lParam = y << 16 | x
        self.pycwnd.SendMessage(win32con.WM_CAPTURECHANGED, None, None)
        self.pycwnd.SendMessage(win32con.WM_SETCURSOR,  win32api.MAKELONG(
            win32con.HTCLIENT, win32con.WM_MOUSEMOVE))
        self.pycwnd.SendMessage(win32con.WM_MOUSEACTIVATE,  win32api.MAKELONG(
            win32con.HTCLIENT, win32con.WM_LBUTTONDOWN))
        # target.pycwnd.PostMessage( win32con.WM_WINDOWPOSCHANGING, 0, pywintypes.Unicode( None, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE))
        self.pycwnd.SendMessage(win32con.WM_NCPAINT, 1, 0)
        # target.pycwnd.PostMessage( win32con.WM_WINDOWPOSCHANGED, 0, pywintypes.Unicode( None, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE))
        self.pycwnd.SendMessage(win32con.WM_ACTIVATEAPP, 1, 0)
        self.pycwnd.SendMessage(win32con.WM_NCACTIVATE, 1, 0)
        self.pycwnd.SendMessage(win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
        self.pycwnd.SendMessage(win32con.WM_SETFOCUS, 0, 0)
        self.pycwnd.SendMessage(win32con.WM_MOUSEMOVE,
                                0, lParam)
        self.pycwnd.SendMessage(win32con.WM_LBUTTONDOWN,
                                win32con.MK_LBUTTON, lParam)
        time.sleep(0.2)
        self.pycwnd.SendMessage(win32con.WM_LBUTTONUP, 0, lParam)
