"""
Dialogs for the application.
Note that they can be used either with:
    result = await [app or window].dialog(MyDialog())
or
    dialog = MyDialog()
    dialog.show()
    result = await dialog
"""

from toga.window import Window
from toga.widgets.textinput import TextInput
from toga.widgets.button import Button
from toga.widgets.box import Box

class AddTransactionDialog(Window):
    def __init__(self):
        super().__init__(title="Add Transaction", resizable=False, size=(400, 300))

        self.textinput = TextInput()
        self.ok_button = Button("OK", on_press=self.on_accept)
        self.content = Box(children=[self.textinput, self.ok_button])
        self.future = self.app.loop.create_future()

    def on_accept(self, widget, **kwargs):
        self.future.set_result(self.textinput.value)
        self.close()
        return widget

    def __await__(self):
        return self.future.__await__()
    
    def _show(self, widget):
        self.show()
        return self.future