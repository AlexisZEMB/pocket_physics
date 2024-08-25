from PyQt5.QtWidgets import QSlider

class custom_slider_bar(QSlider):
    """ Custom slider bar class """
    def __init__(self, min:int, max:int, default_value:int, tickInterval:int) -> None:
        super(custom_slider_bar, self).__init__() 

        self.setMinimum(min)
        self.setMaximum(max)
        self.setValue(default_value)
        self.setTickInterval(tickInterval)
        self.setOrientation(1)



