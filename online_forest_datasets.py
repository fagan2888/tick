
import os
import pandas as pd
import numpy as np
from time import time
import zipfile

from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from tick.inference import OnlineForestClassifier


import matplotlib.pyplot as plt


path = '/Users/stephane.gaiffas/Dropbox/jaouad/online-forests/datasets/'


def read_abalone(path):
    archive = zipfile.ZipFile(os.path.join(path, 'abalone.csv.zip'), 'r')
    with archive.open('abalone.csv') as f:
        data = pd.read_csv(f, header=None)
    continuous = list(range(1, 8))
    discrete = [0]
    y = data.pop(8)
    y -= 1
    X_continuous = MinMaxScaler().fit_transform(data[continuous])
    data_discrete = pd.get_dummies(data[discrete], prefix_sep='#')
    X_discrete = data_discrete.as_matrix()
    y = y.as_matrix()
    X = np.hstack((X_continuous, X_discrete))
    return X, y, 'abalone'


def read_adult(path):
    archive = zipfile.ZipFile(os.path.join(path, 'adult.csv.zip'), 'r')
    with archive.open('adult.csv') as f:
        data = pd.read_csv(f, header=None)
    y = data.pop(13)
    discrete = [1, 3, 4, 5, 6, 7, 8, 12]
    continuous = list(set(range(13)) - set(discrete))
    X_continuous = MinMaxScaler().fit_transform(data[continuous])
    data_discrete = pd.get_dummies(data[discrete], prefix_sep='#')
    X_discrete = data_discrete.as_matrix()
    y = pd.get_dummies(y).as_matrix()[:, 1]
    X = np.hstack((X_continuous, X_discrete))
    return X, y, 'adult'


def read_bank(path):
    archive = zipfile.ZipFile(os.path.join(path, 'bank.csv.zip'), 'r')
    with archive.open('bank.csv') as f:
        data = pd.read_csv(f)
    y = data.pop('y')
    discrete = ['job', 'marital', 'education', 'default', 'housing',
           'loan', 'contact', 'day', 'month', 'campaign', 'poutcome']
    continuous = ['age', 'balance', 'duration', 'pdays', 'previous']
    X_continuous = MinMaxScaler().fit_transform(data[continuous])
    data_discrete = pd.get_dummies(data[discrete], prefix_sep='#')
    X_discrete = data_discrete.as_matrix()
    y = pd.get_dummies(y).as_matrix()[:, 1]
    X = np.hstack((X_continuous, X_discrete))
    return X, y, 'bank'


def read_car(path):
    archive = zipfile.ZipFile(os.path.join(path, 'car.csv.zip'), 'r')
    with archive.open('car.csv') as f:
        data = pd.read_csv(f, header=None)
    y = data.pop(6)
    y = np.argmax(pd.get_dummies(y).as_matrix(), axis=1)
    X = pd.get_dummies(data, prefix_sep='#').as_matrix()
    return X, y, 'car'


def read_cardio(path):
    archive = zipfile.ZipFile(os.path.join(path, 'cardiotocography.csv.zip'),
                              'r')
    with archive.open('cardiotocography.csv', ) as f:
        data = pd.read_csv(f, sep=';', decimal=',')

    data.drop(['FileName', 'Date', 'SegFile',
               'A', 'B', 'C', 'D', 'E', 'AD', 'DE',
               'LD', 'FS', 'SUSP'], axis=1, inplace=True)
    # A 10-class label
    y_class = data.pop('CLASS').as_matrix()
    y_class -= 1
    # A 3-class label
    y_nsp = data.pop('NSP').as_matrix()
    y_nsp -= 1
    continuous = [
        'b', 'e', 'LBE', 'LB', 'AC', 'FM', 'UC',
        'ASTV', 'MSTV', 'ALTV', 'MLTV',
        'DL', 'DS', 'DP',
        'Width', 'Min', 'Max', 'Nmax', 'Nzeros', 'Mode',
        'Mean', 'Median', 'Variance'
    ]

    discrete = [
        'Tendency'
    ]
    X_continuous = MinMaxScaler().fit_transform(data[continuous])
    data_discrete = pd.get_dummies(data[discrete], prefix_sep='#')
    X_discrete = data_discrete.as_matrix()
    X = np.hstack((X_continuous, X_discrete))
    return X, y_nsp, 'cardio'


