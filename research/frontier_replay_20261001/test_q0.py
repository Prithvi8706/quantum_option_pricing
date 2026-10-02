from research.frontier_replay_20261001.q0_replay import get_path, walk


def test_get_path_resolves_walk_paths():
    archived = {"a": [{"b": 1.0}, {"b": 2.0}], "seconds": 3.0}
    replayed = {"a": [{"b": 1.0}, {"b": 2.5}], "seconds": 4.0}
    out = {"exact": {"compared": 0, "differ": []}, "timing": {"compared": 0, "differ": []}}
    walk(archived, replayed, "", out)
    assert out["exact"]["differ"] == ["/a[1]/b"]
    assert out["timing"]["differ"] == ["/seconds"]
    assert get_path(archived, "/a[1]/b") == 2.0
    assert get_path(replayed, "/a[1]/b") == 2.5
