import wx

class NotifWin(wx.Frame):
    def __init__(self, x=0, y=0, width=500, height=300):
        self.x, self.y = x, y
        self.width, self.height = width, height
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
        self.SetTransparent( 220 )
        self.Show(True)
    def pushNotif(self, title="", content=""):
        pass
    def close(self):
        self.Close(force=True)

app = wx.App()
win = NotifWin()
app.MainLoop()
