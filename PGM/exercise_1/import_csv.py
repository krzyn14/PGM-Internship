from pathlib import Path
import sqlite3

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
CSV_PATH = PROJECT_DIR / "data" / "Polonia Bytom_Pogo  Grodzisk Mazowiecki_4068759.csv"
DATABASE_PATH = PROJECT_DIR / "data" / "match_analysis.sqlite3"

TABLE_NAME = "events_raw"


def import_csv_to_sqlite():

    events = pd.read_csv(
        CSV_PATH,
        encoding="utf-8-sig",
        low_memory=False
    )
    
    with sqlite3.connect(DATABASE_PATH) as connection:
        events.to_sql(
            name=TABLE_NAME,
            con=connection,
            if_exists="replace",
            index=False,
        )

        row_count = connection.execute(
            f"SELECT COUNT(*) FROM {TABLE_NAME}"
        ).fetchone()[0]

        unique_event_count = connection.execute(
            f"""
            SELECT COUNT(DISTINCT id)
            FROM {TABLE_NAME}
            """
        ).fetchone()[0]

    print("Import completed")
    print(f"DB: {DATABASE_PATH}")
    print(f"Table {TABLE_NAME}")
    print(f"Rows count: {row_count}")
    print(f"Unique Events count: {unique_event_count}")


if __name__ == "__main__":
    import_csv_to_sqlite()