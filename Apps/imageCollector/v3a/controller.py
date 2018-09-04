from PyQt4 import QtCore
from PyQt4 import QtGui
import webbrowser
import pyqtgraph as pg
import colorcet  # for nice colour maps
from epics import caget, caput
import numpy as np
import os
import sys
from datetime import datetime
from collections import OrderedDict
sys.path.append(r'\\apclara1.dl.ac.uk\ControlRoomApps\Controllers\bin\Release')
os.environ['PATH'] = os.environ['PATH'] + r';\\apclara1.dl.ac.uk\ControlRoomApps\Controllers\bin\stage\root_v5.34.34\bin'
import VELA_CLARA_Camera_Control
import VELA_CLARA_Screen_Control
cam_init = VELA_CLARA_Camera_Control.init()
scr_init = VELA_CLARA_Screen_Control.init()

os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1280
IMAGE_DIMS = (IMAGE_WIDTH, IMAGE_HEIGHT)

image_credits = {
    'pause.png': 'https://www.flaticon.com/free-icon/pause-symbol_25696#term=pause&page=1&position=5',
    'play.png': 'https://www.flaticon.com/free-icon/play-button_25226#term=play&page=1&position=1',
    'eye.png': 'https://www.flaticon.com/free-icon/eye_159604#term=eye&page=1&position=5',
    'in.png': 'https://www.flaticon.com/free-icon/vision_94922#term=vision&page=1&position=2',
    'out.png': 'https://www.flaticon.com/free-icon/vision-off_94930#term=eye%20cross&page=1&position=4',
}

# hardcode this here since it isn't exposed by the controller interface yet
# Taken from the config file camera.config
pix2mm = {'S01-CAM-01': 0.0134, 'S02-CAM-01': 0.0207, 'S02-CAM-02': 0.0122, 'S02-CAM-03': 0.0181, 'C2V-CAM-01': 0.0179}


def pixmap(icon_name):
    icon_filename = os.getcwd() + r'\resources\imageCollector\{}.png'.format(icon_name)
    return QtGui.QPixmap(icon_filename)


