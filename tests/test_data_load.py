from svm_proto.data import load_csv


def test_load_csv_parses_rows(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("1,2,1\n-1,-2,-1\n")
    X, y = load_csv(str(p))
    assert X == [[1.0, 2.0], [-1.0, -2.0]]
    assert y == [1, -1]
