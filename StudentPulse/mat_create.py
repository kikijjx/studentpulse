from keras.preprocessing.text import Tokenizer
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
import pandas as pd
import pickle

# Загрузка данных
df = pd.read_csv('datasets/distortion_train.tsv', sep='\t')

# Преобразование целевой переменной
label_encoder = LabelEncoder()
df['target'] = label_encoder.fit_transform(df['target'])

# Разделение данных
train_data, test_data, train_labels, test_labels = train_test_split(
    df['doc'], df['target'], test_size=0.2, random_state=42
)

class_counts = df['target'].value_counts()
print("Количество встречающихся классов:")
print(class_counts)

# Токенизация текста
max_words = 10000
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_data)

# Сохранение токенизатора
with open(f'tokenizers/tokenizer_mat.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Преобразование в последовательности и дополнение нулями
train_sequences = tokenizer.texts_to_sequences(train_data)
test_sequences = tokenizer.texts_to_sequences(test_data)

max_sequence_length = 100
train_data_pad = pad_sequences(train_sequences, maxlen=max_sequence_length)
test_data_pad = pad_sequences(test_sequences, maxlen=max_sequence_length)

# Создание модели
embedding_dim = 50
model = Sequential()
model.add(Embedding(input_dim=max_words, output_dim=embedding_dim, input_length=max_sequence_length))
model.add(LSTM(units=100))
model.add(Dropout(0.2))
model.add(Dense(units=1, activation='sigmoid'))

# Компиляция модели
model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

# Обучение модели с использованием весов классов
class_weights = {0: 1, 1: 1}  # Экспериментируйте с весами классов
model.fit(train_data_pad, train_labels, epochs=50, batch_size=16, validation_split=0.2, class_weight=class_weights)

# Оценка модели на тестовых данных
test_loss, test_accuracy = model.evaluate(test_data_pad, test_labels)
print(f'Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.4f}')

# Сохранение модели
model.save('models/updated_model_mat.keras')
