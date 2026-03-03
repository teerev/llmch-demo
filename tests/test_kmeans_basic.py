from kmeans_model.kmeans import KMeans


def test_kmeans_basic_clustering_and_prediction():
    X = [[0.0, 0.0], [9.0, 9.0], [0.1, 0.0], [9.1, 9.0]]
    km = KMeans(n_clusters=2, max_iter=100, tol=1e-6)
    km.fit(X)

    labels = km.predict(X)

    assert labels[0] == labels[2]
    assert labels[1] == labels[3]
    assert labels[0] != labels[1]

    near_a = [[0.05, 0.02], [0.2, -0.1]]
    near_b = [[9.05, 9.02], [8.9, 9.2]]

    pred_a = km.predict(near_a)
    pred_b = km.predict(near_b)

    assert all(l == labels[0] for l in pred_a)
    assert all(l == labels[1] for l in pred_b)
