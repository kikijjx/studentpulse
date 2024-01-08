from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, load_model
from keras.layers import Embedding, LSTM, Dense
import pandas as pd
import pickle
df = pd.read_csv('datasets/distortion_train.tsv', sep='\t')

label_encoder = LabelEncoder()
df['target'] = label_encoder.fit_transform(df['target'])
train_data, test_data, train_labels, test_labels = train_test_split(
    df['doc'], df['target'], test_size=0.2, random_state=42
)

max_words = 10000
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_data)

with open(f'tokenizers/tokenizer_mat.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

train_sequences = tokenizer.texts_to_sequences(train_data)
test_sequences = tokenizer.texts_to_sequences(test_data)

max_sequence_length = 100
train_data_pad = pad_sequences(train_sequences, maxlen=max_sequence_length)
test_data_pad = pad_sequences(test_sequences, maxlen=max_sequence_length)

embedding_dim = 50#200
model = Sequential()
model.add(Embedding(input_dim=max_words, output_dim=embedding_dim,
                    input_length=max_sequence_length))
model.add(LSTM(units=100))
model.add(Dense(units=1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(train_data_pad, train_labels, epochs=5, batch_size=32, validation_split=0.2)
model.save('models/model_mat.keras')