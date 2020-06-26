from PyQt5.QtCore import *


class UnifiedController:
    """ Unified Controller class"""

    def __init__(self, m_ControllerRun, m_ControllerPostProcessing):
        self.rpc = m_ControllerRun
        self.ppc = m_ControllerPostProcessing
        self.rpc.view.IMGpushButton.clicked.connect(self.run_rpc_process)

    def run_rpc_process(self):
        self.rpc.disable_run_button()
        self.rpc.app_sequence()

        # def run_rpc_process(self):
        #    self.rpc.disable_run_button()
        #    self.rpc.run_thread(self.rpc.app_sequence)
        #    self.rpc.thread.start()

        # def run_ppc_process(self):
        # self.ppc.disable_run_postproc_button()
        # self.ppc.app_sequence_post()
        # self.ppc.enable_run_postproc_button()
        # #self.ppc.run_thread(self.ppc.app_sequence_post)
        # #self.ppc.thread.start()
