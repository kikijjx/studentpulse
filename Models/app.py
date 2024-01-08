from ratings_test import get_ratings
from mat_test import get_mat
from spam_test import get_spam
input_text = 'very good'

print('Cпам:')
print(get_spam(input_text))
print('Нецензурная лексика:')
print(get_mat(input_text))
print('Оценки:')
print(get_ratings(input_text))