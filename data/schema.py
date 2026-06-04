from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal, Annotated
import re


VALID_PERIODS = [
    'D',   # Calendar day
    'B',   # Business day
    'W',   # Weekly
    'M',  # Month end
    'MS',  # Month start
    'Q',  # Quarter end
    'QS',  # Quarter start
    'Y',  # Year end
    'YS',  # Year start
    'h',   # Hourly
    'min', # Minutely
    's',   # Secondly
]


class WranglingSchema(BaseModel):
    startdate: Optional[str] = Field(
        None, 
        description='Observation-start in "XXXX-XX-XX" format.'
    )
    
    enddate: Optional[str] = Field(
        None, 
        description='Observation-end in "XXXX-XX-XX" format.'
    )
    
    resample_period: Optional[Literal[tuple(VALID_PERIODS)]] = Field(
        None, 
        description='Pandas frequency alias for resampling (e.g., "MS" for Month Start, "D" for Daily).'
    )
    
    row_threshold: Annotated[float, Field(
        ge=0.0, 
        le=1.0, 
        description='Maximum ratio of null-values in a row. 0.0 means no missing values allowed.'
    )]
    
    col_threshold: Annotated[float, Field(
        ge=0.0, 
        le=1.0, 
        description='Maximum ratio of null-values in a column. 0.0 means no missing values allowed.'
    )]
    
    interpolate_fill: Optional[List[str]] = Field(
        None,
        min_length=1,
        description='List of column names where remaining NaNs will be filled using linear interpolation.'
    )
    
    mean_fill: Optional[List[str]] = Field(
        None,
        min_length=1,
        description='List of column names where remaining NaNs will be filled with the respective column’s mean value.'
    )
    
    @field_validator('startdate', 'enddate')
    @classmethod
    def validate_dateformat(cls, value: str) -> str:
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if value == 'null':
            return None
        if not re.match(pattern, value):
            raise ValueError('Invalid Date. Must be in "XXXX-XX-XX" format')
        return value