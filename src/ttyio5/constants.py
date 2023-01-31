from .lib import *

CSI = "\x9B"
ESC = "\033"

# https://www.c64-wiki.com/wiki/Color
# https://en.wikipedia.org/wiki/ANSI_escape_code
echocommands = (
{ "command": "{clear}",      "ansi": "2J" },
{ "command": "{home}",       "ansi": "0;0H" },
# { "command": "{clreol}",     "ansi": "K" },
# { "command": "{/all}",       "ansi": "0;39;49m" },
{ "command": "{/fgcolor}",   "ansi": "39m" },
{ "command": "{/bgcolor}",   "ansi": "49m" },

{ "command": "{bold}",       "ansi": "1m" },
{ "command": "{/bold}",      "ansi": "22m" },
{ "command": "{faint}",      "ansi": "2m" },
{ "command": "{italic}",     "ansi": "3m" },
{ "command": "{/italic}",    "ansi": "23m" },
{ "command": "{underline}",  "ansi": "4m" },
{ "command": "{/underline}", "ansi": "24m" },
{ "command": "{blink}",      "ansi": "5m" },
{ "command": "{/blink}",     "ansi": "25m" },

{ "command": "{strike}",     "ansi": "9m" },
{ "command": "{/strike}",    "ansi": "29m" },

{ "command": "{magenta}",    "ansi": "35m" },

{ "command": "{reverse}",    "ansi": "7m" },
{ "command": "{/reverse}",   "ansi": "27m" },
)

acs = {
  "ULCORNER":"l",
  "LLCORNER":"m",
  "URCORNER":"k",
  "LRCORNER":"j",
  "LTEE":    "t",
  "RTEE":    "u",
  "BTEE":    "v",
  "TTEE":    "w",
  "HLINE":   "q",
  "VLINE":   "x",
  "PLUS":    "n",
  "S1":      "o",
  "S9":      "s",
  "DIAMOND": "`",
  "CKBOARD": "a",
  "DEGREE":  "f",
  "PLMINUS": "g",
  "BULLET":  "~",
  "LARROW":  ",",
  "RARROW":  "+",
  "DARROW":  ".",
  "UARROW":  "-",
  "BOARD":   "h",
  "LANTERN": "i",
#  "BLOCK":   "0",
}

unicode = {
  "HEART":           "\u2665",
  "DIAMOND":         "\u2666",
  "CLUB":            "\u2663",
  "SPADE":           "\u2660",
  "LIGHTSHADE":      "\u2591",
  "MEDIUMSHADE":     "\u2592",
  "DARKSHADE":       "\u2593",
  "SOLIDBLOCK":      "\u2588",
  "BLOCKUPPERHALF":  "\u2580",
  "BLOCKLEFTHALF":   "\u258C",
  "BLOCKCORNER":     "\u25A0",
  "SV":              "\u2502",
  "SVSL":            "\u2524",
  "DVDL":            "\u2563",
  "DVDR":	     "\u2560",
  "DV":              "\u2551",
  "DRDVCORNER":      "\u2554",
  "DHLINE":          "\u2550",
  "DLDVCORNER":      "\u2557",
  "DVLINE":          "\u2551",
  "DVDRCORNER":	     "\u255a",
  "DVDLCORNER":  "\u255d",
  "DVDHRTEE":    "\u2560",
  "DVDHLTEE":    "\u2563",
  "DVSHRTEE":    "\u255F",
  "DVSHLTEE":	 "\u2562",
  "SVDHCROSS":   "\u256A",
  "SVSHCROSS":   "\u253C",
  "DVSHCROSS":   "\u256B",
  "DVDHCROSS":   "\u256C", # double vertical double horizontal cross
  "DIEONE":      "\u2680",
  "DIETWO":      "\u2681",
  "DIETHREE":    "\u2682",
  "DIEFOUR":     "\u2683",
  "DIEFIVE":     "\u2684",
  "DIESIX":      "\u2685",
}

