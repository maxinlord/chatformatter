import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from weightWord import weight_word
import pyfiglet

API_TOKEN = '5664499159:AAGW7_RzX4mhsb7_bBT7VyBr7Qg_N75-AVA'

# настройка логгирования
logging.basicConfig(level=logging.INFO)

# создание экземпляра бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


exists_format = '''> &r - реверс
> &u - всё к верхнему регистру
> &c - первое слово с большой буквы, остальные с маленькой
> &t - каждое слово с большой буквы
> &rp[old][new] - заменяет все old буквы на new, пример (&rpst stone -> ttone),
> &w - подсчет веса слов(-a), подробнее в блоге
> &a - ASCii арт из слова(буквы) 
> & - знак останова'''

def replace_with_index(string, old: list, new):
    return string[:old[0]] + new + string[old[1]:]

def is_russian_letter(letter):
    code_point = ord(letter)
    return code_point >= 0x0400 and code_point <= 0x04FF

def is_english_letter(letter):
    code_point = ord(letter)
    return (code_point >= 0x0041 and code_point <= 0x005A) or (code_point >= 0x0061 and code_point <= 0x007A)


def is_english_word(word):
    for letter in word:
        if not is_english_letter(letter):
            return False
    return True

class TextFormatter:

    @staticmethod
    def reverse(text: str, *args) -> str:
        return text[::-1]
    
    @staticmethod
    def ascii_art(char: str, *args) -> str:
        russian_fonts = ['graceful', 'banner']
        font = russian_fonts[1]
        if is_english_word(char):
            eng_fonts = ['whimsy', 'univers']
            font = eng_fonts[0]
        art = pyfiglet.figlet_format(text=char, font=font)
        return f'<code>{art}</code>'

    @staticmethod
    def upper(text: str, *args) -> str:
        return text.upper()

    @staticmethod
    def capitalize(text: str, *args) -> str:
        return text.capitalize()
    
    @staticmethod
    def title(text: str, *args) -> str:
        return text.title()
    
    @staticmethod
    def replace(text: str, *args) -> str:
        old, new = args
        return text.replace(old, new)

    format_map = {
        '&r': reverse,
        '&u': upper,
        '&c': capitalize,
        '&t': title,
        '&w': weight_word,
        '&a': ascii_art
        # '&rp': replace
    }

    @staticmethod
    def format_text(text: str):
        text = text.strip(' ')
        list_ind = [i for i, char in enumerate(text) if char == '&']
        list_to_edit = []
        try:
            text[list_ind[-1]+1]
        except Exception:
            list_ind.pop(-1)
        ind_back = -2
        q = []
        for i in list_ind:
            # if text[i:].partition('&rp')[1] != '':
            if text[i:i+3] in '&rp':
                ind_rp = text.index('&rp')
                list_to_edit.append([text[ind_rp:ind_rp+5], ind_rp+5, len(text)])
                q.append(1)
                # list_ind.remove(ind_rp)
                # continue
                # list_to_edit.append([text[i:i+2], i, -1])
            elif text[i:i+2] in TextFormatter.format_map:
                # ind = len(list_ind)-list_ind.index(i)-1
                list_to_edit.append([text[i:i+2], i+2, len(text)])
                q.append(1)
            else:
                if q[-1] == 1:
                    list_to_edit[-1][-1] = i
                else:
                    list_to_edit[ind_back][-1] = i
                    ind_back += -1
                q.append(0)
            
        to_clean=[]
        for x in list_to_edit[::-1]:
            if x[0][:3] == '&rp':
                old, new = x[0][3:]
                t = TextFormatter.replace(text[x[1]:x[2]], old, new)
                to_clean.extend((x[0], x[0][::-1]))
            else:
                t = TextFormatter.format_map[x[0]](text[x[1]:x[2]])
            text = replace_with_index(text, [x[1], x[2]], t)
        [text:=text.replace(i, '') for i in to_clean]
        [text:=text.replace(i, '') for i in TextFormatter.format_map]
        [text:=text.replace(i[::-1], '') for i in TextFormatter.format_map]
        text = text.replace('&', '')
        return text



# print(TextFormatter.format_text('&r&adoom'))
# print('ss&rsss'.partition('&'))


# обработка инлайн-запросов
@dp.inline_handler()
async def inline_echo(inline_query: types.InlineQuery):
    # получаем текст запроса от пользователя
    text = inline_query.query
    description = '...'
    if text == '&func':
        _ = exists_format
    elif '&' in text:
        description = 'Конфуций, 479 год до н.э'
        try:
            _ = TextFormatter.format_text(text)
        except:
            _ = '¯\_(ツ)_/¯'
            description = ''
    else:
        _ = text
   
    # формируем ответ для пользователя
    results = [
        types.InlineQueryResultArticle(
            id='1',
            title=_,
            description=description,
            thumb_url='https://avatars.mds.yandex.net/i?id=3288914965329bedc36d4c39f7ef1552_l-5322671-images-thumbs&ref=rim&n=13',
            input_message_content=types.InputTextMessageContent(message_text=_, parse_mode='HTML'))
    ]
    # отправляем ответ пользователю
    await bot.answer_inline_query(inline_query.id, results=results)

# запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
