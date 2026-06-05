from data.schema import WranglingSchema
from data.wrangling import build_dataset
from fred.schema import FredSchema
from fred.database import FredDatabase
from fred.database import VALID_FREQUENCIES
from utils.validation import validate_json
from typing import List, Annotated, Literal
from pydantic import BaseModel, Field, ValidationError, field_validator
from pathlib import Path
import logging
from time import sleep


logger = logging.getLogger(__name__)


DEFAULT_SERIES_IDS = [
    'CPIAUCSL',
    'ACOGNO',
    'RSXFS',
    'PPIACO',
    'AMTMNO',
    'INDPRO'
]


class MainArgs(BaseModel):
    series_ids: Annotated[
        set[Annotated[str, Field(pattern='^[A-Z0-9]+$', min_length=1)]], 
        Field(min_length=2, description='List of FRED Series-IDs')
    ]
    frequency: Literal[tuple(VALID_FREQUENCIES)]
    target_path: Path
    
    @field_validator('target_path')
    @classmethod
    def validate_filetype(cls, path: Path) -> Path:
        if path.suffix.lower() != '.csv':
            raise ValueError('Invalid target-path. Must end with ".csv"')
        return path
    
    
def main(series_ids: List[str]=DEFAULT_SERIES_IDS, frequency: str='m', target_path: str='dataset.csv') -> None:

    try:
        MainArgs(series_ids=series_ids, frequency=frequency, target_path=target_path)
    except ValidationError as e:
        logger.error(e)
        return
    
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
            sample = db.get_data(sid, frequency, autosave=True)
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
    main()