# https://stackoverflow.com/questions/3220031/how-to-filter-or-replace-unicode-characters-that-would-take-more-than-3-bytes
# https://medium.com/analytics-vidhya/how-to-print-emojis-using-python-2e4f93443f7e
emoji = {
  "grin":                   "\U0001F600",
  "smile":                  "\U0001f642",
  "rofl":                   "\U0001f923",
  "wink":                   "\U0001f609",
  "thinking":               "\U0001f914",
  "sunglasses":             "\U0001f60e",
  "100":                    "\U0001f4af",
  "thumbup":                "\U0001f44d",
  "thumbdown":              "\U0001f44e",
  "vulcan":                 "\U0001f596",
  "spiral":                 "\U0001f4ab",
  "fire":                   "\U0001f525",
  "bank":                   "\U0001f3e6",
  "house":                  "\U0001f3e0",
  "military-helmet":        "\U0001fa96",
  "door":                   "\U0001f6aa",
  "receipt":                "\U0001f9fe",
  "newspaper":              "\U0001f4f0",
  "prince":                 "\U0001f934",
  "princess":               "\U0001f478",
  "thread":                 "\U0001f9f5",
  "ice":                    "\U0001f9ca",
  "moneybag":               "\U0001f4b0",
  "person":                 "\U0001f9d1",
  "sun":                    "\U00002600", # @see https://emojipedia.org/sun/
  "thunder-cloud-and-rain": "\U000026C8", # @see https://emojipedia.org/cloud-with-lightning-and-rain/
  "crop":                   "\U0001F33E", # @see https://emojipedia.org/sheaf-of-rice/
  "horse":                  "\U0001F40E", # @see https://emojipedia.org/horse/
  "cactus":                 "\U0001F335", # @see https://emojipedia.org/cactus/
  "ship":                   "\U0001F6A2", # @see https://emojipedia.org/ship/
  "wood":                   "\U0001FAB5", # @see https://emojipedia.org/wood/
  "link":                   "\U0001F517", # @see https://emojipedia.org/link/
  "anchor":                 "\U00002693", # @see https://emojipedia.org/anchor/
  "ballot-box":             "\U0001F5F3", # @see https://emojipedia.org/ballot-box-with-ballot/ @blacklist breaks monospace font
  "building":               "\U0001F3DB", # @see https://emojipedia.org/classical-building/
  "envelope":               "\U00002709", # @see https://emojipedia.org/envelope/
  "dolphin":                "\U0001F42C", # @see https://emojipedia.org/dolphin/
  "bellhop-bell":           "\U0001F6CE", # @see https://emojipedia.org/bellhop-bell/
  "hotel":                  "\U0001F3E8", # @see https://emojipedia.org/hotel/

  "waninggibbousmoon":      "\U0001F316",
  "waxinggibbousmoon":      "\U0001F314",
  "waningcrescentmoon":     "\U0001F318",
  "waxingcrescentmoon":     "\U0001F312",
  "lastquartermoon":        "\U0001F317",
  "firstquartermoon":       "\U0001F313",
  "newmoon":                "\U0001F311",
  "fullmoon":               "\U0001F315",

  "sco":                    "\U0000264F", # @see https://emojipedia.org/search/?q=zodiac
  "sag":                    "\U00002650",
  "cap":                    "\U00002651",
  "aqu":                    "\U00002652",
  "pic":                    "\U00002653",
  "ari":                    "\U00002648",
  "tau":                    "\U00002649",
  "gem":                    "\U0000264A",
  "can":                    "\U0000264B",
  "leo":                    "\U0000264C",
  "vir":                    "\U0000264D",
  "lib":                    "\U0000264E",

  "package":                "\U0001F4E6", # @since 20220907 @see https://emojipedia.org/package/
  "compass":                "\U0001F9ED", # @since 20220907
  "worldmap":               "\U0001F5FA", # @since 20220916

  "wolf":                   "\U0001F43A", # @since 20221002
  "person":                 "\U0001F9D1",
  
  "supervillian":           "\U0001F9B9", # @since 20221016
  "joker":                  "\U0001F0CF", # @since 20221127

  "warning":                "\U000026A0",
  "stopsign":               "\U0001F6D1",
}

