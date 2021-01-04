import re
import datetime as dt
import pandas as pd
import plotly
from plotly.graph_objs import Bar, Figure
import click


def line2list(path):
    file = open(path, "rt", encoding="utf-8")

    date_pattern = re.compile(r"^\d{4}/\d{2}/\d{2}")
    time_pattern = re.compile(r"^\d{2}:\d{2}")
    name_pattern = re.compile(r"\t.+\t")

    table = []
    table.append(["date", "time", "name", "message"])

    lines = file.readlines()
    is_multiline = False

    for i, t in enumerate(lines):
        t = t.replace("\r", "")
        t = t.replace("\n", "")

        date_result = date_pattern.search(t)
        time_result = time_pattern.search(t)
        name_result = name_pattern.search(t)

        if is_multiline:
            message += str(t)
            if t != "" and t[-1] == '"':
                message = message[:-1]
                is_multiline = False
                row = [date, time, name, message]
                table.append(row)

        if date_result:
            date = date_result.group()
        if time_result:
            time = time_result.group()
            if name_result:
                name = name_result.group()[1:-1:]
                message = t[name_result.span()[1] :]
            else:
                name = "event"
                message = t[time_result.span()[1] + 1 :]

            if message != "" and message[0] == '"':
                is_multiline = True
                message = message[1:]

            if not is_multiline:
                row = [date, time, name, message]
                table.append(row)
    return table


def line2BarPlot(table, filename="graph.html"):
    df = pd.DataFrame(table[1:], columns=table[0])

    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"] > dt.datetime(2016, 1, 1)]
    print(f"total amount of message:\t{len(df)-1}")
    print(
        f'last message time:\t{df["date"].tail(1).to_string(index=False)} {df["time"].tail(1).to_string(index=False)}'
    )

    df_count = df.groupby("date").count()
    fig = Figure(
        Bar(
            x=df_count.index,
            y=df_count["message"],
        )
    )
    fig.update_layout(autosize=True)

    plotly.offline.plot(fig, filename=filename)


def line2LinePlot(table, filename="graph.html"):
    df = pd.DataFrame(table[1:], columns=table[0])

    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"] > dt.datetime(2016, 1, 1)]
    print(f"total amount of message:\t{len(df)-1}")
    print(
        f'last message time:\t{df["date"].tail(1).to_string(index=False)} {df["time"].tail(1).to_string(index=False)}'
    )

    df_count = df.groupby("date").count()
    plotly.offline.plot(
        [{"x": df_count.index, "y": df_count["message"]}], filename=filename
    )


@click.command()
@click.option("--input", "-i", default="line.txt")
@click.option("--output", "-o", default="index.html")
@click.option("--type", "-t", type=click.Choice(["bar", "line"]), default="bar")
def cmd(input, output, type):
    table = line2list(input)
    if type == "bar":
        line2BarPlot(table, output)
    elif type == "line":
        line2LinePlot(table, output)


if __name__ == "__main__":
    cmd()
