import unittest
import sys
from io import StringIO
import pandas.util.testing as pdt
import pandas
from transform_transcripts import UniversityTranscriptsAnalysis

columns = (
    "course",
    "class",
    "grade",
    "first_name",
    "last_name",
)

columns_after_transform = columns + ("uni",)

data = (
    [
        "physics",
        "quantum_physics",
        65,
        "clara",
        "bradley",
        "university_of_bristol",
    ],
    [
        "physics",
        "super_conductors",
        70,
        "clara",
        "bradley",
        "university_of_bristol",
    ],
    [
        "physics",
        "newtonian_mechanics",
        67,
        "clara",
        "bradley",
        "university_of_bristol",
    ],
    [
        "philosophy",
        "philosophy_of_science",
        70,
        "will",
        "sheaf",
        "lse"
    ],
    [
        "philosophy",
        "philosophy_of_mathematics",
        60,
        "will",
        "sheaf",
        "lse"
    ],
    [
        "philosophy",
        "rationality_and_choice",
        63,
        "will",
        "sheaf",
        "lse"
    ],
)

df = pandas.DataFrame(columns=columns_after_transform, data=data)


class TestTransformTranscripts(unittest.TestCase):
    def test_validating_inputs_with_formatting_issues(self):
        queries = None
        directory = "fixtures/formatting_issues"
        transcripts = UniversityTranscriptsAnalysis(
            directory=directory, queries=queries, columns=columns
        )

        non_csv = transcripts.validate_input_files("non_csv.txt")
        empty_csv = transcripts.validate_input_files("empty_csv.csv")

        self.assertFalse(non_csv)
        self.assertFalse(empty_csv)

    def test_read_input_files(self):
        queries = None
        directory = "fixtures/good_test_data"
        transcripts = UniversityTranscriptsAnalysis(
            directory=directory, queries=queries, columns=columns
        )
        actual_output = transcripts.read_input_files()
        pdt.assert_frame_equal(actual_output, df, check_dtype=False)

    def test_sql_quality_check(self):
        queries = [("This is wrong", "SELECT this is not correct syntax")]
        directory = "fixtures/good_test_data"

        transcripts = UniversityTranscriptsAnalysis(
            directory=directory, queries=queries, columns=columns
        )

        # Capturing the print statements
        captured_output = StringIO()
        sys.stdout = captured_output
        transcripts.execute_queries(df)
        # Reset redirect
        sys.stdout = sys.__stdout__

        self.assertEqual(
            captured_output.getvalue(),
            "Formatting issue with SQL statement, skipping.\n",
        )

    def test_sql_output(self): 
        queries = [
            (
                "What are the different courses?",
                "SELECT DISTINCT course AS course FROM df",
            )
        ]
        directory = "fixtures/good_test_data"
        sql_output = UniversityTranscriptsAnalysis(
            directory=directory, queries=queries, columns=columns
        )

        expected_output = (
            f"The result of the query '{queries[0][0]}' is as follows:\n"
            f"{pandas.DataFrame(columns=(['course']), data=({'course':'physics'}, {'course':'philosophy'}))}\n"
        )

        # Capturing the print statements
        captured_output = StringIO()
        sys.stdout = captured_output
        sql_output.execute_queries(df)
        # Reset redirect
        sys.stdout = sys.__stdout__

        self.assertEqual(
            captured_output.getvalue(),
            expected_output,
        )


if __name__ == "__main__":
    unittest.main()
