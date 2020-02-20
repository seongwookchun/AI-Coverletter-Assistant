from time import time
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dense, SimpleRNN, LSTM


def text_preprocessing(filepath):
    with open(filepath, 'r') as f:    # text는 \n 개행문자로 문장이 구분되어 있는 텍스트 파일이다.
        text = f.read()
        print('text file is loaded from')
        print(filepath)
        
    t = Tokenizer()
    t.fit_on_texts([text])
    vocab_size = len(t.word_index) + 1
    # 케라스 토크나이저의 정수 인코딩은 인덱스가 1부터 시작하지만,
    # 케라스 원-핫 인코딩에서 배열의 인덱스가 0부터 시작하기 때문에
    # 배열의 크기를 실제 단어 집합의 크기보다 +1로 생성해야하므로 미리 +1 선언 
    print('Keras tokenizer is created.')
    print('단어 집합의 크기 : %d' % vocab_size)
    
    sequences = list()
    time_i = time()
    for line in text.split('\n'): # Wn을 기준으로 문장 단위로 샘플 구성
        encoded = t.texts_to_sequences([line])[0]
        for i in range(1, len(encoded)):
            sequence = encoded[:i+1]
#             print(i)
#             print(sequence)
            sequences.append(np.array(sequence))
    print('Sliding is done.')
    print('Time elapsed:', time() - time_i)
    print('학습에 사용할 문장의 개수: %d' % len(sequences))

    max_len = max([len(seq) for seq in sequences])
    print('max length of sentencees:', max_len)
    sequences = pad_sequences(sequences, maxlen=max_len, padding='pre')
    # sequences

    sequences = np.array(sequences)
    print('shape of sequences:', sequences.shape)
    # >>> (11,)

    sequences = np.array(sequences)
    X = sequences[:,:-1]
    y = sequences[:,-1]
    y = to_categorical(y, num_classes=vocab_size)
    print('x_train, y_train are created.')
    return X, y
# y[:3]
# >>> array([[0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
#       [0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
#       [0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0.]], dtype=float32)


def genModel():
    model = Sequential()
    model.add(Embedding(vocab_size, 2, input_length=max_len-1)) # 레이블을 분리하였으므로 이제 X의 길이는 5
    model.add(SimpleRNN(3))
    model.add(Dense(11 +1, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# model.fit(X, y, epochs=200, verbose=2)

# test
def test_asample(token:str):
    # ex) token : '말이'
    sample = t.texts_to_sequences([token])
    sample = pad_sequences(sample, maxlen=6 -1)
    # sample
    # >>> [[0.00387258 0.05016697 0.00410838 0.21625255 0.0292282  0.00172935
    #   0.0044616  0.22670373 0.00537118 0.22052407 0.00571809 0.23186329]]
    # 1.0

    print(model.predict(sample))
    print(model.predict(sample).sum())

    pred_id = np.argmax(model.predict(sample))
    # print('예측한 단어:', t.sequences_to_texts([[pred_id]]))
    # >>> 예측한 단어: ['곱다']
