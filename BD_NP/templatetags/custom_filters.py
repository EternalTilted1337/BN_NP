from django import template


register = template.Library()

#CURRENCIES_SYMBOLS = {
   #'rub': 'Р',
   #'usd': '$',
#}

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value):
   """
   value: значение, к которому нужно применить фильтр
   """
   # Возвращаемое функцией значение подставится в шаблон.
   return f'{value} Р'


# @register.filter()
# def censor(value):
#    bad_words = ['word1', 'word2']
#
#    for word in bad_words:
#       value = value.replace(word, '*' * len(word))
#
#    return value