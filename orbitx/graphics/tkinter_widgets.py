import tkinter as tk
from typing import Union, Optional

# Colour reference
BLUE = '#4d4dff'    # Text colour
BLACK = '#1a1a1a'   # Background colour
GRAY = '#b3b3b3'    # Indicator inactive
GREEN = '#009933'   # Indicator active
RED = '#cc0000'    # Alert flash
WHITE = '#d9d9d9'    # Alert flash text
DARK_GRAY = '#4d4d4d' # OneTimeButton, used

# Fonts
LARGE_FONT = ('Arial', 14)
NORMAL_FONT = ('Arial', 12)
SMALL_FONT = ('Arial', 10)


class ENGLabel(tk.Label):

    def __init__(self, parent: tk.Widget, text: str, value: Union[int, str], unit: Optional[str] = None):
        super().__init__(parent)
        self.text = text
        self.value = value
        self.unit = unit

        self.update()

    def text_decorator(self) -> str:
        if self.unit is not None:
            return self.text + ' ' + str(self.value) + ' ' + self.unit
        else:
            return self.text + ' ' + str(self.value)

    def update(self):
        self.configure(text=self.text_decorator(),
                       bg=BLACK,
                       fg=BLUE,
                       font=NORMAL_FONT,
                       anchor=tk.W,
                       justify=tk.LEFT
                       )


class ENGLabelFrame(tk.LabelFrame):

    def __init__(self, parent: tk.Widget, text: str):
        font = NORMAL_FONT
        super().__init__(parent, text=text, font=font, fg=BLUE, bg=BLACK)


class Indicator(tk.Button):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Allows for button width, height to be specified in px
        self.px_img = tk.PhotoImage(width=1, height=1)

        self.configure(image=self.px_img,
                       compound='c',
                       width=50,
                       height=50,
                       command=self.press,
                       font=NORMAL_FONT
                       )
        self.value = 1    # Will be set to 0, on next line
        self.invoke()

    def press(self):
        if self.value == 0:
            self.value = 1
            self.configure(relief=tk.RAISED,
                           bg=GREEN
                           )
        else:
            self.value = 0
            self.configure(relief=tk.SUNKEN,
                           bg=GRAY
                           )


class OneTimeButton(tk.Button):

    def __init__(self, parent, command=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Allows for button width, height to be specified in px
        self.px_img = tk.PhotoImage(width=1, height=1)

        self.configure(image=self.px_img,
                       compound='c',
                       width=100,
                       height=40,
                       font=NORMAL_FONT,
                       relief=tk.RIDGE,
                       bg=GRAY
                       )
        # TODO This doesn't work for binding multiple functions
        if command is None:
            self.configure(command=self.press)

        self.value = 0

    def press(self):
        self.configure(state=tk.DISABLED,
                       relief=tk.FLAT,
                       bg=DARK_GRAY,
                       fg=GRAY
                       )


class Alert(tk.Button):
    """TODO Fix INVIS and FLASHING"""

    def __init__(self, parent, invis: bool = False, counter:int = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # Allows for button width, height to be specified in px
        self.px_img = tk.PhotoImage(width=1, height=1)

        self.configure(image=self.px_img,
                       compound='c',
                       width=80,
                       height=35,
                       font=NORMAL_FONT,
                       state=tk.DISABLED,
                       command=self.quiet
                       )
        self.alerted = 0
        self.normal_state()

        # Invis doesn't seem to work?
        if invis:
            self.configure(fg=parent['bg'], bg=parent['bg'])

        if counter is not None:
            self.counter = counter

        self.flash_period = 450    #ms
        self.duty_cycle = 0.7    # Duty Cycle = 0.8 means turned on 80% of period

    def alert(self):
        self.alerted = 1
        #print('ALERT')
        self.alerted_state()
        # self.after(int(0.6*self.flash_time), lambda: self.normal_state())
        #self.after(int(0.6 * self.flash_time), lambda: self.configure(bg=BLACK))

    def alerted_state(self):
        #print('AS')
        self.configure(relief=tk.RAISED,
                       bg=RED,
                       fg=WHITE,
                       state=tk.NORMAL)
        if self.alerted:
            self.after(int(self.duty_cycle * self.flash_period),
                       lambda: self.normal_state())

    def normal_state(self):
        #print('NS', self.value==True)
        self.configure(relief=tk.FLAT,
                       bg=BLACK,
                       fg=GRAY,
                       )
        if self.alerted:
            self.after(int((1-self.duty_cycle)*self.flash_period),
                       lambda: self.alerted_state())

    def quiet(self):
        # Stop flashing, but stay alerted
        self.update_idletasks()    # Clear the buffer of any remaining flashes
        self.alerted = False
        self.alerted_state()
        self.configure(state=tk.DISABLED, relief=tk.GROOVE)


class ENGScale(tk.Scale):

    def __init__(self, parent, label: ENGLabel):
        super().__init__(parent)

        self.label = label

        self.configure(from_=0,
                       to_=100,
                       resolution=5,
                       orient=tk.HORIZONTAL,
                       bg=BLACK,
                       fg=GRAY,
                       troughcolor=BLACK,
                       showvalue=0,
                       command=self.update_slider_label
                       )

    def update_slider_label(self, val):
        self.label.value = val
        self.label.update()
