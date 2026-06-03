from data.schema import WranglingSchema
from data.wrangling import build_dataset
from fred.schema import FredSchema
from fred.database import FredDatabase
from utils.validation import validate_json
from typing import List
import logging
from time import sleep


def main(series_ids: List[str], target_path: str='dataset.csv') -> None:
    db_configs = validate_json('fred/configs.json', FredSchema)
    df_configs = validate_json('data/configs.json', WranglingSchema)
    
    if db_configs is None:
        return
    if df_configs is None:
        return
    
    data = []
    with FredDatabase(db_configs['api_key']) as db:
        for sid in series_ids:
            sleep(.5)
            sample = db.get_data(sid, frequency='q', autosave=True)
            if not sample.empty:
                data.append(sample)
    
    if not data:
        return
        
    df = build_dataset(data, df_configs, dynamic=True, drop_rem=True)
    if not df.empty:
        df.to_csv(target_path)
        
    
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s – %(levelname)s – %(message)s',
    )
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s – %(levelname)s – %(message)s',
        filename='fred/database.py'
    )
    series_ids = [
        "GDPC1",
        "PCEPILFE",
        "RSXFS",
        "INDPRO"
    ]
    main(series_ids)