#!/usr/bin/env python3

from src import metric as mt
import pandas as pd
import argparse

def main():

    parser = argparse.ArgumentParser(
        description="checking solution with Kaggle metric"
    )

    parser.add_argument(
        "--file",
        type=str,
        default="./results/full_solution.csv",
        help="solution file to check"
    )

    args = parser.parse_args()

    print("checking file:", args.file)

    row_id_column_name = 'id'

    submission = pd.read_csv(args.file)

    solution = submission[['id']].copy()

    final_score = mt.score(solution, submission, row_id_column_name)

    print(final_score)


if __name__ == "__main__":
    main()