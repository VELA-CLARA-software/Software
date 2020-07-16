class UnifiedController:
    """ Unified Controller class"""

    def __init__(self, m_ControllerRun):
        self.rpc = m_ControllerRun
        self.rpc.view.IMGpushButton.clicked.connect(self.run_rpc_process)

    def run_rpc_process(self):
        self.rpc.disable_run_button()
        self.rpc.app_sequence()
