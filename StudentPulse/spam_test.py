import pickle
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

def get_spam(text='good'):

    with open('tokenizers/tokenizer_spam.pickle', 'rb') as handle:
        tokenizer_spam = pickle.load(handle)

    new_text = text

    # Токенизация текста
    new_text_seq_spam = tokenizer_spam.texts_to_sequences([new_text])
    max_sequence_length = 100
    new_text_pad_spam = pad_sequences(new_text_seq_spam, maxlen=max_sequence_length)

    # Загрузка модели
    model_spam = load_model('models/model_spam_updated.keras')

    # Предсказание
    prediction_spam = model_spam.predict(new_text_pad_spam)[0][0]

    return prediction_spam
