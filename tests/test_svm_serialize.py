from svm_proto.svm import LinearSVM


def test_linear_svm_roundtrip_dict():
    model = LinearSVM(learning_rate=0.05, epochs=10, C=2.0)
    model.weights = [1.0, -1.0]
    model.bias = 0.5
    data = model.to_dict()
    restored = LinearSVM.from_dict(data)
    assert restored.learning_rate == 0.05
    assert restored.epochs == 10
    assert restored.C == 2.0
    assert restored.weights == [1.0, -1.0]
    assert restored.bias == 0.5
