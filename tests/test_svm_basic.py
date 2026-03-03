from svm_proto.svm import LinearSVM


def test_linear_svm_fits_simple_data():
    X = [[2.0, 2.0], [2.0, 0.0], [0.0, 0.0], [0.0, 2.0]]
    y = [1, 1, -1, -1]
    model = LinearSVM(learning_rate=0.1, epochs=1000, C=1.0)
    model.fit(X, y)
    preds = model.predict(X)
    assert preds == y
    assert len(model.weights) == 2
