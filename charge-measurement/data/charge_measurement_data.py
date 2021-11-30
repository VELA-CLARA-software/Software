import data.charge_measurement_data_base as dat


class charge_measurement_data(dat.charge_measurement_data_base):
    # whoami
    my_name = 'charge_measurement_data'

    main_monitor_states = {}
    previous_main_monitor_states = {}

    def __init__(self):
        dat.charge_measurement_data_base.__init__(self)
        self.values = dat.charge_measurement_data_base.values