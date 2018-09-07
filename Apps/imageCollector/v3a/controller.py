from PyQt4 import QtCore
from PyQt4 import QtGui
import webbrowser
import pyqtgraph as pg
import colorcet  # for nice colour maps
# from epics import caget, caput
import numpy as np
import h5py
import os
import sys
import time
from datetime import datetime
from collections import OrderedDict, defaultdict
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
IMAGE_DIMS = (IMAGE_HEIGHT, IMAGE_WIDTH)
IMAGE_WIDTH_FULL = IMAGE_WIDTH * 2
IMAGE_HEIGHT_FULL = IMAGE_HEIGHT * 2
IMAGE_DIMS_FULL = (IMAGE_HEIGHT_FULL, IMAGE_WIDTH_FULL)
IMAGE_WIDTH_VELA = 1392
IMAGE_HEIGHT_VELA = 1040
IMAGE_DIMS_VELA = (IMAGE_HEIGHT_VELA, IMAGE_WIDTH_VELA)
image_path = [r'\\claraserv3', 'CameraImages']
hdf5_image_folder = '\\'.join(image_path)
# only show top-level dirs, and ones that consist entirely of digits (i.e. year/month/date)
filter_regexp = '|'.join([d.replace('\\', '\\\\') for d in image_path]) + '|^\d+$'

image_credits = {
    'pause.png': 'https://www.flaticon.com/free-icon/pause-symbol_25696#term=pause&page=1&position=5',
    'play.png': 'https://www.flaticon.com/free-icon/play-button_25226#term=play&page=1&position=1',
    'eye.png': 'https://www.flaticon.com/free-icon/eye_159604#term=eye&page=1&position=5',
    'in.png': 'https://www.flaticon.com/free-icon/vision_94922#term=vision&page=1&position=2',
    'out.png': 'https://www.flaticon.com/free-icon/vision-off_94930#term=eye%20cross&page=1&position=4',
}

