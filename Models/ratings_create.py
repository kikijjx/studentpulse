import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
import pickle
from tqdm import tqdm

file_path = 'datasets/Reviews.csv'
df = pd.read_csv(file_path, delimiter=',')

df['текст'] = df['текст'].astype(str).fillna('')

X_columns = ['текст', 'понимание материала', 'организация занятия', 'полезность материала', 'интересность материала']
y_columns = ['понимание материала', 'организация занятия', 'полезность материала', 'интересность материала']

X_train, X_test, y_train, y_test = train_test_split(df[X_columns[0]], df[y_columns], test_size=0.2, random_state=42)

max_words = 100000
max_sequence_length = 100
embedding_dim = 50

for aspect in y_columns:
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(X_train)

    with open(f'tokenizers/tokenizer_{aspect}.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    X_train_seq = tokenizer.texts_to_sequences(X_train)
    X_test_seq = tokenizer.texts_to_sequences(X_test)

    X_train_pad = pad_sequences(X_train_seq, maxlen=max_sequence_length)
    X_test_pad = pad_sequences(X_test_seq, maxlen=max_sequence_length)

    model = Sequential()
    model.add(Embedding(input_dim=max_words, output_dim=embedding_dim, input_length=max_sequence_length))
    model.add(LSTM(units=10))
    model.add(Dense(1, activation='linear'))

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error'])

    model.fit(X_train_pad, y_train[aspect], epochs=12, batch_size=64, validation_split=0.2)

    model.save(f'models/model_{aspect}.keras')