# c64 color palette
colors = (
{ "command": "{white}",      "ansi": rgb(38, (255, 255, 255))}, # )"38;2;255;255;255m", "rgb": (255,255,255) }, # 37m
{ "command": "{red}",        "ansi": rgb(38, (136, 0, 0))}, # "38;2;136;0;0m"},
{ "command": "{cyan}",       "ansi": rgb(38, (170, 255, 238))}, # "38;2;170;255;238m"},
{ "command": "{purple}",     "ansi": rgb(38, (204, 68, 204))}, #"38;2;204;68;204m"},
{ "command": "{green}",      "ansi": rgb(38, (0, 204, 85))},#"38;2;0;204;85m"},
{ "command": "{blue}",       "ansi": rgb(38, (0, 0, 170))},#"38;2;0;0;170m"},
{ "command": "{yellow}",     "ansi": rgb(38, (238, 238, 119))},#"38;2;238;238;119m"},
{ "command": "{orange}",     "ansi": rgb(38, (221, 136, 85))},#"38;2;221;136;85m"},
{ "command": "{brown}",      "ansi": rgb(38, (102, 68, 0))},#"38;2;102;68;0m"},
{ "command": "{lightred}",   "ansi": rgb(38, (255, 119, 119))},#"38;2;255;119;119m"},
{ "command": "{darkgray}",   "ansi": rgb(38, (51, 51, 51))},#"38;2;51;51;51m"},
{ "command": "{gray}",       "ansi": rgb(38, (119, 119,119))}, # "38;2;119;119;119m"},
{ "command": "{lightgreen}", "ansi": rgb(38, (170, 255, 102))},#"38;2;170;255;102m"},
{ "command": "{lightblue}",  "ansi": rgb(38, (0, 136, 255))},#"38;2;0;136;255m"},
{ "command": "{lightgray}",  "ansi": rgb(38, (187, 187, 187))},#"38;2;187;187;187m"},
{ "command": "{black}",      "ansi": rgb(38, (0,0,0))}, # "38;2;0;0;0m"},
{ "command": "{darkgreen}",  "ansi": darken(38, (0, 204, 85), 0.20)},#  "rgb": (0,183,76) } # darken("green", 0.10)
)

bgcolors = (
    { "command": "{bgwhite}",      "ansi": rgb(48, (255, 255, 255))},#"48;2;255;255;255m", "rgb": (255,255,255) }, # 37m
    { "command": "{bgred}",        "ansi": rgb(48, (136, 0, 0))},#"48;2;136;0;0m",     "rgb": (136,0,0) }, # 31m
    { "command": "{bgcyan}",       "ansi": rgb(48, (170, 255, 238))},#"48;2;170;255;238m", "rgb": (170,255,238) }, # 36m
    { "command": "{bgpurple}",     "ansi": rgb(48, (204, 68, 204))},#"48;2;204;68;204m",  "rgb": (204, 68, 204) }, # 35m
    { "command": "{bggreen}",      "ansi": rgb(48, (0, 204, 85))},#"48;2;0;204;85m",    "rgb": (0,204,85) }, # 32m
    { "command": "{bgblue}",       "ansi": rgb(48, (0, 0, 170))},#"48;2;0;0;170m",     "rgb": (0,0,170) }, # 34m
    { "command": "{bgyellow}",     "ansi": rgb(48, (238, 238, 119))},#"48;2;238;238;119m", "rgb": (238,238,119) }, # 33m
    { "command": "{bgorange}",     "ansi": rgb(48, (221, 136, 85))},#"48;2;221;136;85m",  "rgb": (221,136,85) },
    { "command": "{bgbrown}",      "ansi": rgb(48, (102, 68, 0))},#"48;2;102;68;0m",    "rgb": (102,68,0) },
    { "command": "{bglightred}",   "ansi": rgb(48, (255, 119, 119))},#"48;2;255;119;119m", "rgb": (255, 119, 119) },
    { "command": "{bgdarkgray}",   "ansi": rgb(48, (51, 51, 51))},#"48;2;51;51;51m",    "rgb": (51, 51, 51) },
    { "command": "{bggray}",       "ansi": rgb(48, (119, 119, 119))},#"48;2;119;119;119m", "rgb": (119, 119, 119) },
    { "command": "{bglightgreen}", "ansi": rgb(48, (170, 255, 102))},#"48;2;170;255;102m", "rgb": (170, 255, 102) },
    { "command": "{bglightblue}",  "ansi": rgb(48, (0, 136, 255))},#"48;2;0;136;255m",   "rgb": (0, 136, 255) },
    { "command": "{bglightgray}",  "ansi": rgb(48, (187, 187, 187))},#"48;2;187;187;187m", "rgb": (187, 187, 187) },
    { "command": "{bgblack}",      "ansi": rgb(48, (0,0,0)) }, # "48;2;0;0;0m",       "rgb": (0,0,0) }, # 30m
    { "command": "{bgdarkgreen}",  "ansi": darken(48, (0, 204, 85), 0.20) }, # "48;2;0;183;76m",  "rgb": (0,183,76) } # darken("green", 0.10)
)
