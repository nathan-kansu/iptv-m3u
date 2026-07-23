
import duckdb
from pandas import DataFrame
from backend.app.config import countries_url
from typing import TypedDict

class Countries(TypedDict):
    name: str
    code: str
    languages: list[str]
    flag: str

def fetch_countries() -> DataFrame:
    return duckdb.sql(
        f"""
        SELECT name, code, languages, flag
        FROM '{countries_url}' AS countries
        ORDER BY countries.name ASC
        """
    ).df()