class ImageDirFilter(QtGui.QSortFilterProxyModel):
    """This is a proxy model for a file system model that implements a 'natural sort' algorithm."""
    def __init__(self):
        super(ImageDirFilter, self).__init__()

    def lessThan(self, left_index, right_index):
        """Implement 'natural sort' for folders without leading zeroes."""
        model = self.sourceModel()
        left_str = str(model.data(left_index).toString())
        right_str = str(model.data(right_index).toString())
        try:
            return int(left_str) < int(right_str)
        except ValueError:  # conversion to int failed
            return left_str < right_str


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
        layout = pg.GraphicsLayout()
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
        view.cameras_treeview.viewport().setAutoFillBackground(False)
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

        view.overlay_checkbox.stateChanged.connect(self.displayOverlay)
        view.overlay_treeview.viewport().setAutoFillBackground(False)
        self.overlays = QtGui.QFileSystemModel()
        self.overlays.directoryLoaded.connect(self.folderLoaded)  # expands tree to day entries initially
        self.overlays.setRootPath(hdf5_image_folder)
        self.overlays.setReadOnly(True)
        self.overlays.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
        self.overlays.setNameFilterDisables(False)  # hide entries that don't pass the filter

        # use a proxy to do advanced filtering (numeric-only dir entries, and only HD5 files)
        self.overlays_proxy = ImageDirFilter()
        self.overlays_proxy.setSourceModel(self.overlays)
        view.overlay_treeview.setModel(self.overlays_proxy)
        self.view.overlay_treeview.selectionModel().selectionChanged.connect(self.overlaySelectionChanged)
        self.view.overlay_treeview.setMouseTracking(True)
        self.view.overlay_treeview.entered.connect(self.mouseMoveOverTree)
        self.tooltip_checker = QtCore.QTimer()
        self.tooltip_checker.timeout.connect(self.keepToolTipShown)

        view.overlay_treeview.setRootIndex(self.overlays_proxy.mapFromSource(self.overlays.index(hdf5_image_folder)))
        self.overlays_proxy.setFilterRegExp(QtCore.QRegExp(filter_regexp, QtCore.Qt.CaseInsensitive))
        self.overlays_proxy.sort(0, QtCore.Qt.DescendingOrder)
        [self.view.overlay_treeview.hideColumn(i) for i in range(1, self.overlays.columnCount())]  # only show names

        view.cameras_treeview.expandAll()
        view.useBackground_checkBox.stateChanged.connect(self.cam_ctrl.useBackground)
        view.useNPoint_checkBox.setVisible(False)  # TODO: maybe remove?
        view.useNPoint_checkBox.stateChanged.connect(self.cam_ctrl.useNPoint)
        view.feedback_checkbox.stateChanged.connect(self.toggleFeedBack)
        view.stepSize_spinBox.setVisible(False)
        view.step_size_label.setVisible(False)
        view.stepSize_spinBox.valueChanged.connect(self.cam_ctrl.setStepSize)
        view.reset_averages_button.clicked.connect(self.resetAverages)

        # Update GUI
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        # Create a nice-looking sample image
        x, y = np.meshgrid(np.arange(IMAGE_HEIGHT), np.arange(IMAGE_WIDTH))
        d = np.sqrt((x - IMAGE_HEIGHT / 2) ** 2 + (y - IMAGE_WIDTH / 2) ** 2)
        h = 2**16 - 1
        sigma = 100
        data = h * np.exp(-(d**2) / (2 * sigma**2))
        self.Image = pg.ImageItem(data)
        # Scale it to a reasonable size
        self.Image.scale(0.0134, 0.0134)

        # Make an overlay image too
        self.OverlayImage = pg.ImageItem(data)
        self.OverlayImage.scale(0.0134, 0.0134)
        self.OverlayImage.setOpacity(0.5)

        self.ImageBox = layout.addPlot()
        # Ensure that auto-ranging adds no padding to the image - maximise the size on our screen
        self.ImageBox.getViewBox().suggestPadding = lambda axis: 0.001
        self.ImageBox.addItem(self.Image)

        # Create the ROI for the mask
        self.roi = pg.EllipseROI([0, 0], [1, 1])#, movable=False)
        # self.roi.addTranslateHandle([0.5, 0.5])  # centre of ellipse
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

    def mouseMoveOverTree(self, index):
        """Most image filenames are too long to show in our little treeview. Show a persistent tooltip when the mouse
        hovers over them, so we can read the filenames."""
        treeview = self.view.overlay_treeview
        model = treeview.model()
        rect = treeview.visualRect(index)  # space occupied by the item we're hovering over
        source_index = model.mapToSource(index)
        filename = model.sourceModel().fileName(source_index)
        item_text_width = QtGui.QFontMetrics(treeview.font()).width(filename)
        if item_text_width > rect.width():  # need to show a tooltip if item size is more than viewport size
            self.make_tooltip = lambda: QtGui.QToolTip.showText(
                treeview.mapToGlobal(QtCore.QPoint(rect.left() + 18, rect.top() - rect.height() - 2)), filename, treeview)
            self.make_tooltip()
            # The tip often disappears immediately for some reason. So keep calling the function to create it for 5 seconds
            self.tooltip_start_time = time.time()
            self.tooltip_checker.start(100)
        else:  # we're over an item that doesn't need a tooltip - turn off any we might have shown previously
            self.tooltip_checker.stop()
            QtGui.QToolTip.hideText()

    def keepToolTipShown(self):
        """Function to keep the treeview tooltip shown for up to 5 seconds."""
        if time.time() - self.tooltip_start_time < 5:
            self.make_tooltip()
        else:
            self.tooltip_checker.stop()

    def folderLoaded(self, folder_name):
        """A folder has been loaded in the overlay treeview - keep trying until all depth-2 folders (days) are loaded."""
        depth = folder_name[len(hdf5_image_folder):].count('/')
        if depth < 2:
            self.view.overlay_treeview.expandToDepth(2)
        else:
            self.overlays.directoryLoaded.disconnect()  # now stop!

    def displayOverlay(self, checked):
        """Show or hide the overlay image."""
        if checked and not self.OverlayImage in self.ImageBox.items:
            self.ImageBox.addItem(self.OverlayImage)
        elif not checked:
            self.ImageBox.removeItem(self.OverlayImage)

    def overlaySelectionChanged(self, selection):
        """An overlay image has been selected - update the overlay in the GUI."""
        indices = selection.indexes()
        if len(indices) > 0:
            model = self.view.overlay_treeview.model()
            source_index = model.mapToSource(indices[0])
            filename = str(model.sourceModel().filePath(source_index))
            if filename.lower().endswith('.hdf5'):
                file = h5py.File(filename)
                data = np.array(file['Capture000001'])
                is_full_image = data.size == IMAGE_WIDTH_FULL * IMAGE_HEIGHT_FULL
                dims = IMAGE_DIMS_FULL if is_full_image else IMAGE_DIMS_VELA
                self.OverlayImage.setImage(np.flip(np.transpose(data.reshape(dims)), 1))
                max_level = self.view.max_level_spin.maximum()
                self.OverlayImage.setLevels([0, max_level], update=True)
                conv = self.pix2mm() / (2 if is_full_image else 1)
                self.OverlayImage.setRect(QtCore.QRect(0, 0, dims[1] * conv, dims[0] * conv))
                if not self.OverlayImage in self.ImageBox.items:
                    self.view.overlay_checkbox.setChecked(True)
            else:
                self.view.overlay_checkbox.setChecked(False)
        else:
            self.view.overlay_checkbox.setChecked(False)

    def pix2mm(self):
        """Return the pixel-to-mm ratio for the current screen."""
        screen_name = self.getCurrentScreen()
        ratio = self.cam_ctrl.getPix2mmDef(screen_name)
        if ratio == -999.999:
            ratio = 0.01  # better default value!
        return ratio

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
        self.view.statusbar.showMessage('Switching LEDs {}'.format('ON' if is_on else 'OFF'))
        if is_on:
            self.cam_ctrl.claraLEDOn()
            self.cam_ctrl.velaLEDOn()
        else:
            self.cam_ctrl.claraLEDOff()
            self.cam_ctrl.velaLEDOff()

    def changeColourMap(self, map_name):
        """A colour map has been selected from the dropdown box. Set the image colour map."""
        colour_list_hex = getattr(colorcet, str(map_name))
        colour_list = np.array([pg.colorTuple(pg.mkColor(code)) for code in colour_list_hex])
        colour_map = pg.ColorMap(np.linspace(0, 1, len(colour_list_hex)), colour_list)
        lookup_table = colour_map.getLookupTable()
        self.Image.setLookupTable(lookup_table)
        self.OverlayImage.setLookupTable(lookup_table)
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
        self.settings.setValue(self.cam_dict[self.getCurrentScreen()] + '/autoLevel', checked)

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

        # update the visible image files in the overlay treeview to show current camera only
        regexp = self.overlays_proxy.filterRegExp()
        regexp.setPattern(filter_regexp + '|^' + camera_name + r'.*\.hdf5$')
        self.overlays_proxy.setFilterRegExp(regexp)

    def getCurrentScreen(self):
        index = self.view.cameras_treeview.currentIndex()
        screen = self.screens.itemFromIndex(index)
        screen_name = str(screen.data().toString())
        return screen_name

    def updateROIFromMask(self):
        """The mask has changed - update the ROI."""
        mask = self.cam_ctrl.getMaskObj()
        print('got mask obj', mask.mask_x, mask.mask_y, mask.mask_x_rad, mask.mask_y_rad)
        x = mask.mask_x - mask.mask_x_rad
        y = mask.mask_y - mask.mask_y_rad
        self.roi.blockSignals(True)  # don't update the mask recursively!
        conv = self.pix2mm()
        self.roi.setPos(QtCore.QPoint(x * conv, y * conv))
        if mask.mask_x_rad > 0 and mask.mask_y_rad > 0:
            self.roi.setSize(QtCore.QPoint(mask.mask_x_rad * 2 * conv, mask.mask_y_rad * 2 * conv))
        self.roi.blockSignals(False)

    def roiChanged(self):
        """The ROI ellipse has been altered by dragging the handles. Update the mask accordingly."""
        pos, size = self.roi.pos(), self.roi.size()  # in mm
        conv = self.pix2mm()
        x, y = pos.x(), pos.y()
        x_rad, y_rad = size.x() / 2, size.y() / 2
        centre_x, centre_y = x + x_rad, y + y_rad
        status = 'Setting mask: centre ({:.3f}, {:.3f}), radius ({:.3f}, {:.3f})'
        dims = [centre_x, centre_y, x_rad, y_rad]
        self.view.statusbar.showMessage(status.format(*dims))
        set_dims = [int(d / conv) for d in dims]
        print(set_dims)
        self.cam_ctrl.setMask(*set_dims)

    def openImageDir(self):
        """Open an Explorer window at the location of the saved images."""
        folder = datetime.today().strftime(hdf5_image_folder + r'\%Y\%#m\%#d')  # omit leading zeros from month and day
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
                conv = self.cam_ctrl.getCameraObj(name).screenName.replace('YAG', 'SCR')
                screen_state = self.scr_ctrl.getScreenState(conv)
                # screen_in = screen_state in (VELA_CLARA_Screen_Control.SCREEN_STATE.V_YAG, VELA_CLARA_Screen_Control.SCREEN_STATE.YAG)
                screen_in = self.scr_ctrl.isScreenIn(conv)
                # TODO: maybe more icons for other objects (collimator, slit, graticule etc)
                item.setIcon(QtGui.QIcon(pixmap('in' if screen_in else 'out')))  # TODO: correct?

                if is_acquiring:
                    index = self.screens.indexFromItem(item)
                    self.view.cameras_treeview.setCurrentIndex(index)
                    current_camera_name = name
                    if self.scr_ctrl.isScreenMoving(conv):
                        self.view.screen_progress.setFormat('%p%')
                        pneumatic = self.scr_ctrl.isPneumatic(conv)
                        state = VELA_CLARA_Screen_Control.SCREEN_STATE
                        states = (state.V_RF, state.V_YAG) if pneumatic else (state.RETRACTED, state.YAG)
                        out_pos, in_pos = (self.scr_ctrl.getDevicePosition(conv, state) for state in states)
                        sign = np.copysign(1, in_pos - out_pos)  # in case out > in. We want 100% to be 'in', so out should be less
                        self.view.screen_progress.setRange(sign * out_pos, sign * in_pos)
                        self.view.screen_progress.setValue(sign * self.scr_ctrl.getACTPOS(conv))
                    else:
                        self.view.screen_progress.setFormat(str(screen_state))
                        self.view.screen_progress.setValue(self.view.screen_progress.maximum() if screen_in else 0)

        if current_camera_name is None:
            self.view.cameras_treeview.selectionModel().clearSelection()
            return

        # if current_camera_name != self.camera_name:
        #     self.changeCamera()

        # Set crosshairs
        analysis = cam_ctrl.getAnalysisObj(current_camera_name)
        x, y = analysis.x_mean, analysis.y_mean  # TODO: no 'y_pix_mean' !!
        sigX, sigY = analysis.sig_x_mean, analysis.sig_y_mean
        self.vLineMLE_avg.setData(x=[x, x], y=[y - sigY, y + sigY])
        self.hLineMLE_avg.setData(x=[x - sigX, x + sigX], y=[y, y])
        # print(analysis.x, analysis.y, analysis.x_pix, analysis.y_pix)
        x, y = analysis.x, analysis.y
        sigX, sigY = analysis.sig_x, analysis.sig_y
        data_ok = -999.999 not in (x, y, sigX, sigY)
        self.hLineMLE.setVisible(data_ok)
        self.vLineMLE.setVisible(data_ok)
        if data_ok:
            self.vLineMLE.setData(x=[x, x], y=[y - sigY, y + sigY])
            self.hLineMLE.setData(x=[x - sigX, x + sigX], y=[y, y])
        label_text = '''<h1>{}</h1><h2 style="color: green;">Immediate</h2>
                        <p style="color: green;"><b>Position</b>: {:.3f}, {:.3f} mm<br><b>Size (1 &sigma;)</b>: {:.3f}, {:.3f} mm<br>
                        <b>Covariance XY</b>: {:.3f} mm<sup>2</sup><br><b>Average intensity</b>: {:.3f}</p>
                        <h2 style="color: cyan;">Average ({})</h2>
                        <p style="color: cyan;"><b>Position</b>: {:.3f}, {:.3f} mm<br><b>Size (1 &sigma;)</b>: {:.3f}, {:.3f} mm<br>
                        <b>Covariance XY</b>: {:.3f} mm<sup>2</sup><br><b>Average intensity</b>: {:.3f}</p>'''
        if self.view.overlay_checkbox.isChecked():
            model = self.view.overlay_treeview.model()
            indices = self.view.overlay_treeview.selectionModel().selectedIndexes()
            source_index = model.mapToSource(indices[0])
            filename = str(model.sourceModel().filePath(source_index))
            label_text += '\n<h2>Overlay</h2>\n<p>{}</p>'.format(filename[len(hdf5_image_folder)+1:])

        self.title_label.setText(label_text.format(current_camera_name,
                                                   analysis.x, analysis.y, analysis.sig_x,
                                                   analysis.sig_y, analysis.sig_xy, analysis.avg_pix,
                                                   analysis.sig_x_n,
                                                   analysis.x_mean, analysis.y_mean, analysis.sig_x_mean,
                                                   analysis.sig_y_mean, analysis.sig_xy_mean, analysis.avg_pix_mean
                                                   ))
        # data = None  # for testing
        # pv_name = cam_ctrl.getCameraObj(current_camera_name).pvRoot + 'CAM2:ArrayData'
        data = cam_ctrl.takeAndGetFastImage()
        # data = cam_ctrl.getImageObj().data
        # data = caget(pv_name)  # this seems a bit faster than takeAndGetFastImage()
        if data is not None:
            leds_on = cam_ctrl.isClaraLEDOn() or cam_ctrl.isVelaLEDOn()
            if self.view.auto_level_checkbox.isChecked() and not leds_on:
                centile90 = np.percentile(data, 99.9)
                self.view.max_level_spin.setValue(int(centile90))

            dims = IMAGE_DIMS if len(data) == IMAGE_WIDTH * IMAGE_HEIGHT else IMAGE_DIMS_VELA
            npData = np.array(data).reshape(dims)
            self.Image.setImage(np.flip(np.transpose(npData), 1))
            max_level = self.view.max_level_spin.maximum() if leds_on else self.view.max_level_spin.value()
            self.Image.setLevels([0, max_level], update=True)
            conv = self.pix2mm()
            image_rect = QtCore.QRect(0, 0, dims[1] * conv, dims[0] * conv)
            self.Image.setRect(image_rect)

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