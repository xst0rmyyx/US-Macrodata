from fred.database import FredDatabase
from fred.schema import FredSchema
from utils.validation import validate_json
import logging
from time import sleep


def main() -> None:
    configs = validate_json('fred/configs.json', FredSchema)
    if configs is None:
        return
    
    with FredDatabase(configs['api_key']) as db:
        for sid in configs['series_ids']:
            sleep(.5)
            db.get_data(sid)
            

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s – %(levelname)s – %(message)s'
    )
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s – %(levelname)s – %(message)s',
        filename='fred/database.py'
    )
    main()
