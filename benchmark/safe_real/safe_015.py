# source: SentrySafe / .github/workflows/scripts/test_calculate_backend_test_shards.py
# function: test_full_suite_ignores_excluded_dirs

class TestCollectTestCount:
    def test_full_suite_ignores_excluded_dirs(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("SELECTED_TESTS_FILE", raising=False)

        tests = tmp_path / "tests"
        tests.mkdir()
        (tests / "test_ok.py").write_text("def test_a(): pass\n")

        for excluded in ("acceptance", "apidocs", "js", "tools"):
            d = tests / excluded
            d.mkdir()
            (d / "test_skip.py").write_text("def test_no(): pass\n")

        assert collect_test_count() == 1