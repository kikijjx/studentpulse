from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, load_model
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.optimizers import Adam
import pandas as pd
import pickle
from keras.models import save_model
from sklearn.utils import class_weight

# Загрузка данных
df = pd.read_csv('datasets/spamdata_ru.csv', sep='`')
class_counts = df['class'].value_counts()

print("Количество встречающихся классов:")
print(class_counts)
# Преобразование целевой переменной
label_encoder = LabelEncoder()
df['class'] = label_encoder.fit_transform(df['class'])

# Разделение данных
train_data, test_data, train_labels, test_labels = train_test_split(
    df['message'], df['class'], test_size=0.2, random_state=42
)

# Токенизация текста
max_words = 10000
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_data)

# Сохранение токенизатора
with open(f'tokenizers/tokenizer_spam.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Преобразование в последовательности и дополнение нулями
train_sequences = tokenizer.texts_to_sequences(train_data)
test_sequences = tokenizer.texts_to_sequences(test_data)

max_sequence_length = 100
train_data_pad = pad_sequences(train_sequences, maxlen=max_sequence_length)
test_data_pad = pad_sequences(test_sequences, maxlen=max_sequence_length)

# Создание модели
embedding_dim = 100  # Увеличил размерность эмбеддингов
model = Sequential()
model.add(Embedding(input_dim=max_words, output_dim=embedding_dim, input_length=max_sequence_length))
model.add(LSTM(units=100, return_sequences=True))
model.add(LSTM(units=100))
model.add(Dropout(0.5))  # Добавил слой Dropout
model.add(Dense(units=1, activation='sigmoid'))

# Компиляция модели
model.compile(optimizer=Adam(learning_rate=0.00001), loss='binary_crossentropy', metrics=['accuracy'])

# Обучение модели
weight_for_0 = 0.5  # Вес для класса ham
weight_for_1 = 5.0  # Вес для класса spam

class_weighted = {0: weight_for_0, 1: weight_for_1}

model.fit(train_data_pad, train_labels, epochs=20, batch_size=16, validation_split=0.2, class_weight=class_weighted)

# Сохранение модели
save_model(model, 'models/model_spam_updated.keras')
