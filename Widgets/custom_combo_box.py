from PyQt5.QtWidgets import QComboBox

class custom_combo_box(QComboBox):
    """ Custom combo box class """
    def __init__(self, items:list) -> None:
        super(custom_combo_box, self).__init__()

        self.addItems(items)
