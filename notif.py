import wx

TITLESIZE = 30
TEXTSIZE = 18
LR_PADDING = 5

def main(win):
    win.pushNotif(
        "Help Page",
        "Iterations since last update: {}".format(win.counter)
    )
    print("Pushed notification")

class NotifWin(wx.Frame):
    def __init__(self, loc="UPPER_LEFT", width=500, height=300):
        scr_width, scr_height = wx.DisplaySize()
        locs = {
            "UPPER_LEFT": (0, 0),
            "UPPER_RIGHT": (scr_width-width, 0),
            "LOWER_LEFT": (0, scr_height-height),
            "LOWER_RIGHT": (scr_width-width, scr_height-height)
        }
        self.x, self.y = locs[loc]
        print(self.x, self.y)
        self.width, self.height = width, height

        # Initialise frame and panel
        style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                  wx.NO_BORDER | wx.FRAME_SHAPED  )
        wx.Frame.__init__(
            self,
            None,
            title='CS-AI',
            pos=(self.x, self.y),
            size=(self.width, self.height),
            style=style
        )
        self.panel = wx.Panel(self)

        # Set timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(1000)

        # Set displays
        self.title = wx.StaticText(
            self.panel,
            pos=(0, 20),
            size=(self.width, TITLESIZE+20),
            style=wx.ALIGN_CENTRE_HORIZONTAL
        )
        self.title.SetFont(wx.Font(
            TITLESIZE,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            underline=True
        ))
        self.notif = wx.StaticText(
            self.panel,
            pos=(LR_PADDING, TITLESIZE+25),
            size=(self.width-2*LR_PADDING, self.height-TITLESIZE-25),
            style=wx.ALIGN_LEFT
        )
        self.notif.SetFont(wx.Font(
            TEXTSIZE,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL
        ))
        self.notif.Wrap(self.width)
        self.SetTransparent( 220 )

        self.Show(True)

        self.counter = 0

    def pushNotif(self, title="", content=""):
        self.title.SetLabel(title)
        self.notif.SetLabel(content)

    def update(self, event):
        # main code for other components over here
        main(self)
        self.counter += 1

    def close(self):
        self.Close(force=True)

# Stuff to put in main program
app = wx.App()
win = NotifWin(loc="LOWER_RIGHT")
app.MainLoop()
