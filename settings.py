import os
from utils import toHex

# do not touch this:
SRC_DIR = "/".join(os.path.realpath(__file__).split("/")[:-1])


SCREEN_SIZE = (1920, 1080)

# define the initial screen size
WINDOW_SIZE = (1000, 500)



MAIN_FONT = "Lucida Sans"

# DO NOT NEED TO MODIFY THESE:
SMALL_FONT = (MAIN_FONT, 8)
SMALL_BOLD_FONT = (MAIN_FONT, 8, "bold")
FONT = (MAIN_FONT, 10)
BOLD_FONT = (MAIN_FONT, 10, "bold")
MED_FONT = (MAIN_FONT, 12)
LARGE_FONT = (MAIN_FONT, 18, "bold")



'''
#TODO: can we get rid of most of these?
BG_DARK_f = (0.1, 0.1, 0.1)
BG_DARK = toHex(BG_DARK_f)

BG_LIGHT_f= (0.2, 0.2, 0.2)
BG_LIGHT= toHex(BG_LIGHT_f)



PRIMARY_f = (0.258824, 0.521569, 0.956863)#(0.0, 0.65, 1.0)
#PRIMARY_f = (0.0, 1.0, 0.2)
PRIMARY = toHex(PRIMARY_f)

LIGHT_PRIMARY_f = tuple([v*0.4 + 0.6*1 for v in PRIMARY_f])
LIGHT_PRIMARY = toHex(LIGHT_PRIMARY_f)

DARK_PRIMARY_f = tuple([v*0.5 + 0.5*0 for v in PRIMARY_f])
DARK_PRIMARY = toHex(DARK_PRIMARY_f)

COMPLEMENT_f = tuple([1.0-v for v in PRIMARY_f])
COMPLEMENT = toHex(COMPLEMENT_f)

#LIGHT_PRIMARY = toHex((1.0, 0.85, 0.5))
#PRIMARY = toHex((1.0, 0.5, 0.0))
#DARK_PRIMARY = toHex((0.5, 0.25, 0.0))
'''
