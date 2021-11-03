import pandas
import pickle
from sklearn.linear_model import LinearRegression

# データの読み込み
df = pandas.read_csv(
    './ch6-8.csv',
    encoding='Shift_JIS',
)
df_stations = pandas.read_csv(
    './amedas_stations.csv',
    encoding='Shift_JIS',
    index_col=0,
)
df = df.join(
    df_stations,
    on='station'
)
# 学習済みモデルのセーブ
df7 = df[df['date'] == '2018/9/1']
reg = LinearRegression()
X = df7[['latitude']]
y = df7['temp']
reg.fit(X, y)
with open('./trained-reg-model.pickle', 'wb') as f:
    pickle.dump(reg, f)
