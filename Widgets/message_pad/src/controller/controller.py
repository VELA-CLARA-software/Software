


from src.data.data import data
from src.procedure.procedure import procedure
from src.gui.gui import gui



class controller(object):




    def __init__(self, argv):
        object.__init__(self)
        self.my_name = "controller"
        self.argv = argv
        print('controller created with arguments',self.argv)

        # create the objects used in th edesign
        self.data = data()
        self.proccedure = procedure()
        self.gui = gui()
        self.hello()
        self.gui.show()

    def hello(self):
        print(self.my_name+ ' says hello')
        self.data.hello()
        self.proccedure.hello()
        self.gui.hello()
