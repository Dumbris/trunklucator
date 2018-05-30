import collections, pandas as pd, numpy as np

#from sklearn.linear_model import LogisticRegression
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

# libact classes
from libact.models import LogisticRegression as LibActLogReg
from libact.query_strategies import UncertaintySampling
from libact.base.dataset import Dataset
from libact.query_strategies import UncertaintySampling, RandomSampling
from my_interactive_labeler import MyInteractiveLabeler

cats = ['alt.atheism', 'sci.space']


# Loading the 20newsgroups dataset# Loadi 
train_dataset = fetch_20newsgroups(subset='train', categories=cats)
test_dataset = fetch_20newsgroups(subset='test', categories=cats)


# Preparing features
vectorizer = TfidfVectorizer(min_df=3, max_df=0.5, sublinear_tf=True)

X_train = vectorizer.fit_transform(train_dataset.data)
Y_train = train_dataset.target

X_test = vectorizer.transform(test_dataset.data)
Y_test = test_dataset.target

n_labeled = 5

print(type(X_train))

trn_ds = Dataset(X_train, np.concatenate(
        [Y_train[:n_labeled], [None] * (Y_train.shape[0] - n_labeled)]))

tst_ds = Dataset(X_test, Y_test)


#clf = LogisticRegression()
#clf.fit(X_train, Y_train)
#Y_pred = clf.predict(X_test)
#Y_pred_proba = clf.predict_proba(X_test)
#print('Accuracy', accuracy_score(Y_test, Y_pred))
#print('F1 macro', f1_score(Y_test, Y_pred, average='macro'))

#==Train-test with active learning and human-in-the-loop
# We choose 20 random examples as seed set for active learning.
Y_seed = Y_train.copy().astype('O')
unknown_indexes = np.random.randint(Y_seed.shape[0], size = Y_seed.shape[0] - 20)
Y_seed[unknown_indexes] = None

model = LibActLogReg()
qs = UncertaintySampling(trn_ds, method='lc', model=LibActLogReg())
E_out1 = []

# Give each label its name (labels are from 0 to n_classes-1)
lbr = MyInteractiveLabeler(label_name=[0,1])
quota = 10
for i in range(quota):
    ask_id = qs.make_query()
    lb = lbr.label(train_dataset.data[ask_id])
    print(lb)
    print(type(lb))
    trn_ds.update(ask_id, lb)
    model.train(trn_ds)
    print(model.score(tst_ds))
    E_out1 = np.append(E_out1, 1 - model.score(tst_ds))

print(E_out1)

