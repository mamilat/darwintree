__author__ = 'aclapes'

import numpy as np
from sklearn.svm import LinearSVR

def rootSIFT(X):
    '''
    :param X: rootSIFT operation applied to elements of X (element-wise).
    Check Fisher Vectors literature.
    :return:
    '''
    return np.multiply(np.sign(X), np.sqrt(np.abs(X)))

def normalizeL1(X):
    """
    Normalize the data using L1-norm.
    :param X: each row of X is an instance
    :return: the normalized data
    """
    X = np.matrix(X)
    return X / np.sqrt(np.sum(np.abs(X), axis=1))

def normalizeL2(X):
    """
    Normalize the data using L2-norm.
    :param X: each row of X is an instance
    :return: the normalized data
    """
    X = np.matrix(X)
    return X / np.sqrt(np.sum(np.multiply(X,X), axis=1))

def linearSVR(X, c_param, norm=2):
    if norm == 1:
        XX = normalizeL1(X)
    else:
        XX = normalizeL2(X)

    T = X.shape[0] # temporal length
    clf = LinearSVR(C=c_param, dual=False, loss='squared_epsilon_insensitive', \
                    epsilon=0.1, tol=0.001, verbose=False)  # epsilon is "-p" in C's liblinear and tol is "-e"
    clf.fit(XX, np.linspace(1,T,T))

    return clf.coef_

def darwin(X, c_svm_param=1):
    w_fw, w_rv = _darwin(X, c_svm_param=c_svm_param)

    return np.concatenate([w_fw, w_rv])

def _darwin(X, c_svm_param=1):
    '''
    Computes the videodarwin representation of a multi-variate temporal series.
    :param X: a N-by-T matrix, with N the number of features and T the time instants.
    :param c_svm_param: the C regularization parameter of the linear SVM.
    :return: the videodarwin representation
    '''
    T = X.shape[0] # temporal length
    one_to_T = np.linspace(1,T,T)
    one_to_T = one_to_T[:,np.newaxis]

    V = np.cumsum(X,axis=0) / one_to_T
    w_fw = linearSVR(rootSIFT(V), c_svm_param, 2) # videodarwin

    V = np.cumsum(np.flipud(X),axis=0) / one_to_T # reverse videodarwin
    w_rv = linearSVR(rootSIFT(V), c_svm_param, 2)

    return w_fw, w_rv