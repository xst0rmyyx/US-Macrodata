from fred.database import FredDatabase
from fred.database import VALID_FREQUENCIES
from fred.schema import COMMON_SERIES_IDS
from fred.schema import FredSchema
from utils.validation import validate_json
from pydantic import BaseModel, Field, ValidationError
from typing import Annotated, Literal, List
import logging
from time import sleep


logger = logging.getLogger(__name__)


class MainArgs(BaseModel):
    series_ids: Annotated[
        set[Annotated[str, Field(pattern='^[A-Z0-9]+$', min_length=1)]], 
        Field(min_length=1, description='List of FRED Series-IDs')
    ]
    frequency: Literal[tuple(VALID_FREQUENCIES)]
    
    
def main(series_ids: List[str]=COMMON_SERIES_IDS, frequency: str='q') -> None:
    try:
        MainArgs(series_ids=series_ids, frequency=frequency)
    except ValidationError as e:
        logger.error(e)
        return
        
    configs = validate_json('fred/configs.json', FredSchema)
    if configs is None:
        return
    
    with FredDatabase(configs['api_key']) as db:
        existing = db.get_existing_tables()
        for sid in series_ids:
            if f'{sid}_{frequency}' not in existing:
                sleep(.5)
                db.get_data(sid, frequency, autosave=True)
            

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s – %(levelname)s – %(message)s'
    )
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s – %(levelname)s – %(message)s',
        filename='fred/database.py'
    )
    main()
