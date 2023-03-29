import pandas as pd
from outliers import smirnov_grubbs as sgt # pip install outlier_utils

CONFIDENCE_LEVEL = 0.05  # Chance for false-positive

df_perf = pd.DataFrame(
    [
        ["2023-03-01", 14.2, "no-regression"],
        ["2023-03-02", 13.8, "no-regression"],
        ["2023-03-03", 19.0, "false-positive"],
        ["2023-03-04", 14.7, "no-regression"],
        ["2023-03-05", 18.1, "regression"],
        ["2023-03-06", 18.7, "no-regression"],
        ["2023-03-07", 18.5, "no-regression"],
        ["2023-03-08", 13.9, "improvement"],
        ["2023-03-09", 14.5, "no-regression"],
        ["2023-03-10", 14.1, "no-regression"],
        ["2023-03-11", 13.9, "no-regression"],
        ["2023-03-12", 13.5, "no-regression"],
        ["2023-03-13", 13.9, "no-regression"],
    ],
    columns=["Date", "Performance", "Verdict"]
)
df_perf.Date = pd.to_datetime(df_perf.Date)

new_improvement = ["2023-03-14", 10.1, ""]
new_regression = ["2023-03-14", 18.4, ""]
new_no_regression = ["2023-03-14", 14.5, ""]


def test_for_outlier(data, alpha):
    """
    Perform two-sided Grubb-Smirnov test for outliers
    :param data: dataframe with historic data. Last row includes the new data point
    :param alpha: confidence level, e.g. alpha=0.05 leaves 5% chance of false-positive
    :return: dataframe with changed Verdict column
    """
    df = data
    if len(df) < 3:
        # Here if there is not enough historic data
        df.loc[df.index[-1], "Verdict"] = "manual-inspection"
    else:
        # Here if we have at least 3 data points
        df.loc[df.index[-1], "Verdict"] = "no-regression"

        print("Improvements")
        improvements = sgt.min_test_indices(df.Performance.values, alpha)
        print(improvements)
        if len(improvements) > 0:
            df.loc[improvements, "Verdict"] = "potential-improvement"
        print("Regressions")
        regressions = sgt.max_test_indices(df.Performance.values, alpha)
        print(regressions)
        if len(regressions) > 0:
            df.loc[regressions, "Verdict"] = "potential-regression"

        return df


def main():
    print("Historic data")
    print(df_perf)

    # Get only trailing data with no regressions + 1 row where the change happened
    df = df_perf.iloc[::-1]
    df = df.loc[df.index.max():df[df.Verdict != "no-regression"].index[0]].iloc[::-1]
    print("Trailing data from the last material change")
    print(df)


    print("\nTrailing data + new data")
    #df.loc[len(df)] = new_improvement
    #df.loc[len(df)] = new_no_regression
    df.loc[len(df)] = new_regression
    df.Date = pd.to_datetime(df.Date)
    df.reset_index(inplace=True, drop=True)
    print(df)

    df = test_for_outlier(df, CONFIDENCE_LEVEL)
    print("\nResults of running test for outliers")
    print(df)


if __name__ == '__main__':
    main()
