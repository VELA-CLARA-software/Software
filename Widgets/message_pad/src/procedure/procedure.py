


class procedure(object):


    def __init__(self):
        # super(base, self).__init__()
        object.__init__(self)
        self.my_name = "procedure"

    def hello(self):
        print(self.my_name+ ' says hello')