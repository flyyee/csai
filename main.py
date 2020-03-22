import wx
import sys

from notif import NotifWin

# Mock main program
# Only used as a guide

def main(win):
    # include everything to run in the main program here
    # win refers to the window for the notifications
    pass

if __name__ == "__main__":
    cmd_args = sys.argv
    help_loc = cmd_args[1] if len(cmd_args) > 1 else "UPPER_LEFT"
    app = wx.App()
    win = NotifWin(help_loc)
    app.MainLoop()
