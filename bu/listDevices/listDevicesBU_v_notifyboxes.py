

#Install:    min python3.5 requiered
#            
import evdev, asyncio, sys, os

DOWN = 1
UP = 0
HOLD = 2

scancodes = {
        # Scancode: ASCIICode
        1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
        10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'x', 17: u'v', 18: u'l', 19: u'c',
        20: u'w', 21: u'k', 22: u'h', 23: u'g', 24: u'f', 25: u'q', 26: u'ß', 27: u']', 28: u'CRLF', 29: u'LCTRL',
        30: u'u', 31: u'i', 32: u'a', 33: u'e', 34: u'o', 35: u's', 36: u'n', 37: u'r', 38: u't', 39: u'd',
        40: u'y', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'ü', 45: u'ö', 46: u'ä', 47: u'p', 48: u'z', 49: u'b',
        50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u'SPACE', 58: u'MOD2', 86: u'MOD3', 97: u'RCTRL', 100: u'RALT'
        }

def isKeyEvent(event):
    if event.type == evdev.ecodes.EV_KEY:
        return 1

def checkUpperOrDownerCase(event,old_val):
    keyevent = evdev.categorize(event)
    shift = 1 if (keyevent.scancode == 42 or keyevent.scancode == 54) else 0

    if shift:
        if keyevent.keystate == DOWN or keyevent.keystate == HOLD:
            return 'UPPER'
        else:
            return 'DOWNER'

    else:
        return old_val

def collectLetterForWord(keyevent):
    if keyevent.keystate == UP:
        return ""

    try:
        letter = scancodes.get(keyevent.scancode) 
        letter = "" if (letter is None) else letter
        letter = "" if (len(letter) > 1 and letter != 'SPACE') else letter
    except:
        print("No mapping yet.")
        letter = ""

    return letter




async def print_events(device):
    word = ""
    case = 'DOWNER'

    async for event in device.async_read_loop():
        if isKeyEvent(event):
            case = checkUpperOrDownerCase(event, case)
            letter = collectLetterForWord(evdev.categorize(event))
            letter = letter.upper() if case == 'UPPER' else letter

            if letter == "SPACE":
                print(word)
                os.system('notify-send ' + word)

                    #SEND TO FILE
                word = ""
            else:
                word = word + letter



device = evdev.InputDevice('/dev/input/event3')
asyncio.ensure_future(print_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()

easygui.msgbox("This is a message!", title="simple gui")

