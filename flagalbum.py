
# changelog

# - removed Kosovo (xk) from special codes ('sp') list

# 2024-08-03
# - expanded menu to listprovide a flags not yet obtained
# - adjusted count to include 'unobtainable' flags
# - modified definition of flags directory to not hardcode username

# 2024-09-01
# - removed eu (European Union) from exceptions
# - moved ap (Asia-Pacific Region) from ub to sp
# - made ub a list instead of a dictionary
# - created dict 'rename_list' to handle renaming of code entries
# - delegated colours to variables
# - made flag count dynamic instead of hardcoded
# - info menu now includes flag count out of obtainable and total flags

import os, string, csv, requests
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


def csv2dic(filepath):
    with open(filepath) as csv_file:
        t = list(csv.reader(csv_file, delimiter=':'))
        
    d = {a:b for a,b in [j.split(';') for i in t for j in i]}
    return d


# this is the directory used by the program to see which flags have been obtained.
flagdir = os.path.expanduser('~') + r'/Desktop/flags/0 national flags/'

url = "https://raw.githubusercontent.com/louarn-rous/csv-resources/main/ISO_3166-1_alpha-2.csv"
lines = requests.get(url).text.split('\n')
d1 = {a:b for a,b in [i.replace('\r','').split(';') for i in lines[:-1]]}

#d1 = csv2dic(r'/home/lain/Documents/dat_ref/ISO_3166-1_alpha-2.csv')

# special codes
sp = {
    'ap':'Asia-Pacific Region',
    'xx':'???',
    'xe':'England',
    'xs':'Scotland',
    'xw':'Wales'
    }

# unobtainable codes
ub = [
    'ap', # Asia-Pacific Region (special)
    'bv',  # Bouvet Island
    'eh', # Western Sahara
    'eu', # Europe(an Union)
    'um', # United States Minor Outlying Islands
    'hm' # Heard Island and McDonald Islands
    ]

# codes not to be included
exceptions = [
    'ac', # Ascension Island (already counted as part of SH)
    'cp', # Clipperton Island
    'cq', # Island of Sark
    'dg', # Diego Garcia
    'ea', # Ceuta, Melilla
    'ez', # Eurozone
    'fx', # France, Metropolitan
    'ic', # Canary Islands
    'su', # Soviet Union
    'ta', # Tristan da Cunha (already counted as part of SH)
    'uk', # already has GB
    'un'  # United Nations
    ]

# codes to be renamed
rename_list = {
    'eu':'Europe', # ISO entry is 'European Union'
    'fj':'Fiji Islands', # ISO entry is 'Fiji'
    'fk':'Falklands', # ISO entry is 'Falkland Islands'
    'kp':'North Korea', # ISO entry is 'Democratic People's Republic of Korea'
    'kr':'South Korea', # ISO entry is 'Republic of Korea'
    'sh':'Saint Helena, Ascension, and Tristan da Cunha',
    'tr':'Turkey', # ISO entry is 'Türkiye'
    'um':'U.S. Minor Outlying Islands', # full is 'United States ...'
    'us':'United States', # '... of America'
    'va':'Holy See (Vatican City State)', # ISO entry does not include '(Vatican City State)'
    'vg':'British Virgin Islands', # unusure. just a guess for consistency
    'vi':'U.S. Virgin Islands' # full is 'United States ...'
    }

# define larger codes dictionary as the union of the regular ISO 3166-1 alpha-2 codes, special codes and unobtainable codes
code_dict = {}

for key in d1.keys():
    if not(key in exceptions):
        code_dict[key] = d1[key]

code_dict |= sp

for key in rename_list.keys():
    code_dict[key] = rename_list[key]

count_total = len(code_dict.keys())
count_obt = len([i for i in code_dict.keys() if not (i in ub)])
    

