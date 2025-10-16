from backend.utils.shortid import generate_short_id


def test_short_id_length_and_charset():
    sid = generate_short_id()
    assert len(sid) == 7
    assert sid.isalnum()


def test_short_id_randomness():
    values = {generate_short_id() for _ in range(100)}
    assert len(values) > 90
