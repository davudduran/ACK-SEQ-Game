import os,pyautogui,time,sys
from pathlib import Path

parent = Path(__file__).parent
server_path = parent.joinpath("server.py")
client_path = parent.joinpath("client.py")

os.system("wt")
time.sleep(1)
pyautogui.typewrite("cls")
pyautogui.press("return")
pyautogui.typewrite("{} {}".format(sys.executable, server_path))
pyautogui.press("return")
pyautogui.hotkey("alt", "shift", "d")
time.sleep(1)
pyautogui.typewrite("cls")
pyautogui.press("return")
pyautogui.typewrite("{} {}".format(sys.executable, client_path))
pyautogui.press("return")