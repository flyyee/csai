# Mock main program
# Only used as a guide

def main(win):
    # include everything to run in the main program here
    # win refers to the window for the notifications
    pass

if __name__ == "__main__":
    app = wx.App()
    win = NotifWin()
    win.show()
    app.MainLoop()
