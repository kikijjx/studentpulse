import pickle
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

def get_mat(text='good'):

    with open('tokenizers/tokenizer_mat.pickle', 'rb') as handle:
        tokenizer_mat = pickle.load(handle)

    new_text = text

    new_text_seq_mat = tokenizer_mat.texts_to_sequences(new_text)
    max_sequence_length = 100
    new_text_pad_mat = pad_sequences(new_text_seq_mat, maxlen=max_sequence_length)
    model_mat = load_model('models/model_mat.keras')
    prediction_mat = model_mat.predict(new_text_pad_mat)[0][0]

    return prediction_mat

