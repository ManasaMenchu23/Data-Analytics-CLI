import pandas as pd
import typer
from rich import print

__version__ = "0.1.0"

app = typer.Typer(help="Data Analysis CLI Tool")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"data-analytics-cli {__version__}")
        raise typer.Exit()


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df

@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """Data Analytics CLI root command."""
    pass

@app.command()

def info(file: str):
    """Show dataset shape and column names."""

    df = load_csv(file)
    print(f"[bold green]Rows:[/bold green] {df.shape[0]}")
    print(f"[bold green]Colums:[/bold green] {df.shape[1]}")
    print(f"[bold]Column Names:[/bold] {list(df.columns)}")


@app.command()
def summary(file: str):
    """Show dataset summary statistics."""
    df = load_csv(file)
    print(df.describe(include = "all"))

@app.command()
def filter_rows(
    file: str,
    column: str,
    value: str,
    out: str | None = typer.Option(None, "--out", help="Write result to this CSV path."),
):
    """Filter rows where column is equal to value."""
    df = load_csv(file)
    filtered = df[df[column].astype(str).str.strip() == value]

    if out:
        filtered.to_csv(out, index=False)
        print(f"[bold green]Wrote[/bold green] {len(filtered)} rows to {out}")
    else:
        print(filtered)
@app.command()
def sort(
    file: str,
    column: str,
    desc: bool = typer.Option(False, "--desc", help="Sort descending (largest first)."),
    out: str | None = typer.Option(None, "--out", help = "write result to this CSV path.")
):
    """Sort dataset by a column."""
    df = load_csv(file)
    sorted_df = df.sort_values(by=column, ascending=not desc)

    if out:
        sorted_df.to_csv(out, index=False)
        print(f"[bold green]wrote[/bold green] {len(sorted_df)} rows to {out}")

    else:    
        print(sorted_df)

@app.command()
def group_mean(file: str, group_col: str, value_col: str, out: str | None = typer.Option(None, "--out", help="write result to this CSV path.")):
    """Calculate the mean of a column grouped by another column."""
    df = load_csv(file)
    result = df.groupby(group_col)[value_col].mean()

    if out:
        result.reset_index().to_csv(out, index=False)
        print(f"[bold green]Wrote[/bold green] {len(result)} rows to {out}")
    else:
        print(result)


@app.command()
def nulls(file: str):
    """Count missing values per column."""
    df = load_csv(file)
    print(df.isnull().sum())

@app.command()
def head(
    file: str,
    n: int = typer.Option(5, "--n","-n", help = "How many rows to display.")
):
    """Display the first n rows of the dataset."""
    df = load_csv(file)
    print(df.head(n))


@app.command()  
def tail(
    file: str,
    n: int = typer.Option(5, "--n", "-n", help = "How many rows to display.")
):
    """Display the last n rows of the dataset."""
    df = load_csv(file)
    print(df.tail(n))

@app.command()
def value_counts(
    file:str,
    column: str,
    out: str | None = typer.Option(None, "--out", help="write result to this CSV path.")):

    """Display the value counts of a column."""
    df = load_csv(file)
    counts = df[column].astype(str).str.strip().value_counts()

    if out:
        counts.reset_index().to_csv(out, index = False)
        print(f"[bold green]wrote[/bold green] {len(counts)} rows to {out}")

    else:
        print(counts)    


@app.command(name = "dtypes")
def column_dtypes(file: str):
    """Show pandas dtype for each column."""
    df = load_csv(file)
    print(df.dtypes)  

@app.command()
def correlate(file:str, col_a: str, col_b: str):
    """Show correlation between two columns."""
    df = load_csv(file)
    a = pd.to_numeric(df[col_a],  errors="coerce")
    b = pd.to_numeric(df[col_b], errors="coerce")
    print(f"Correlation between {col_a} and {col_b}: {a.corr(b)}")

@app.command()
def drop_duplicates(
    file: str,
    out: str | None = typer.Option(None, "--out", help = "write all the unique rows to this CSV path.")
):
    """Drop duplicate rows from the dataset."""
    df = load_csv(file)
    deduped = df.drop_duplicates()
    if out:
        deduped.to_csv(out, index = False)
        removed = len(df) - len(deduped)
        print(f"[bold green]wrote[/bold green] {len(deduped)} rows to {out}")
        print(f"[bold green]remove[/bold green] {removed} duplicate rows")
    else:
        print(deduped)

@app.command()
def keep_cols(
    file: str,
    cols: list[str] = typer.Argument(..., help="Columns to keep, comma separated."),
    out: str | None = typer.Option(None, "--out", help = "write result to this CSV path.")
):
    """Keep only the specified columns."""
    df = load_csv(file)
    missing = [col for col in cols if col not in df.columns]
    if missing:
        raise typer.BadParameter(f"unknown columns: {missing}")
    selected = df[cols]
    if out:
        selected.to_csv(out, index = False)
        print(f"[bold green]wrote[/bold green] {len(selected)} rows, {len(cols)} columns to {out}")
    else:
        print(selected)

@app.command()
def drop_cols(
    file: str,
    cols: list[str] = typer.Argument(..., help = "Columns to drop, comma separated."),
    out: str | None = typer.Option(None, "--out", help = "write result to this CSV path.")
):
    """Drop the specified columns."""
    df = load_csv(file)
    missing = [col for col in cols if col not in df.columns]
    if missing:
        raise typer.BadParameter(f"unknown columns: {missing}")
    dropped = df.drop(columns = cols)
    if out:
        dropped.to_csv(out, index = False)
        print(f"[bold green]wrote[/bold green] {len(dropped)} rows, {len(df.columns) - len(cols)} columns to {out}")
    else:
        print(dropped)
      



def run() -> None:
    """Console entry point (see pyproject.toml [project.scripts])."""
    app()


if __name__ == "__main__":
    run()


