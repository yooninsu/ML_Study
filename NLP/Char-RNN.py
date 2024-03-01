import tensorflow as tf
from pandas import read_excel
from sklearn.model_selection import train_test_split
import numpy as np

shakespeare_url = "https://homl.info/shakespeare"  # 단축 URL
filepath = tf.keras.utils.get_file("shakespeare.txt", shakespeare_url)
with open(filepath) as f:
    shakespeare_text = f.read()
# print(shakespeare_text[:200])

# tf.kears.layers.TextVectorization 층을 사용해 텍스트 인코딩
# split="character"로 설정해 문자 수준 인코딩
# standardize = 'lower'를 사용해 텍스트 소문자 전환

text_vec_layer = tf.keras.layers.TextVectorization(
    split="character", standardize="lower"
)
text_vec_layer.adapt([shakespeare_text])
encoded = text_vec_layer([shakespeare_text])[0]  # 2D
# 해당 글자들이 대응되는 숫자로 잘 바뀌었음을 확인

encoded -= 2  # 토큰 0(패딩 토큰)과 1(알려지지 않은 문자)을 사용하지 않으므로 무시한다.
n_tokens = text_vec_layer.vocabulary_size() - 2  # 고유한 문자 개수 = 39
dataset_size = len(encoded)  # 1,115,394개


# 이 시퀀스를 seq2seq RNN을 훈련하는데 사용할 수 있도록 윈도의 데이터셋으로 바꾼다.
# 문자 ID로 구성된 시퀸스를 입력과 타깃 윈도 쌍의 데이터 셋으로 변환하는 함수.
def to_dataset(sequence, length, shuffle=False, seed=None, batch_size=32):
    ds = tf.data.Dataset.from_tensor_slices(sequence)  # 데이터 객체 생성
    ds = ds.window(
        length + 1, shift=1, drop_remainder=True
    )  # 데이터 셋 윈도우로 변경 length의 +1은 타깃을 위한 다음 문자가 필요하기 때문
    ds = ds.flat_map(lambda window_ds: window_ds.batch(length + 1))
    # 각 윈도우를 정확한 길이로 배치 처리합니다. 이는 모든 윈도우가 같은 크기를 갖도록 합니다.6
    if shuffle:
        ds = ds.shuffle(buffer_size=100_000, seed=seed)
        # 필요한 경우 데이터셋을 섞습니다. 이는 모델이 데이터의 순서에 의존하지 않도록 하여 일반화 성능을 향상
    ds = ds.batch(batch_size)  # 지정된 배치 크기로 데이터를 그룹화합
    return ds.map(lambda window: (window[:, :-1], window[:, 1:])).prefetch(1)


# window[:, :-1]은 윈도우의 첫 번째 요소부터 마지막 요소 전까지를 의미 -> 입력
# window[:, 1:]은 윈도우의 두 번째 요소부터 마지막 요소까지를 의미 -> 타깃
# 윈도우에서 입력과 타깃을 분리. 입력은 윈도우의 처음부터 length까지이고, 타깃은 윈도우의 마지막 값
# prefetch(1)은 학습 중에 GPU 또는 다른 계산 장치가 데이터를 기다리지 않도록, 한 번에 하나의 배치를 미리 준비해 둡니다. 이는 학습 속도를 개선할 수 있습니다.

# 훈련, 검증, 테스트 셋 생성
length = 100
tf.random.set_seed(42)
train_set = to_dataset(encoded[:1_000_000], length=length, shuffle=True, seed=42)
valid_set = to_dataset(encoded[1_000_000:1_060_000], length=length)
test_set = to_dataset(encoded[1_060_000:], length=length)

print(train_set, valid_set, test_set)
model = tf.keras.Sequential(
    [
        tf.keras.layers.Embedding(input_dim=n_tokens, output_dim=16),
        # 문자 ID를 인코딩 embedding 층의 입력 차원 수는 고유한 문자 ID 개수 출력 차원 수는 조절
        # Embedding(배치크기, 윈도길이) 2D 텐서 -> Embedding 출력 [배치크기, 윈도 길이, 임베딩 크기] 3D 텐서
        tf.keras.layers.GRU(128, return_sequences=True),
        # Gated Recurrent Unit(GRU) 레이어에가 시퀸스의 각 타임스텝에 대하여 128차원 출력을 진행함을 의미한다.
        tf.keras.layers.Dense(n_tokens, activation="softmax"),
        # n_tokens는 39개의 고유 문자가 있고, 입력된 벡터를 확률 분포로 변환한다.
    ]
)

model.compile(
    loss="sparse_categorical_crossentropy", optimizer="nadam", metrics=["accuracy"]
)
model_ckpt = tf.keras.callbacks.ModelCheckpoint(
    "my_shakespeare_model", monitor="val_accuracy", save_best_only=True
)
history = model.fit(
    train_set, validation_data=valid_set, epochs=10, callbacks=[model_ckpt]
)

shakespeare_model = tf.keras.Sequential(
    [
        text_vec_layer,
        tf.keras.layers.Lambda(lambda X: X - 2),  # <PAD> 와 <UNK> 토큰을 제외
        model,
    ]
)

y_proba = shakespeare_model.predict(["To be or not to b"])[0, -1]
y_pred = tf.argmax(y_proba)
text_vec_layer.get_vocabulary()[y_pred + 2]
