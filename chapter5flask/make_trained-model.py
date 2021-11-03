from sklearn.linear_model._logistic import LogisticRegression
from sklearn import datasets
import pickle

# 学習済みモデルのセーブ
clf = LogisticRegression(random_state=0, solver='liblinear', multi_class='auto')
X, y = datasets.load_digits(return_X_y=True)
clf.fit(X, y)
with open('trained-model.pickle', 'wb') as f:  # wbモードで保存先を開く
   pickle.dump(clf, f)  # 学習済みモデルを保存先に書き出す
