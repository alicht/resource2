import os
import pandas as pd
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()

def parse_timestamps(timestamp):
    try:
        return pd.to_datetime(timestamp, format="%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return pd.to_datetime(timestamp, format="%Y-%m-%d %H:%M:%S")
