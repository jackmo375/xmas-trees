#!/usr/bin/env python3

from src import metric as mt
import pandas as pd

def main():

    row_id_column_name = 'id'

    submission = pd.read_csv("./results/full_solution.csv")
    print(submission.head())

    solution = submission[['id']].copy()

    final_score = mt.score(solution, submission, row_id_column_name)

    print(final_score)


if __name__ == "__main__":
    main()