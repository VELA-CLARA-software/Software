from PyQt4 import QtGui, QtCore
import controller.control as controller
import view.view_v6 as view
import model.model as model
import data.data as data
import sys

# 
sys.path.append('../../../../Controllers/bin/Release')

class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

class App(QtCore.QObject):
	def __init__(self, sys_argv):
		super(App, self).__init__()
		self.view = view.Ui_MainWindow()
		self.MainWindow = QtGui.QMainWindow()
		self.data = data.data()
		self.view.setupUi(self.MainWindow)

		w = self.view
		#w.setupUi(self)
		#btn = w.pushButton
		#btn.clicked.connect(self.test)
		self.process = w.textEdit
		self.process.moveCursor(QtGui.QTextCursor.Start)
		self.process.ensureCursorVisible()
		self.process.setLineWrapColumnOrWidth(500)
		self.process.setLineWrapMode(QtGui.QTextEdit.FixedPixelWidth)
		#self.show()

		self.model = model.Model(self, self.view, self.data)
		self.controller = controller.Controller(self.view, self.model, self.data)
		self.MainWindow.show()
		#self.home()
		sys.stdout = Stream(newText=self.onUpdateText)

	def onUpdateText(self, text):
		cursor = self.process.textCursor()
		cursor.movePosition(QtGui.QTextCursor.End)
		cursor.insertText(text)
		self.process.setTextCursor(cursor)
		self.process.ensureCursorVisible()

	def __del__(self):
		sys.stdout = sys.__stdout__

	def test(self):
		try:
			nonexistent_function()
		except Exception as e:
			print e
			#print 'test'

	# def home(self):
	# 	w = self.view
	# 	#w.setupUi(self)
	# 	#btn = w.pushButton
	# 	#btn.clicked.connect(self.test)
	# 	self.process = w.textEdit
	# 	self.process.moveCursor(QtGui.QTextCursor.Start)
	# 	self.process.ensureCursorVisible()
	# 	self.process.setLineWrapColumnOrWidth(500)
	# 	self.process.setLineWrapMode(QtGui.QTextEdit.FixedPixelWidth)
	# 	self.show()


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	appObject = App(sys.argv)
	sys.exit(app.exec_())
