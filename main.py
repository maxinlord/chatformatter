from datetime import timedelta
import logging
import math
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from weightWord import weight_word
import pyfiglet
import html
import string
import wikipedia

API_TOKEN = '5664499159:AAHaLuZeCYV49sB6fMC-bB2nklXfEFHp9Ds'

# настройка логгирования
logging.basicConfig(level=logging.INFO)

# создание экземпляра бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


exists_format = '''> $r - реверс,
> $u - всё к верхнему регистру,
> $c - первое слово с большой буквы, остальные с маленькой,
> $t - каждое слово с большой буквы,
> $w - подсчет веса слов(-a), подробнее в блоге,
> $a - ASCii арт из слова(буквы),
> $e - выполняет математические функции, пример ($e5+5 -> 5+5=10)
> $/ - таким образом можно использовать символ доллара, пример($uсимвол доллара $/ хех -> СИМВОЛ ДОЛЛАРА $ ХЕХ)
> $rp[old][new] - заменяет все old буквы на new, пример ($rpst stone -> ttone),
> $at - ASCii translate перевод из букв в символы
> $tl - транслитерация с русского на английский
> $ - знак останова, пример ($ugood$ job -> GOOD job)'''

def replace_with_index(string, old: list, new: str):
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

def void_word(len=10):  # sourcery skip: avoid-builtin-shadow
    void_word = ''
    all = string.digits + string.ascii_letters
    for _ in range(len):
        a = random.choice(all)
        void_word += a
    return void_word

class TextFormatter:

    @staticmethod
    def reverse(text: str, *args) -> str:
        not_revers_symbols = ['<code>', '</code>', '$/']
        for i in not_revers_symbols:
            if i not in text:
                continue
            elif i == '<code>':
                text = text.replace(i, not_revers_symbols[1][::-1])
            elif i == '</code>':
                text = text.replace(i, not_revers_symbols[0][::-1])
            else:
                text = text.replace(i, i[::-1])
        return text[::-1]
    
    @staticmethod
    def ascii_translate(text: str):
        ascii_dict = {
            'a': '@', 'b': 'ß',
            'c': 'ℂ', 'd': '∂',
            'e': '∑', 'f': '5',
            'g': '9', 'h': '#',
            'i': '1', 'j': 'ʝ',
            'k': 'ḵ', 'l': '₤',
            'm': '爪', 'n': '₦',
            'o': 'Θ', 'p': '₽',
            'q': 'ჹ', 'r': 'ᚱ',
            's': '$/', 't': 'テ',
            'u': 'ʊ', 'v': '√',
            'w': '₩', 'x': '乂',
            'y': 'ɣ', 'z': '2'
        }
        for key in ascii_dict:
            text = text.replace(key, ascii_dict[key])
            text = text.replace(key.upper(), ascii_dict[key])
        return text
    
    @staticmethod
    def transliteration(text: str):
        ru_dict = {
            'а': 'a', 'б': 'b',
            'в': 'v', 'г': 'g',
            'д': 'd', 'е': 'e',
            'ё': 'yo', 'ж': 'zh',
            'з': 'z', 'и': 'i',
            'й': 'y', 'к': 'k',
            'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o',
            'п': 'p', 'р': 'r',
            'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f',
            'х': 'kh', 'ц': 'ts',
            'ч': 'ch', 'ш': 'sh',
            'щ': 'shch', 'ъ': '',
            'ы': 'y', 'ь': '',
            'э': 'e', 'ю': 'yu',
            'я': 'ya'
        } # необходимо заменить двойные и более буквы на одинарные из-за смещения индексов пример(щ[shch]+4)
        for key in ru_dict:
            text = text.replace(key, ru_dict[key])
            text = text.replace(key.upper(), ru_dict[key])
        return text
    
    # @staticmethod
    # def wiki(text):
    #     wikipedia.set_lang('ru')
    #     wikipedia.set_rate_limiting(True)
    #     wikipedia.set_rate_limiting(True)
    #     wikipedia.set_rate_limiting(rate_limit=2, min_wait=timedelta(milliseconds=100))
    #     try:
    #         page = wikipedia.page(text)
    #     except wikipedia.exceptions.DisambiguationError as e:
    #         results = []
    #         for ind, option in enumerate(e.options):
    #             if option == text:
    #                 continue
    #             title = option
    #             try:
    #                 description = wikipedia.summary(option, sentences=1)
    #             except:
    #                 description = 'Не найдено'
    #             input_message_content = types.InputTextMessageContent(f"{option}\n\n{description}")
    #             result = types.InlineQueryResultArticle(
    #                 id=ind,
    #                 title=title,
    #                 input_message_content=input_message_content,
    #                 description=description
    #             )
    #             results.append(result)
    #         return results
    #     except wikipedia.exceptions.PageError:
    #         return

    #     description = wikipedia.summary(page.title, sentences=1)
    #     input_message_content = types.InputTextMessageContent(f"{page.title}\n\n{description}")
    #     result = types.InlineQueryResultArticle(
    #         id=1,
    #         title=page.title,
    #         input_message_content=input_message_content,
    #         description=description
    #     )
    #     return [result]


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

    @staticmethod
    def ev(text: str, *args) -> str:
        safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos',
                 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor',
                 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10',
                 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt',
                 'tan', 'tanh']
        
        safe_dict = {}
         # adding math functions to safe_dict
        for math_func in dir(math):
            if not math_func.startswith('__'):
                safe_dict[math_func] = getattr(math, math_func)
            

        return f'{text} = {eval(text, {}, safe_dict)}'
    
    
    format_map = {
        '$r': reverse,
        '$u': upper,
        '$c': capitalize,
        '$t': title,
        '$w': weight_word,
        '$a': ascii_art,
        '$e': ev
        # '$tl' transliteration
        # '$at': ascii_translate
        # '$rp': replace
    }

    @staticmethod
    def _sign_indexing(text: str):
        text = text.strip(' ')
        list_ind = [i for i, char in enumerate(text) if char == '$'][::-1]
        if not list_ind:
            return []
        list_to_edit = []
        try:
            text[list_ind[-1]+1]
        except Exception:
            text = text[:list_ind.pop(-1)]
        border = len(text)
        for i in list_ind:
            if text[i:i+2] == '$/':
                continue
            elif text[i:i+3] == '$rp':
                ind_rp = text.index('$rp')
                list_to_edit.append([text[ind_rp:ind_rp+5], ind_rp+5, border])
                break
            elif text[i:i+3] == '$tl':
                ind_rp = text.index('$tl')
                # offset += len(result:=TextFormatter.transliteration(text[ind_rp+3:border])) - len(text[ind_rp+3:border])
                list_to_edit.append([text[ind_rp:ind_rp+3], ind_rp+3, border])
                break
            elif text[i:i+3] == '$at':
                ind_rp = text.index('$at')
                # offset += len(result:=TextFormatter.ascii_translate(text[ind_rp+3:border])) - len(text[ind_rp+3:border])
                list_to_edit.append([text[ind_rp:ind_rp+3], ind_rp+3, border])
                break
            elif text[i:i+2] in TextFormatter.format_map:
                # ind = len(list_ind)-list_ind.index(i)-1
                list_to_edit.append([text[i:i+2], i+2, border])
                break
            else:
                border = i
                list_to_edit.append([text[i:i+1], i, i+1])
        return list_to_edit

    @staticmethod
    def _format_text(text: str):
        list_to_edit = TextFormatter._sign_indexing(text)
        if not list_to_edit:
            return text
        to_clean=['스']
        for x in list_to_edit:
            if x[0] == '$':
                text = replace_with_index(text, [x[1], x[2]], '스')
                # to_clean.append('스')
                continue
            elif x[0][:3] == '$rp':
                old, new = x[0][3:]
                t = TextFormatter.replace(text[x[1]:x[2]], old, new)
                text = replace_with_index(text, [x[1]-5, x[1]], '스'*5)
                break
                # to_clean.append('스'*5)
            elif x[0] == '$at':
                t = TextFormatter.ascii_translate(text[x[1]:x[2]])
                text = replace_with_index(text, [x[1]-3, x[1]], '스'*3)
                break
                # to_clean.append('스'*3)
            elif x[0] == '$tl':
                t = TextFormatter.transliteration(text[x[1]:x[2]])
                text = replace_with_index(text, [x[1]-3, x[1]], '스'*3)
                break
                # to_clean.append('스'*3)
            else:
                t = TextFormatter.format_map[x[0]](text[x[1]:x[2]])
                text = replace_with_index(text, [x[1]-2, x[1]], '스'*2)
                break
                # to_clean.append('스'*2)
        text = replace_with_index(text, [x[1], x[2]], t)
        [text:=text.replace(i, '') for i in to_clean]
        return text
    
    @staticmethod
    def finite_format_text(text: str):
        count_dollars = text.count('$') - text.count('$/')
        for _ in range(count_dollars):
            text=TextFormatter._format_text(text)
        text = text.replace('$/', '$')
        return text



