import pyfiglet

art = pyfiglet.figlet_format('maks')
# print(art)


# for i in pyfiglet.FigletFont.getFonts():
#     art = pyfiglet.figlet_format('maks', font=i)
#     print(art, i)

a = 'whimsy, univers, thick, smkeyboard, smisome1'
# def format(text: str):
#     formats = ['&r', '&u']
#     ls_words = text.split(' ')
#     ls_words2 = []
#     for ind, word  in enumerate(ls_words):
#         for x in formats:
#             prt = list(word.partition(x))
#             if prt[1] == '':
#                 ls_words[ind] = prt[0]
#                 continue
#             ls_words[ind] = (prt[0]+prt[2])
#     # ls_words2.insert(0, x)



#     print(ls_words)

# format('&uThis is&r an apple')
# format('&rThis is&&u an& apple')
# 