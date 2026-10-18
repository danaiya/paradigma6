import statistics
import unittest


def validate_score(score):
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError("Балл должен быть числом")
    if not 0 <= score <= 100:
        raise ValueError("Балл должен быть от 0 до 100")
    return float(score)


def validate_scores(scores):
    return [validate_score(score) for score in scores]


def calculate_average(scores):
    if not scores:
        return None
    return sum(scores) / len(scores)


def calculate_median(scores):
    if not scores:
        return None
    sorted_scores = sorted(scores)
    return float(statistics.median(sorted_scores))


def admission_status(scores, threshold=50):
    avg = calculate_average(scores)
    if avg is None:
        return "нет данных"
    return "допущен" if avg >= threshold else "не допущен"


def recursive_max(values):
    if not values:
        raise ValueError("Последовательность пуста")
    if len(values) == 1:
        return values[0]
    tail_max = recursive_max(values[1:])
    return values[0] if values[0] > tail_max else tail_max


def build_report(name, scores):
    checked = validate_scores(scores)
    return {
        "name": name.strip(),
        "scores": tuple(checked),
        "average": calculate_average(checked),
        "median": calculate_median(checked),
        "status": admission_status(checked),
        "maximum": recursive_max(checked) if checked else None,
    }


class FunctionalCoreTests(unittest.TestCase):

    def test_build_report_does_not_change_source(self):
        source = [80, 75, 90]
        snapshot = source.copy()
        report = build_report("Данайя", source)
        self.assertEqual(source, snapshot)
        self.assertEqual(report["status"], "допущен")

    def test_recursive_max_rejects_empty_sequence(self):
        with self.assertRaisesRegex(ValueError, "пуста"):
            recursive_max([])

    def test_same_arguments_give_same_result(self):
        self.assertEqual(
            build_report("Данайя", [60, 70]), build_report("Данайя", [60, 70])
        )

    def test_validate_score_rejects_booleans(self):
        with self.assertRaises(TypeError):
            validate_score(True)

    def test_validate_score_rejects_out_of_bounds(self):
        with self.assertRaises(ValueError):
            validate_score(105)

    def test_calculate_average_empty(self):
        self.assertIsNone(calculate_average([]))

    def test_calculate_median_correctness(self):
        self.assertEqual(calculate_median([10, 20, 30]), 20.0)

    def test_recursive_max_correctness(self):
        self.assertEqual(recursive_max([12, 45, 2, 89, 33]), 89.0)


if __name__ == "__main__":
    unittest.main()