import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from modAL.models import ActiveLearner
from modAL.uncertainty import uncertainty_sampling
from plot_perf import plot_performance
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
import trunklucator

categories = ['comp.graphics', 'sci.med']

N_QUERIES = 300
META = {"buttons":[('comp.graphics (A)', 0, 65), ('sci.med (X)', 1, 88), ('Skip (Enter)', -1, 13)]}

twenty_train = fetch_20newsgroups(subset='train',
    categories=categories, shuffle=True, random_state=42)

# Let's take small part of labeled data to bootstrap classifier
X_big, X_small, _, y_small = train_test_split(twenty_train.data, twenty_train.target, test_size = 0.005)

count_vect = CountVectorizer()
tfidf_transformer = TfidfTransformer()
X_pool = tfidf_transformer.fit_transform(count_vect.fit_transform(X_big)).toarray()


X_text = np.stack([txt.replace("\n", "<br/>") for txt in X_big], axis=0)


text_clf =  SGDClassifier(loss="log", penalty='l2',
                          alpha=1e-3, random_state=42,
                          max_iter=5, tol=None)

#text_clf =  MultinomialNB()

twenty_test = fetch_20newsgroups(subset='test',
            categories=categories, shuffle=True, random_state=42)

X_test = tfidf_transformer.transform(count_vect.transform(twenty_test.data)).toarray()

learner = ActiveLearner(
    estimator=text_clf,
    query_strategy=uncertainty_sampling,
    X_training=tfidf_transformer.transform(count_vect.transform(X_small)).toarray(), y_training=y_small
)

performance_history = [learner.score(X_test, twenty_test.target)]
# Allow our model to query our unlabeled dataset for the most
# informative points according to our query strategy (uncertainty sampling).
with trunklucator.WebUI() as tru:

    tru.update({"html":plot_performance(performance_history)})

    for index in range(N_QUERIES):
        query_index, _ = learner.query(X_pool)

        # Teach our ActiveLearner model the record it has requested.
        X, text = X_pool[query_index].reshape(1, -1), X_text[query_index].reshape(1, -1)
        y = tru.ask({"html":"<pre>{}</pre>".format(text)}, meta=META) # We are waiting for human action here

        if y == -1:
            continue

        print(twenty_train.target_names[y])

        learner.teach(X=X, y=np.array([y]))

        # Remove the queried instance from the unlabeled pool.
        X_pool = np.delete(X_pool, query_index, axis=0)

        if not ((index % 10) == 0):
            continue
        # Calculate and report our model's accuracy.
        model_accuracy = learner.score(X_test, twenty_test.target)
        print('Accuracy after query {n}: {acc:0.4f}'.format(n=index + 1, acc=model_accuracy))

        # Save our model's performance for plotting.
        performance_history.append(model_accuracy)
        #tru.update({"img":self.plot_performance(), "img_pca":self.draw_pca(self.X_train, self.y_train)})
        tru.update({"html":plot_performance(performance_history)})



