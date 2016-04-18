



from evdev import UInput, ecodes as e
import time


DOWN = 1
UP = 0
KEY_RIGHTSHIFT = 54

scancodes = {
        # Scancode: ASCIICode
        1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
        10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'x', 17: u'v', 18: u'l', 19: u'c',
        20: u'w', 21: u'k', 22: u'h', 23: u'g', 24: u'f', 25: u'q', 26: u'ß', 27: u']', 28: u'CRLF', 29: u'LCTRL',
        30: u'u', 31: u'i', 32: u'a', 33: u'e', 34: u'o', 35: u's', 36: u'n', 37: u'r', 38: u't', 39: u'd',
        40: u'y', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'ü', 45: u'ö', 46: u'ä', 47: u'p', 48: u'z', 49: u'b',
        50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u'SPACE', 58: u'MOD2', 86: u'MOD3', 97: u'RCTRL', 100: u'RALT'
        }


def mapToCorrectScancode(letter):

    try:
        scancode = list(scancodes.keys())[list(scancodes.values()).index(letter)]

        scancode = "16" if (scancode is None) else scancode
    except:
        scancode = "16"

    return scancode

def writeUiCase(letter, ui, case='lower'):
    scancode = mapToCorrectScancode(letter)

    if case == 'lower':
        ui.write(e.EV_KEY, e.ecodes[e.KEY[scancode]], DOWN)  
        ui.write(e.EV_KEY, e.ecodes[e.KEY[scancode]], UP) 
    else:
        ui.write(e.EV_KEY, e.ecodes[e.KEY[KEY_RIGHTSHIFT]], DOWN)  

        ui.write(e.EV_KEY, e.ecodes[e.KEY[scancode]], DOWN)  
        ui.write(e.EV_KEY, e.ecodes[e.KEY[scancode]], UP) 

        ui.write(e.EV_KEY, e.ecodes[e.KEY[KEY_RIGHTSHIFT]], UP)  


def writeWord(word):
    listOfLetters = list(word)
    
    
    ui = UInput()
    
    for letter in listOfLetters:
        if letter.isupper():
            letter = letter.lower()
            case = 'upper'
        else:
            case = 'lower'

        writeUiCase(letter, ui, case)

    ui.syn()
    ui.close()

time.sleep(2)

writeWord('hahahaMotherFucker')









