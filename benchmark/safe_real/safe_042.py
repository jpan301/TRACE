# source: SentrySafe / .github/workflows/scripts/test_calculate_backend_test_shards.py
# function: test_class_with_parametrize_on_method

class TestCountTestsInFile:
    def test_class_with_parametrize_on_method(self, tmp_path):
        p = _write(
            tmp_path,
            """\
            import pytest

            class TestMath:
                @pytest.mark.parametrize("n", [1, 2, 3])
                def test_square(self, n):
                    pass

                def test_plain(self):
                    pass
            """,
        )
        assert count_tests_in_file(p) == 4