def read_churn(path):
    archive = zipfile.ZipFile(os.path.join(path, 'churn.csv.zip'), 'r')
    with archive.open('churn.csv') as f:
        data = pd.read_csv(f)
    y = data.pop('Churn?')
    discrete = [
        'State', 'Area Code', "Int'l Plan", 'VMail Plan', ]

    continuous = [
        'Account Length', 'Day Mins', 'Day Calls', 'Eve Calls', 'Day Charge',
        'Eve Mins', 'Eve Charge', 'Night Mins', 'Night Calls',
        'Night Charge', 'Intl Mins', 'Intl Calls', 'Intl Charge',
        'CustServ Calls', 'VMail Message'
    ]
    X_continuous = MinMaxScaler().fit_transform(data[continuous])
    data_discrete = pd.get_dummies(data[discrete], prefix_sep='#')
    X_discrete = data_discrete.as_matrix()
    y = pd.get_dummies(y).as_matrix()[:, 1]
    X = np.hstack((X_continuous, X_discrete))
    return X, y, 'churn'


def read_default_cb(path):
    archive = zipfile.ZipFile(os.path.join(path, 'default_cb.csv.zip'), 'r')
    with archive.open('default_cb.csv') as f:
        data = pd.read_csv(f)
    continuous = [
        'AGE', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'LIMIT_BAL',
        'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1',
        'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6'
    ]
    discrete = [
        'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
        'SEX', 'EDUCATION', 'MARRIAGE'
    ]
    _ = data.pop('ID')
    y = data.pop('default payment next month')
    X_continuous = MinMaxScaler().fit_transform(data[continuous])
    data_discrete = pd.get_dummies(data[discrete], prefix_sep='#')
    X_discrete = data_discrete.as_matrix()
    y = pd.get_dummies(y).as_matrix()[:, 1]
    X = np.hstack((X_continuous, X_discrete))
    return X, y, 'default_cb'

readers = [
    # read_abalone,
    # read_adult
    # read_bank
    # read_car,
    read_cardio,
    read_churn,
    read_default_cb
]

n_trees = 10

names = [
    "OF (agg, step=1.)",
    "OF(agg, step=100.)",
    "OF(no agg.)",
    "KNN (k=5)",
    "LR",
    "ET",
    "BRF"
]


data_description = pd.DataFrame(
    columns=['name', '#samples', '#features', '#classes']
)

performances = pd.DataFrame(
    columns=['dataset'] + names
)

timings = pd.DataFrame(
    columns=['dataset'] + names
)


for reader in readers:
    # Read the data
    X, y, dataset_name = reader(path)
    X_train, X_test, y_train, y_test \
        = train_test_split(X, y, test_size=.3, random_state=42)

    n_samples, n_features = X.shape
    n_classes = int(y.max() + 1)

    data_description = data_description.append(
        pd.DataFrame([[dataset_name, n_samples, n_features, n_classes]],
                     columns=data_description.columns)
    )

    classifiers = [
        OnlineForestClassifier(n_classes=n_classes, n_trees=n_trees, seed=123, step=1.,
                               use_aggregation=True),
        OnlineForestClassifier(n_classes=n_classes, n_trees=n_trees, seed=123,
                               step=100.,
                               use_aggregation=True),
        OnlineForestClassifier(n_classes=n_classes, n_trees=n_trees, seed=123, step=1.,
                               use_aggregation=False),
        KNeighborsClassifier(n_neighbors=5),
        LogisticRegression(class_weight='balanced'),
        ExtraTreesClassifier(n_estimators=n_trees),
        RandomForestClassifier(n_estimators=n_trees)
    ]

    performance = [dataset_name]
    timing = [dataset_name]

    for clf, name in zip(classifiers, names):
        if hasattr(clf, 'clear'):
            clf.clear()
        t1 = time()
        clf.fit(X_train, y_train)
        t2 = time()
        score = clf.score(X_test, y_test)
        t = t2 - t1
        timing.append(t)
        performance.append(score)
        print('Accuracy of', name, ': ',
              '%.2f' % score,
              "in %.2f (s)" % t)

    performances = performances.append(
        pd.DataFrame([performance], columns=performances.columns)
    )
    timings = timings.append(
        pd.DataFrame([timing], columns=timings.columns)
    )

print(data_description)

print(performances)

print(timings)