class flagtile:
    def __init__(self, x, y, code):
        self.x = x
        self.y = y
        self.code = code
        self.image = pygame.image.load(f'{flagdir}{code}.gif')
        self.rect = pygame.Rect(x, y, 16, 11)
        flaglist.append(self)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def tt(self):
        z = code_dict[self.code] if self.code in code_dict.keys() else '???'
        
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            
            df_x = s_font.size(z)[0] + 8 if pygame.mouse.get_pos()[0] + s_font.size(z)[0] + 8 > SCREEN_WIDTH else 0
            df_y = 15 if pygame.mouse.get_pos()[1] + 15 > SCREEN_HEIGHT else 0
                    
            ttrect = pygame.Rect(pygame.mouse.get_pos()[0] - df_x, pygame.mouse.get_pos()[1] - df_y, s_font.size(z)[0] + 8, 15)
        
            pygame.draw.rect(screen, C_WHITE, ttrect, width=0)
            pygame.draw.rect(screen, C_BLACK, ttrect, width=1)
            screen.blit(s_font.render(z, False, C_BLACK), (ttrect.x + 4, ttrect.y + 2))
            
flaglist = []

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 460, 325
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
s_font = pygame.font.SysFont('Consolas',12)
pygame.mouse.set_visible(False)
pygame.display.set_caption('flagalbum')

# colours
C_BLACK = (0,0,0)
C_DARK = (48,48,48)
C_LIGHT = (192,192,192)
C_MEDIUM = (128,128,128)
C_WHITE = (255,255,255)

missinglist = []

for i,a in enumerate(string.ascii_lowercase):
    for j,b in enumerate(string.ascii_lowercase):
        if f'{a}{b}' in code_dict.keys():
            if os.path.exists(f'{flagdir}{a}{b}.gif'):
                p = flagtile(18 + j*17, 13 + i*12, f'{a}{b}')
            elif f'{a}{b}' not in exceptions:
                cndastx = '* ' if f'{a}{b}' in ub else ''
                missinglist.append(cndastx + code_dict[f'{a}{b}'])
                


while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                break
        if event.type == pygame.QUIT:
            pygame.quit()
            break
            
    try:
        screen.fill((255,255,255))
    except:
        break

    for i,a in enumerate(string.ascii_lowercase):
        for j,b in enumerate(string.ascii_lowercase):
            rect = pygame.Rect(18 + j*17, 13 + i*12, 16, 11)

            if f'{a}{b}' in (sp.keys() | ub):
                TILE_C = C_MEDIUM
            elif f'{a}{b}' in code_dict.keys():
                TILE_C = C_LIGHT
            else:
                TILE_C = C_DARK

            pygame.draw.rect(screen, TILE_C, rect, width=0)
                
                

    for i in range(28):
        pygame.draw.line(screen, C_BLACK, (0,12*i), (460,12*i))
        pygame.draw.line(screen, C_BLACK, (17*i,0), (17*i,325))
        if i <= 25:
            screen.blit(s_font.render(string.ascii_lowercase[i], False, C_BLACK), (24 + i*17, 1))
            screen.blit(s_font.render(string.ascii_lowercase[i], False, C_BLACK), (7, 13 + i*12))

    for i in flaglist: i.draw()
    for i in flaglist: i.tt()

    if pygame.Rect(1, 1, 16, 11).collidepoint(pygame.mouse.get_pos()):

        # if hovering above the topmost leftmost rectangle:
        
        nflags = len(os.listdir(flagdir))

        ttlines = [f'{str(nflags)}/{count_obt} ({str(nflags)}/{count_total}) - {str(round(100 * nflags/count_obt, 1))}%',
                   '',
                   'NOT YET OBTAINED:'] \
                   + [f'- {i}' for i in missinglist] \
                   + ['',
                    '(* = de facto unobtainable)']

        height = len(ttlines) * 12 + 2
        width = max([s_font.size(i)[0] for i in ttlines]) + 8

        krect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], width, height)
        
        pygame.draw.rect(screen, C_WHITE, krect, width=0)
        pygame.draw.rect(screen, C_BLACK, krect, width=1)

        for j,line in enumerate(ttlines):
        
            screen.blit(s_font.render(line, False, C_BLACK),(krect.x + 4, krect.y + 2 + j*12))

    pygame.draw.circle(screen, C_WHITE, pygame.mouse.get_pos(), 2, width=0)
    pygame.draw.circle(screen, C_BLACK, pygame.mouse.get_pos(), 2, width=1)

    pygame.display.flip()
    fpsClock.tick(FPS)
