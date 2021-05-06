import PySide2.QtCore as QtCore, PySide2.QtWidgets as QtWidgets


class BaseImageViewer(QtWidgets.QGraphicsView):
	def __init__(self, parent = None):
		scene = QtWidgets.QGraphicsScene(parent)
		super(BaseImageViewer, self).__init__(scene, parent)
		# create a pixmap item to show the pixmap
		self.pixmapItem = QtWidgets.QGraphicsPixmapItem()

		self.scene().addItem(self.pixmapItem)
		self.setStyleSheet('background-color:#303030')


	def setPixmap(self, pixmap):
		self.pixmapItem.setPixmap(pixmap)


	def getPixmap(self):
		return self.pixmapItem.pixmap()


class ImageViewer(BaseImageViewer):
	def __init__(self, parent = None):
		super(ImageViewer, self).__init__(parent)

		self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse),
		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)


	def wheelEvent(self, event):
		numDegrees = event.delta() / 8
		numSteps = numDegrees / 15.0
		self.zoom(numSteps)
		event.accept()


	def zoom(self, step):
		zoomStep = 0.1
		scaleFactor = 1 + zoomStep * step
		zoom = self.transform().m11() * scaleFactor
		zoom = min(max(0.05, zoom), 3)
		self.scale(zoom / self.transform().m11(), zoom / self.transform().m11())
