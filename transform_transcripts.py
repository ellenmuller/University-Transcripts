import pandas
import os
from typing import Union
from pandas.core.frame import DataFrame
import pandasql

# Define the variables used for the analysis here: 
DIRECTORY: str = "data/"
COLUMNS = ("subject", "grade", "uni")
QUERIES = [
    (
        "What are the top 3 most popular classes spanning all universities?",
        "SELECT subject, COUNT(*) AS num_of_students FROM df GROUP BY subject ORDER BY num_of_students DESC LIMIT 3",
    ),
    (
        "What are the courses offered by no more than 1 university and what is the number of students enrolled in each?",
        "SELECT * FROM (SELECT COUNT(*) as students_enrolled, subject, COUNT(DISTINCT uni) AS num_of_unis FROM df GROUP BY subject) WHERE num_of_unis <= 1",
    ),
    (
        "What is the % passing rate at each university?",
        (
            """
        WITH passes_letters AS (
        SELECT 
        COUNT(*) AS letter, 
        uni 
        FROM df
        WHERE grade IN ('D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+')
        GROUP BY uni
        ),

        passes_numbers AS (
        SELECT 
        COUNT(*) AS number, 
        uni 
        FROM 
        (
        SELECT 
        CASE WHEN grade NOT IN (
        'F-', 'F', 'F+', 'E-', 'E', 'E+', 'D-', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+'
        ) THEN CAST(grade AS INT) ELSE NULL END AS num, 
        uni 
        FROM df
        ) 
        WHERE num IS NOT NULL AND num >= 50 
        GROUP BY uni
        ),

        unis AS (
        SELECT 
        COUNT(*) AS total,
        uni AS uni
        FROM df
        GROUP BY uni
        )
    
        SELECT 
        unis.uni,
        (COALESCE(passes_letters.letter, 0) + COALESCE(passes_numbers.number, 0)) * 100 / unis.total AS percentage
        FROM unis
        LEFT JOIN passes_numbers 
        ON unis.uni = passes_numbers.uni
        LEFT JOIN passes_letters
        ON passes_letters.uni = unis.uni
            """
        ),
    ),
]

class UniversityTranscriptsAnalysis:
    """
    This class represents the analysis of the university transcripts.

    Attributes
    ----------
    directory : str
        the directory containing the university transcript files
    queries : list
        list of tuples containing questions and associated sql queries to execute on the university transcript data
    columns: tuple
        columns necessary to execute the sql queries for the data analysis

    Methods
    -------
    analyse_university_transcripts
        Calls read_input_files and execute_queries
    read_input_files
        Creates empty dataframe and appends non-empty csv or json files to it, calls validate_input_files
    validate_input_files
        Checks if input file is .csv or .json and non-empty
    execute_queries
        Runs sql queries on the dataframe and displays result
    """

    def __init__(self, directory, queries, columns):
        self.directory = directory
        self.queries = queries
        self.columns = columns

    def analyse_university_transcripts(self) -> None:
        df = self.read_input_files()
        self.execute_queries(df)

    def read_input_files(self) -> DataFrame:

        df = pandas.DataFrame(columns=self.columns)

        for filename in os.listdir(self.directory):
            file_validation = self.validate_input_files(filename)
            if file_validation:
                with open(os.path.join(self.directory, filename), "r") as f:
                    if file_validation == ".csv":
                        file = pandas.read_csv(
                            f, delimiter=",", header=0, skipinitialspace=True
                        )
                    if file_validation == ".json":
                        file = pandas.read_json(f, orient="records")
                    # Remove any repeated headers
                    file = file[file.ne(file.columns).any(1)]
                    # Insert uni column with file name as uni
                    file["uni"] = os.path.splitext(filename)[0]
                    df = pandas.concat([df, file], axis=0, ignore_index=True)
  
        return df

    def validate_input_files(self, filename) -> Union[bool, str]:
        if not filename.endswith(".csv") and not filename.endswith(".json"):
            print(f"File {filename} is not in correct .csv/.json format, skipping.")
            return False
        if os.stat(os.path.join(self.directory, filename)).st_size == 0:
            print(f"File {filename} is empty, skipping.")
            return False
        # Return file extension
        return os.path.splitext(filename)[1]

    def execute_queries(self, df) -> None:
        for query in self.queries:
            try:
                result = pandasql.sqldf(query[1])
            except pandasql.PandaSQLException:
                print("Formatting issue with SQL statement, skipping.")
                continue
            # Output results in terminal
            print(f"The result of the query '{query[0]}' is as follows:")
            print(result)
            # Output results as files
            file_string = query[0].replace(" ", "_")
            result.to_csv(f"{file_string}.csv", sep=",")


def run_analysis() -> None:
    analysing = UniversityTranscriptsAnalysis(
        directory=DIRECTORY, queries=QUERIES, columns=COLUMNS
    )
    analysing.analyse_university_transcripts()


if __name__ == "__main__":
    run_analysis()
