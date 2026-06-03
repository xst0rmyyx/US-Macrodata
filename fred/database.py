from fredapi import Fred
import pandas as pd
import sqlite3
import logging
from typing import List


logger = logging.getLogger(__name__)

# More Info on https://fred.stlouisfed.org/docs/api/fred/series_observations.html#frequency
VALID_FREQUENCIES = [
    'd', 'w', 'bw', 'm', 'q', 'sa', 'a',    # without period descriptions
    'wef', 'weth', 'wew', 'wetu', 'wem', 'wesu', 'wesa', 'bwew', 'bwem' # with period descriptions
]


class FredDatabase:
    def __init__(self, api_key: str) -> None:
        self._fred = Fred(api_key)
        self._con = sqlite3.connect('Fred.db')
        
        
    def __enter__(self) -> 'FredDatabase':
        return self
        
        
    def __exit__(self, *args) -> None:
        try:
            self._con.close()
            
        except Exception:
            logger.exception('Failed to close database')
            
            
    def _load_local(self, name: str) -> pd.Series:
        series_id = name.split('_')[0]
        
        try:
            query = f'SELECT * FROM {name};'
            data = pd.read_sql(query, self._con, index_col='index')
            
            data.index = pd.to_datetime(data.index)
            data = pd.Series(data[series_id], data.index, dtype=float, name=name)
            logger.info(f'Successfully loaded {name} from DB')
            return data
            
        except Exception:
            logger.exception(f'Failed to load {name} from DB')
            return pd.Series(name=name, dtype=float)
    
    
    def _load_remote(self, series_id: str, frequency: str) -> pd.Series:
        try:
            data = self._fred.get_series(series_id, frequency=frequency)
            data.index.name = 'index'
            data.name = series_id
            logger.info(f'Successfully fetched {series_id} from API')
            return data
            
        except Exception:
            logger.exception(f'Failed to fetch {series_id} from API')
            return pd.Series(name=series_id, dtype=float)
            
            
    def save_data(self, data: pd.Series, name: str, if_exists: str='fail') -> None:
        VALID_ACTIONS = ['replace', 'fail', 'append']
        
        if if_exists not in VALID_ACTIONS:
            logger.error(f'Invalid action {if_exists} for handling existing table')
            return
            
        if data.empty:
            logger.error(f'Aborted saving {name} to DB – {type(data)} is empty')
            return
            
        try:
            data.to_sql(name, self._con, if_exists=if_exists, index_label='index')
            self._con.commit()
            logger.info(f'Successfully saved {name} to DB')
            
        except Exception:
            logger.exception(f'Failed to save {name} to DB')
            
            
    def get_existing_tables(self) -> List[str]:
        query = 'SELECT name FROM sqlite_master WHERE TYPE="table"'
        cur = self._con.cursor()
        cur.execute(query)
        
        return [name[0] for name in cur.fetchall()]
            
            
    def get_data(self, series_id: str, frequency: str='q', autosave: bool=True) -> pd.Series:
        if frequency not in VALID_FREQUENCIES:
            logger.error(f'Invalid frequency {frequency} requested for {series_id}')
            return pd.Series(name=series_id)
        
        name = f'{series_id}_{frequency}'
        
        existing_tables = self.get_existing_tables()
        
        if name in existing_tables:
            logger.info(f'{name} found in DB')
            
            return self._load_local(name)
        
        data = self._load_remote(series_id, frequency)
        if autosave:
            self.save_data(data, name)
            
        return data