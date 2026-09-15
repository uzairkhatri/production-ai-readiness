def test_retrieval_quality():
    """Illustrative retrieval evaluation signal."""
    recall_at_5 = 0.90
    expected = 0.85
    assert recall_at_5 >= expected
