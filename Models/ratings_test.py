import pickle
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model


def get_ratings(text='good'):

    with open('tokenizers/tokenizer_понимание материала.pickle', 'rb') as handle:
        tokenizer_ponimanie = pickle.load(handle)

    with open('tokenizers/tokenizer_организация занятия.pickle', 'rb') as handle:
        tokenizer_organizatsiya = pickle.load(handle)

    with open('tokenizers/tokenizer_полезность материала.pickle', 'rb') as handle:
        tokenizer_poleznost = pickle.load(handle)

    with open('tokenizers/tokenizer_интересность материала.pickle', 'rb') as handle:
        tokenizer_interesnost = pickle.load(handle)

    new_text = text

    new_text_seq_ponimanie = tokenizer_ponimanie.texts_to_sequences(new_text)
    new_text_seq_organizatsiya = tokenizer_organizatsiya.texts_to_sequences(new_text)
    new_text_seq_poleznost = tokenizer_poleznost.texts_to_sequences(new_text)
    new_text_seq_interesnost = tokenizer_interesnost.texts_to_sequences(new_text)

    max_sequence_length = 100

    new_text_pad_ponimanie = pad_sequences(new_text_seq_ponimanie, maxlen=max_sequence_length)
    new_text_pad_organizatsiya = pad_sequences(new_text_seq_organizatsiya, maxlen=max_sequence_length)
    new_text_pad_poleznost = pad_sequences(new_text_seq_poleznost, maxlen=max_sequence_length)
    new_text_pad_interesnost = pad_sequences(new_text_seq_interesnost, maxlen=max_sequence_length)

    model_ponimanie = load_model('models/model_понимание материала.keras')
    model_organizatsiya = load_model('models/model_организация занятия.keras')
    model_poleznost = load_model('models/model_полезность материала.keras')
    model_interesnost = load_model('models/model_интересность материала.keras')

    prediction_ponimanie = model_ponimanie.predict(new_text_pad_ponimanie)[0][0]
    prediction_organizatsiya = model_organizatsiya.predict(new_text_pad_organizatsiya)[0][0]
    prediction_poleznost = model_poleznost.predict(new_text_pad_poleznost)[0][0]
    prediction_interesnost = model_interesnost.predict(new_text_pad_interesnost)[0][0]

    return prediction_ponimanie, prediction_organizatsiya, prediction_poleznost, prediction_interesnost