print(TextFormatter.finite_format_text('$e5+5$ good'))
# print('ss&rsss'.partition('&'))


# обработка инлайн-запросов
@dp.inline_handler()
async def inline_echo(inline_query: types.InlineQuery):
    # получаем текст запроса от пользователя
    text = inline_query.query
    description = '...'
    if text == '$info':
        _ = title = exists_format
    # elif text.startswith('$wiki'):
    #     await bot.answer_inline_query(inline_query.id, results=TextFormatter.wiki(text.strip('$wiki').strip()), cache_time=timedelta(microseconds=50))
    #     return
    elif '$' in text:
        description = 'Конфуций, 479 год до н.э'
        try:
            _ = TextFormatter.finite_format_text(text)
            title = _
        except:
            _ = title = '¯\_(ツ)_/¯'
            description = ''
    else:
        title = text
        _ = html.escape(text)
   
    # формируем ответ для пользователя
    results = [
        types.InlineQueryResultArticle(
            id='1',
            title=title,
            description=description,
            thumb_url='https://avatars.mds.yandex.net/i?id=3288914965329bedc36d4c39f7ef1552_l-5322671-images-thumbs&ref=rim&n=13',
            input_message_content=types.InputTextMessageContent(message_text=_, parse_mode='HTML'))
    ]
    # отправляем ответ пользователю
    await bot.answer_inline_query(inline_query.id, results=results, cache_time=timedelta(microseconds=50))

# запуск бота
if __name__ == '__main__':
    
    executor.start_polling(dp, skip_updates=True)
    