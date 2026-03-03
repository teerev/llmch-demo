import inspect

from kmeans_model.kmeans import KMeans


def test_kmeans_init_signature():
    sig = inspect.signature(KMeans.__init__)
    params = list(sig.parameters.values())

    assert [p.name for p in params] == ["self", "n_clusters", "max_iter", "tol"]
    assert params[0].default is inspect._empty
    assert params[1].default is inspect._empty
    assert params[2].default == 100
    assert params[3].default == 1e-4


def test_kmeans_fit_signature():
    sig = inspect.signature(KMeans.fit)
    params = list(sig.parameters.values())

    assert [p.name for p in params] == ["self", "X"]
    assert params[0].default is inspect._empty
    assert params[1].default is inspect._empty


def test_kmeans_predict_signature():
    sig = inspect.signature(KMeans.predict)
    params = list(sig.parameters.values())

    assert [p.name for p in params] == ["self", "X"]
    assert params[0].default is inspect._empty
    assert params[1].default is inspect._empty