class Controller():
    def __init__(self, view):
        """Set up GUI and connect to the controllers."""
        self.cam_ctrl = cam_init.physical_Camera_Controller()  # replaces DAQ and IA controllers
        self.scr_ctrl = scr_init.physical_C2B_Screen_Controller()

        ini_filename = os.getcwd() + r'\resources\imageCollector\imageCollector.ini'
        self.settings = QtCore.QSettings(ini_filename, QtCore.QSettings.IniFormat)

        monitor = view.monitor  #pg.GraphicsView()
        layout = pg.GraphicsLayout(border=(100, 100, 100))
        monitor.setCentralItem(layout)
        self.view = view
        # self.model = model
        self.runFeedback = False
        self.counter = 0
        # self.histogram = pg.PlotWidget()
        # view.gridLayout.addWidget(self.histogram, 21, 0, 1, 1)

        view.screen_in_button.clicked.connect(self.moveScreenIn)
        view.screen_out_button.clicked.connect(self.moveScreenOut)
        view.leds_checkbox.stateChanged.connect(self.setLEDs)

        colour_map_names = [name for name in dir(colorcet) if ('_' not in name and name.lower() == name)]
        for i, name in enumerate(colour_map_names):
            icon = QtGui.QPixmap(32, 32)
            colour_map = getattr(colorcet, name)
            if isinstance(colour_map, list):
                icon.fill(QtGui.QColor(colour_map[0]))
                painter = QtGui.QPainter(icon)
                for j in range(32):
                    painter.setPen(QtGui.QColor(colour_map[j * 256 / 32]))
                    painter.drawLine(j, 0, j, 31)
                painter.end()
                view.colour_map_dropdown.addItem(QtGui.QIcon(icon), name)

        view.auto_level_checkbox.stateChanged.connect(self.autoLevelClicked)
        view.max_level_slider.valueChanged.connect(lambda val: view.max_level_spin.setValue(2 ** val - 1))
        view.max_level_spin.valueChanged.connect(self.maxLevelChanged)
        # view.acquire_pushButton.clicked.connect(self.model.acquire)
        self.camera_name = None
        view.save_pushButton.clicked.connect(self.collectAndSave)
        view.live_stream_label.linkActivated.connect(lambda: webbrowser.open(self.model.selectedCameraDAQ[0].streamingIPAddress))
        # view.setMask_pushButton.clicked.connect(self.setMask)
        view.image_folder_label.linkActivated.connect(self.openImageDir)
        # view.analyse_pushButton.clicked.connect(self.model.analyse)
        view.resetBackground_pushButton.clicked.connect(self.cam_ctrl.setBackground)
        camera_names = self.cam_ctrl.getCameraNames()
        screen_names = self.cam_ctrl.getCameraScreenNames()
        self.cam_dict = dict((screen, camera) for screen, camera in zip(screen_names, camera_names))
        item_names = ['S01-SCR-01', 'S02-SCR-01', 'S02-SCR-02', 'S02-SCR-03', 'C2V-SCR-01', 'INJ-YAG-04', 'INJ-YAG-05',
                      'INJ-YAG-06', 'INJ-YAG-07', 'INJ-YAG-08', 'BA1-YAG-01', 'BA1-YAG-02']  # , 'BA2-YAG-01']
        self.screens = QtGui.QStandardItemModel()
        view.cameras_treeview.setModel(self.screens)
        view.cameras_treeview.clicked.connect(self.changeCamera)
        for section in OrderedDict((name[:3], None) for name in item_names):
            parent = QtGui.QStandardItem(section)
            parent.setFlags(QtCore.Qt.NoItemFlags)
            for item in item_names:
                if item.startswith(section):
                    child = QtGui.QStandardItem(item[4:])
                    child.setData(item)
                    parent.appendRow(child)
            self.screens.appendRow(parent)
        view.cameras_treeview.expandAll()
        view.useBackground_checkBox.stateChanged.connect(self.cam_ctrl.useBackground)
        view.useNPoint_checkBox.stateChanged.connect(self.cam_ctrl.useNPoint)
        view.feedback_checkbox.stateChanged.connect(self.toggleFeedBack)
        view.stepSize_spinBox.valueChanged.connect(self.cam_ctrl.setStepSize)
        view.reset_averages_button.clicked.connect(self.resetAverages)

        # Update GUI
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        #self.ImageBox = layout.addViewBox(lockAspect=True, colspan=2)
        # data = np.random.normal(size=(IMAGE_HEIGHT, IMAGE_WIDTH))
        x, y = np.meshgrid(np.arange(IMAGE_HEIGHT), np.arange(IMAGE_WIDTH))
        d = np.sqrt((x - IMAGE_HEIGHT / 2) ** 2 + (y - IMAGE_WIDTH / 2) ** 2)
        h = 2**16 - 1
        sigma = 100
        data = h * np.exp(-(d**2) / (2 * sigma**2))
        self.Image = pg.ImageItem(data)
        # self.Image.setRect(QtCore.QRect(0, 0, 100, 100))
        # self.Image.scale(0.0134, 0.0134)
        self.ImageBox = layout.addPlot()

        # self.ImageBox.setRange(xRange=[0, IMAGE_HEIGHT * 2], yRange=[0, IMAGE_WIDTH * 2])
        self.ImageBox.addItem(self.Image)
        self.roi = pg.EllipseROI([0, 0], [500, 500])#, movable=False)
        self.roi.addTranslateHandle([0.5, 0.5])  # centre of ellipse
        self.ImageBox.addItem(self.roi)
        self.roi.removeHandle(0)  # remove rotation handle
        self.roi.sigRegionChangeFinished.connect(self.roiChanged)
        # self.changing_roi = False  # flag to prevent looping between changing ROI and spinboxes
        self.ImageBox.setAspectLocked(True)
        self.vLineMLE = self.ImageBox.plot(x=[1000, 1000], y=[900, 1100], pen='g')
        self.hLineMLE = self.ImageBox.plot(x=[900, 1100], y=[1000, 1000], pen='g')
        self.vLineMLE_avg = self.ImageBox.plot(x=[1000, 1000], y=[900, 1100], pen='c')
        self.hLineMLE_avg = self.ImageBox.plot(x=[900, 1100], y=[1000, 1000], pen='c')

        # show screen name, beam position and size as an overlay on the image
        self.title_label = pg.LabelItem('', color='#ffffff')
        self.title_label.setPos(50, 20)
        # use a drop shadow so we can always see it
        shadow = QtGui.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setColor(QtGui.QColor('#000000'))
        shadow.setOffset(1, 1)
        self.title_label.setGraphicsEffect(shadow)
        monitor.addItem(self.title_label)

        map_name = str(self.settings.value('colourMap', 'fire').toString())
        view.colour_map_dropdown.currentIndexChanged[QtCore.QString].connect(self.changeColourMap)
        index = view.colour_map_dropdown.findText(map_name, QtCore.Qt.MatchExactly)
        if index == -1:
            index = view.colour_map_dropdown.findText('fire', QtCore.Qt.MatchExactly)
        view.colour_map_dropdown.setCurrentIndex(index)
        self.changeColourMap(map_name)
        view.statusbar.showMessage('Ready.')

    def moveScreenIn(self):
        """The In button was clicked. Move the current screen in."""
        self.moveScreen(move_in=True)

    def moveScreenOut(self):
        """The Out button was clicked. Move the current screen out."""
        self.moveScreen(move_in=False)

    def moveScreen(self, move_in):
        """Move the current screen in or out."""
        camera_name = self.getCurrentScreen()
        screen_name = self.cam_ctrl.getCameraObj(camera_name).screenName.replace('YAG', 'SCR')
        if move_in:
            self.view.statusbar.showMessage('Moving screen {} IN'.format(screen_name))
            self.scr_ctrl.insertYAG(screen_name)
        else:
            self.view.statusbar.showMessage('Moving screen {} OUT'.format(screen_name))
            pneumatic = self.scr_ctrl.isPneumatic(screen_name)
            state = VELA_CLARA_Screen_Control.SCREEN_STATE.RETRACTED if pneumatic else VELA_CLARA_Screen_Control.SCREEN_STATE.V_RF
            self.scr_ctrl.moveScreenTo(screen_name, state)

    def setLEDs(self, is_on):
        """The LEDs checkbox has been clicked - turn them on or off."""
        # TODO: Duncan to add this to controller 28/8
        status = 'On' if is_on else 'Off'
        self.view.statusbar.showMessage('Switching LEDs {}'.format(status.upper()))
        pv_name = 'CLA-LAS-DIA-LED-01:' + (status)
        # simulate pressing button!
        caput(pv_name, 1)
        caput(pv_name, 0)

    def changeColourMap(self, map_name):
        """A colour map has been selected from the dropdown box. Set the image colour map."""
        colour_list_hex = getattr(colorcet, str(map_name))
        colour_list = np.array([pg.colorTuple(pg.mkColor(code)) for code in colour_list_hex])
        colour_map = pg.ColorMap(np.linspace(0, 1, len(colour_list_hex)), colour_list)
        self.Image.setLookupTable(colour_map.getLookupTable())
        self.settings.setValue('colourMap', map_name)

    def maxLevelChanged(self, value):
        """The maximum level spinbox has been changed. Update the slider to an approximate position."""
        self.view.max_level_slider.blockSignals(True)  # otherwise we get a feedback loop!
        self.view.max_level_slider.setValue(int(np.round(np.log2(value + 1))))
        self.view.max_level_slider.blockSignals(False)
        if not self.view.auto_level_checkbox.isChecked():
            self.settings.setValue(self.camera_name + '/maxLevel', value)

    def autoLevelClicked(self, checked):
        """The "auto level" checkbox was clicked."""
        self.view.max_level_slider.setEnabled(not checked)
        self.view.max_level_spin.setEnabled(not checked)
        self.settings.setValue(self.camera_name + '/autoLevel', checked)

    def changeCamera(self):
        """The current item in the list box was changed. Set the correct camera."""
        screen_name = self.getCurrentScreen()
        # convert to camera name
        camera_name = self.cam_dict[screen_name]
        self.camera_name = camera_name
        camera = self.cam_ctrl.getCameraObj(camera_name)
        self.view.statusbar.showMessage('Switching to screen {} (camera {})'.format(screen_name, camera_name))

        self.cam_ctrl.startAcquiring(camera_name)  # this will automatically stop all the other ones
        self.cam_ctrl.startAnalysing(camera_name)

        auto_level = self.settings.value(camera_name + '/autoLevel', False).toBool()
        self.view.auto_level_checkbox.setChecked(auto_level)
        if not auto_level:
            level, ok = self.settings.value(camera_name + '/maxLevel', 1023).toInt()
            self.view.max_level_spin.setValue(level)
        self.view.numImages_spinBox.setMaximum(camera.daq.maxShots)
        self.view.useBackground_checkBox.setChecked(camera.state.use_background)
        self.view.useNPoint_checkBox.setChecked(camera.state.use_npoint)

        self.updateROIFromMask()

    def getCurrentScreen(self):
        index = self.view.cameras_treeview.currentIndex()
        screen = self.screens.itemFromIndex(index)
        screen_name = str(screen.data().toString())
        return screen_name

    def updateROIFromMask(self):
        """The mask has changed - update the ROI."""
        mask =  self.cam_ctrl.getMaskObj()
        print('got mask obj', mask.mask_x, mask.mask_y, mask.mask_x_rad, mask.mask_y_rad)
        x = mask.mask_x - mask.mask_x_rad
        y = mask.mask_y - mask.mask_y_rad
        self.roi.blockSignals(True)  # don't update the mask recursively!
        self.roi.setPos(QtCore.QPoint(x, y))
        if mask.mask_x_rad > 0 and mask.mask_y_rad > 0:
            self.roi.setSize(QtCore.QPoint(mask.mask_x_rad * 2, mask.mask_y_rad * 2))
        self.roi.blockSignals(False)

    def roiChanged(self):
        """The ROI ellipse has been altered by dragging the handles. Update the mask accordingly."""
        pos, size = self.roi.pos(), self.roi.size()
        x, y = pos.x(), pos.y()
        w, h = size.x(), size.y()
        centre_x, centre_y = int(round(x + w / 2)), int(round(y + h / 2))
        x_rad, y_rad = int(round(w / 2)), int(round(h / 2))
        self.view.statusbar.showMessage('Setting mask: centre ({}, {}), radius ({}, {})'.format(centre_x, centre_y, x_rad, y_rad))
        print('Setting mask: centre ({}, {}), radius ({}, {})'.format(centre_x, centre_y, x_rad, y_rad))
        self.cam_ctrl.setMask(centre_x, centre_y, x_rad, y_rad)

    def openImageDir(self):
        """Open an Explorer window at the location of the saved images."""
        folder = datetime.today().strftime(r'\\claraserv3\CameraImages\%Y\%#m\%#d')  # omit leading zeros from month and day
        # go up in the folder structure until we hit a folder that exists!
        while not os.path.exists(folder):
            folder, file = os.path.split(folder)
        os.system('explorer.exe /select,"{}"'.format(folder))

    def toggleFeedBack(self, use):
        self.runFeedback = use

    def update(self):
        current_camera_name = None
        cam_ctrl = self.cam_ctrl
        camera_list = self.screens
        for i in range(camera_list.rowCount()):
            section = camera_list.item(i)
            for j in range(section.rowCount()):
                item = section.child(j)
                name = str(item.data().toString())

                is_acquiring = cam_ctrl.isAcquiring(name)
                screen_name = self.cam_ctrl.getCameraObj(name).screenName.replace('YAG', 'SCR')
                screen_state = self.scr_ctrl.getScreenState(screen_name)
                # screen_in = screen_state in (VELA_CLARA_Screen_Control.SCREEN_STATE.V_YAG, VELA_CLARA_Screen_Control.SCREEN_STATE.YAG)
                screen_in = self.scr_ctrl.isScreenIn(screen_name)
                # TODO: maybe more icons for other objects (collimator, slit, graticule etc)
                item.setIcon(QtGui.QIcon(pixmap('in' if screen_in else 'out')))  # TODO: correct?

                if is_acquiring:
                    index = self.screens.indexFromItem(item)
                    self.view.cameras_treeview.setCurrentIndex(index)
                    current_camera_name = name
                    if self.scr_ctrl.isScreenMoving(screen_name):
                        self.view.screen_progress.setFormat('%p%')
                        pneumatic = self.scr_ctrl.isPneumatic(screen_name)
                        state = VELA_CLARA_Screen_Control.SCREEN_STATE
                        states = (state.V_RF, state.V_YAG) if pneumatic else (state.RETRACTED, state.YAG)
                        out_pos, in_pos = (self.scr_ctrl.getDevicePosition(screen_name, state) for state in states)
                        sign = np.copysign(1, in_pos - out_pos)  # in case out > in. We want 100% to be 'in', so out should be less
                        self.view.screen_progress.setRange(sign * out_pos, sign * in_pos)
                        self.view.screen_progress.setValue(sign * self.scr_ctrl.getACTPOS(screen_name))
                    else:
                        self.view.screen_progress.setFormat(str(screen_state))
                        self.view.screen_progress.setValue(self.view.screen_progress.maximum() if screen_in else 0)

        if current_camera_name is None:
            self.view.cameras_treeview.selectionModel().clearSelection()
            return

        # Set crosshairs
        analysis = cam_ctrl.getAnalysisObj(current_camera_name)
        x, y = analysis.x_pix_mean, analysis.y_pix  # TODO: no 'y_pix_mean' !!
        sigX, sigY = analysis.sig_x_pix_mean, analysis.sig_y_pix_mean
        self.vLineMLE_avg.setData(x=[x, x], y=[y - sigY, y + sigY])
        self.hLineMLE_avg.setData(x=[x - sigX, x + sigX], y=[y, y])
        x, y = analysis.x_pix, analysis.y_pix
        sigX, sigY = analysis.sig_x_pix, analysis.sig_y_pix
        self.vLineMLE.setData(x=[x, x], y=[y - sigY, y + sigY])
        self.hLineMLE.setData(x=[x - sigX, x + sigX], y=[y, y])
        #labels
        label_text = '''<h1>{}</h1>
                        <h2 style="color: green;">Immediate</h2>
                        <p style="color: green;"><b>Position</b>: {:.3f}, {:.3f} mm<br><b>Size (1 &sigma;)</b>: {:.3f}, {:.3f} mm<br>
                        <b>Covariance XY</b>: {:.3f} mm<sup>2</sup><br><b>Average intensity</b>: {:.3f}</p>
                        <h2 style="color: cyan;">Average ({})</h2>
                        <p style="color: cyan;"><b>Position</b>: {:.3f}, {:.3f} mm<br><b>Size (1 &sigma;)</b>: {:.3f}, {:.3f} mm<br>
                        <b>Covariance XY</b>: {:.3f} mm<sup>2</sup><br><b>Average intensity</b>: {:.3f}</p>'''
        self.title_label.setText(label_text.format(current_camera_name,
                                                   analysis.x, analysis.y, analysis.sig_x,
                                                   analysis.sig_y, analysis.sig_xy, analysis.avg_pix,
                                                   analysis.sig_x_n,
                                                   analysis.x_mean, analysis.y_mean, analysis.sig_x_mean,
                                                   analysis.sig_y_mean, analysis.sig_xy_mean, analysis.avg_pix_mean
                                                   ))
        data = cam_ctrl.takeAndGetFastImage()
        # data = cam_ctrl.getImageObj().data
        # data = caget(cam_ctrl.getCameraObj(current_camera_name).pvRoot + 'CAM2:ArrayData')
        leds_on = caget('CLA-LAS-DIA-LED-01:Sta') == 1  # TODO: check this really works
        if self.view.auto_level_checkbox.isChecked() and not leds_on:
            centile90 = np.percentile(data, 99.9)
            self.view.max_level_spin.setValue(int(centile90))

        if data is not None and len(data) == IMAGE_HEIGHT * IMAGE_WIDTH:
            npData = np.array(data).reshape((IMAGE_HEIGHT, IMAGE_WIDTH))
            self.Image.setImage(np.flip(np.transpose(npData), 1))
            max_level = self.view.max_level_spin.maximum() if leds_on else self.view.max_level_spin.value()
            self.Image.setLevels([0, max_level], update=True)
            # image_rect = QtCore.QRect(0, 0, IMAGE_WIDTH * pix2mm[current_camera_name],
            #                           IMAGE_HEIGHT * pix2mm[current_camera_name])
            # self.Image.setRect(image_rect)

        if cam_ctrl.isCollecting(current_camera_name):  # TODO: correct?
            text = 'Kill'
        elif cam_ctrl.isSaving(current_camera_name):
            text = 'Writing'
        else:
            text = 'Save'
        self.view.save_pushButton.setText(text)

        self.counter += 1
        if self.runFeedback and self.counter >= 1:
            self.counter = 0
            height = IMAGE_WIDTH * 2
            width = IMAGE_HEIGHT * 2
            if -999.999 in (x, y, sigX, sigY):
                return
            # DAW says that +/-4sigma should be OK for a window
            # See http://www.ophiropt.com/user_files/laser/beam_profilers/Techniques_Beam_Width_Cameras_pt3.pdf
            # if x-5*sX > 0 and x+5*sX < width and y-5*sY > 0 and y+5*sY < height:
            for n in (4, 3, 2):
                # n = 4
                print 'Setting mask', x, y, n * sigX, n * sigY
                if 0 < n * sigX < height / 2 and 0 < n * sigY < width / 2:
                    self.cam_ctrl.setMask(int(x), int(y), int(n * sigX), int(n * sigY))
                    self.updateROIFromMask()
                    break

    def collectAndSave(self):
        numberOfImages = self.view.numImages_spinBox.value()
        if self.cam_ctrl.isAcquiring():
            self.cam_ctrl.collectAndSave(numberOfImages)
            self.view.statusbar.showMessage('Saving {} images'.format(numberOfImages))
            # self.camerasDAQ.collectAndSaveJPG()
        elif self.cam_ctrl.isCollectingOrSaving():
            self.camerasDAQ.killCollectAndSave()  # TODO: this isn't right any more
        # self.camerasDAQ.killCollectAndSaveJPG()

    def resetAverages(self):
        """The 'reset averages' button was clicked."""
        analysis = self.cam_ctrl.getAnalysisObj()
        [getattr(analysis, name) for name in dir(analysis) if 'clear' in name]