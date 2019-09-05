import sys
from PySide import QtGui
from PySide import QtCore


class MyImage(QtGui.QWidget):

    def __init__(self, image_path="", initial_size=(400, 600)):
        QtGui.QWidget.__init__(self)
        self.image_lab = QtGui.QLabel(self)
        self.image_lab.mouseMoveEvent = self.move_image
        self.image_lab.mousePressEvent = self.mousePress
        self.image_lab.wheelEvent = self.Zoom
        self.image_path = image_path
        self.pixmap = QtGui.QPixmap(self.image_path)
        self.pixmapresized = self.pixmap
        self.image_lab.setPixmap(self.pixmapresized)
        self.initial_size = initial_size
        self.scaleFactor = 1

    def move_image(self, event):
        if event.buttons() & QtCore.Qt.MouseButton.MiddleButton:
            x = self.image_lab.x() + event.x() - self.start_mouse[0]
            y = self.image_lab.y() + event.y() - self.start_mouse[1]
            self.image_lab.setGeometry(x, y, self.image_lab.width(), self.image_lab.height())

    def mousePress(self, event):
        if event.button() == QtCore.Qt.MouseButton.MiddleButton:
            self.start_mouse = event.x(), event.y()
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            return

    def Zoom(self, event):
        if (event.delta() > 0):
            self.zoomIn()
        if (event.delta() < 0):
            self.zoomOut()

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.pixmapresized = self.pixmap.scaled(self.scaleFactor * self.pixmap.size())

        self.image_lab.setPixmap(self.pixmapresized)


class ImageViewer(QtGui.QWidget):

    def __init__(self, app=QtGui.QApplication):
        QtGui.QWidget.__init__(self)
        self.app = app
        self.main_lay = QtGui.QHBoxLayout()
        self.setLayout(self.main_lay)
        self.scaleFactor = 0.0;
        self.setWindowTitle("Picaso")
        self.resize(500, 300)
        self.no_scale = False
        self.start_mouse = 0, 0
        self.createActions()
        self.mousePressEvent = self.mousePress

    def open(self):
        fileName, _ = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                                                        QtCore.QDir.currentPath())
        if fileName:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                                              "Cannot load %s." % fileName)
            return fileName

    def mousePress(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.context_menu(event,)

    def context_menu(self, event):
        menu = QtGui.QMenu(self)
        menu.addAction(self.addImageAct)
        menu.addAction(self.closeAct)

        menu.exec_(event.globalPos())

    def addimage(self):
        image_path = self.open()
        myimage = MyImage(image_path=image_path)
        self.main_lay.addWidget(myimage)

    def close(self):
        self.app.exit()

    def createActions(self):

        self.addImageAct = QtGui.QAction("&addImage...", self, triggered=self.addimage)
        self.closeAct = QtGui.QAction("&Close", self,
                                      statusTip="Closing", triggered=self.close)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    iv = ImageViewer(app=app)
    iv.show()
    app.exec_()
    sys.exit()
