
from transparentQtWindow import TransparentWindow, app, sys
from targetWindow import TargetWindow

root = TransparentWindow()
target = TargetWindow()


def getImg():

    img = target.screenshot().resize((root.windowWidth, root.windowHeight))
    img = img.convert('RGBA')
    img_array = img.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if img_array[x, y][0] < 80 and img_array[x, y][1] < 80 and img_array[x, y][2] < 80:
                img_array[x, y] = (255, 255, 255, 1)

            else:
                img_array[x, y] = (125, 125, 125, 125)

    root.updateImage(img)


def onClick(event):
    point = event.globalPos()-root.pos()
    target_w, target_h = target.size()
    w_rate = target_w/root.windowWidth
    h_rate = target_h/root.windowHeight
    # if point.y() > 100:
    x = int(point.x()*w_rate)
    y = int(point.y()*h_rate)
    # x=48
    # y=572
    print(x, y)
    target.click(x, y)


root.mouseReleaseEventList.append(onClick)
root.updateImageLoop(100, getImg)

root.show()
sys.exit(app.exec_())
