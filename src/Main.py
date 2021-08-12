import os
import sys
import base64
from time import sleep
from UserInterface import Art, Check

if(os.path.getsize("Keys.py") == 0):
    Art()
    print("ERROR FILE HOUSING API KEYS EMPTY, INPUT CREDENTIALS WHEN PROMPTED")

    kuKey = input("\nKuCoin API Key(REQUIRED): ")
    kuSecret = input("\nKuCoin API Secret(REQUIRED): ")
    kuPass = input("\nKuCoin API Password(REQUIRED): ")
    sheetName = input("\nGoogle Sheet Name(REQUIRED): ")

    file = open("Keys.py", "w")
    file.write("\nkuKey = \"" + str(base64.b64encode(bytes(kuKey, "utf-8"))).removeprefix("b'").removesuffix("'") + "\"")
    file.write("\nkuSecret = \"" + str(base64.b64encode(bytes(kuSecret, "utf-8"))).removeprefix("b'").removesuffix("'") + "\"")
    file.write("\nkuPass = \"" + str(base64.b64encode(bytes(kuPass, "utf-8"))).removeprefix("b'").removesuffix("'") + "\"")
    file.write("\nsheetName = \"" + sheetName + "\"")
    file.close()

try:
    from Keys import sheetName
except:
    print("ERROR \"sheetName\" NOT FOUND IN KEYS.PY, FLUSHING KEYS.PY")
    file = open("Keys.py", "w")
    file.flush()
    file.close()
    sys.exit()

Art()
print("Hello! Thank you for downloading OmniBuy Developed by Andre Ceschia\n")

while True:
    userInput = input("\nbot > ")
    Check(userInput)