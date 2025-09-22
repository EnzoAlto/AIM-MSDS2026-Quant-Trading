import pandas as pd
import plotly.graph_objects as go


def main():
    df = pd.read_csv("train.csv")
    print(df.head())

    value_cols = df.columns[df.columns.get_loc("A"): df.columns.get_loc("Y2") + 1]

    fig = go.Figure()
    for col in value_cols:
        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df[col],
                mode="lines",
                name=col,
            )
        )

    fig.update_layout(
        title="Train Columns A to Y2 over Time",
        xaxis_title="Time",
        yaxis_title="Value",
    )

    fig.show()


if __name__ == "__main__":
    main()
