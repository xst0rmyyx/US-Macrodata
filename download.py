from fred.database import FredDatabase
from fred.schema import FredSchema
from utils.validation import validate_json
import logging


logger = logging.getLogger(__name__)


def main() -> None:
    configs = validate_json('fred/configs.json', FredSchema)
    if configs is None:
        return
    
    with FredDatabase(configs['api_key']) as db:
        for sid in configs['series_ids']:
            db.get_data(sid)
            

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s – %(levelname)s – %(message)s'
    )
    main()