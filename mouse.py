import pyautogui
import math

# Constants
SCREEN_SIZE = pyautogui.size()
SCREEN_CENTER_X = SCREEN_SIZE[0]//2
SCREEN_CENTER_Y = SCREEN_SIZE[1]//2
MOVE_DURATION = 0.2

# Function to move mouse
def move_mouse(player, dest, m_yaw=0.022, m_pitch=0.022, sens=1):
    """
    All angles should be in degrees
    player and dest parameters are tuples in the form of (yaw, pitch)
    """
    move_yaw = ((dest[0]-player[0])%180)/(m_yaw*sens)
    move_pitch = ((dest[0]-player[0])%180)/(m_pitch*sens)

    pyautogui.click()
    pyautogui.dragRel(-move_yaw, move_pitch, duration=MOVE_DURATION, button="left")
