from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Annotated


VALID_PERIODS = [
    'W',	# Weekly
    'M',	# Month end
    'MS',	# Month start
    'Q',	# Quarter end
    'QS',	# Quarter start
    'Y',	# Year end
    'YS'	# Year start
]


class WranglingSchema(BaseModel):
    resample_period: Optional[Literal[tuple(VALID_PERIODS)]] = Field(
        None, 
        description='Pandas frequency alias for resampling (e.g., "MS" for Month Start, "Q" for Quarter End).'
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
