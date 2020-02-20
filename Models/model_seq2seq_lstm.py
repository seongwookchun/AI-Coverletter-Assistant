# 병렬 코퍼스 읽어오기
import pandas as pd
import numpy as np

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

lines= pd.read_csv('/content/drive/My Drive/tabditor/FromZero/modeling/seq2seq/kor.txt', names=['src', 'tar'], sep='\t', index_col=False)
display(lines)
len(lines)

x_train = lines['src'].values
x_train


t_en = Tokenizer()
t_en.fit_on_texts(x_train)
vocab_size_en = len(t_en.word_index) + 1
# 케라스 토크나이저의 정수 인코딩은 인덱스가 1부터 시작하지만,
# 케라스 원-핫 인코딩에서 배열의 인덱스가 0부터 시작하기 때문에
# 배열의 크기를 실제 단어 집합의 크기보다 +1로 생성해야하므로 미리 +1 선언 
print('단어 집합의 크기 : %d' % vocab_size_en)

x_train = t_en.texts_to_sequences(x_train)
max_len_en = max([len(seq) for seq in x_train])
max_len_en

x_train = pad_sequences(x_train, maxlen=max_len_en)
x_train

t_ko = Tokenizer()
t_ko.fit_on_texts(y_train)
vocab_size_ko = len(t_ko.word_index) + 1
# 케라스 토크나이저의 정수 인코딩은 인덱스가 1부터 시작하지만,
# 케라스 원-핫 인코딩에서 배열의 인덱스가 0부터 시작하기 때문에
# 배열의 크기를 실제 단어 집합의 크기보다 +1로 생성해야하므로 미리 +1 선언 
print('단어 집합의 크기 : %d' % vocab_size_ko)

y_train = t_ko.texts_to_sequences(y_train)

max_len_ko = max([len(seq) for seq in y_train])
max_len_ko

y_train = pad_sequences(y_train, maxlen=max_len_ko)
y_train

# modeling
from tensorflow.keras.layers import Input, LSTM, Embedding, Dense
from tensorflow.keras.models import Model

encoder_inputs = Input(shape=(None, vocab_size_en))
encoder_lstm = LSTM(units=256, return_state=True)    # return_state ?
encoder_outputs, state_h, state_c = encoder_lstm(encoder_inputs)
# encoder_outputs도 같이 리턴받기는 했지만 여기서는 필요없으므로 이 값은 버림.
encoder_states = [state_h, state_c]
# LSTM은 바닐라 RNN과는 달리 상태가 두 개. 바로 은닉 상태와 셀 상태.

decoder_inputs = Input(shape=(None, vocab_size_ko))
decoder_lstm = LSTM(units=256, return_sequences=True, return_state=True)    # return_sequences ?
decoder_outputs, _, _= decoder_lstm(decoder_inputs, initial_state=encoder_states)
# 디코더의 첫 상태를 인코더의 은닉 상태, 셀 상태로 합니다.
decoder_softmax_layer = Dense(vocab_size_ko, activation='softmax')
decoder_outputs = decoder_softmax_layer(decoder_outputs)

model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer="rmsprop", loss="categorical_crossentropy")

model.fit(x=[encoder_input, decoder_input], y=decoder_target, batch_size=64, epochs=50, validation_split=0.2)

from tensorflow.keras.utils import to_categorical
encoder_input = to_categorical(x_train, num_classes=vocab_size_en)
decoder_input = to_categorical(y_train, num_classes=vocab_size_ko)
decoder_target = to_categorical(y_train, num_classes=vocab_size_ko)

encoder_input = x_train
decoder_input = y_train
decoder_target = y_train

from keras.models import Sequential
from keras.layers import Embedding

model_embedding_en = Sequential()
e_en = Embedding(vocab_size_en, 10, input_length=max_len_en)
model_embedding_en.add(e_en)

print(max_len_ko, max_len_en)
print(vocab_size_ko, vocab_size_en)
print(y_train.shape)
