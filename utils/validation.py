from typing import Type, Optional, Dict
from pydantic import BaseModel, ValidationError
import json
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


def validate_json(path: str, schema: Type[BaseModel]) -> Optional[Dict]:
    path = Path(path)
    
    if not path.exists() or not path.is_file():
        logger.error(f'File {path} not found')
        return
    
    try:
        with open(path, 'r') as file:
            raw = json.load(file)
    
    except json.JSONDecodeError as e:
        logger.error(f'Invalid JSON in {path}\n {e}')
        return
        
    try:
        return schema(**raw).model_dump()
    
    except ValidationError as e:
        logger.error(f'Schema violated in {path}\n   {e}')
        return