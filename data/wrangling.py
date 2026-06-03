import pandas as pd
import logging
from typing import List, Dict, Union, Optional


logger = logging.getLogger(__name__)


DEFAULT_CONFIGS = {
    'resample_period': None,
    'row_threshold': 0.35,
    'col_threshold': 0.25,
    'interpolate_fill': None,
    'mean_fill': None
}


def build_dataset(
    data: List[pd.Series],
    configs: Dict[str, Union[Optional[str], float, Optional[List[str]]]]=DEFAULT_CONFIGS,
    dynamic: bool=True,
    drop_rem: bool=False
) -> pd.DataFrame:
    
    # Data-Merging
    try:
        df = pd.concat(data, axis=1)
        
    except Exception:
        logger.exception('Failed to concat input-data')
        return pd.DataFrame()
    
    # Datetime-Index standardizing
    if configs['resample_period'] is not None:
        try:
            df.index = pd.to_datetime(df.index)
            df = df.resample(configs['resample_period']).mean()
            
        except Exception:
            logger.exception('Failed to standardize dataframe observations')
            return pd.DataFrame()
    
    org_rows = len(df)
    
    # Vertical NaN-Handling
    rownans = df.isna().sum(axis=1)
    rowdrop = rownans.index[rownans >= len(df.columns) * configs['row_threshold']]
    df = df.drop(rowdrop)
    logger.info(f'Dropped {len(rowdrop)} rows')
    
    # Horizontal NaN-Handling
    if not df.empty:
        colnans = df.isna().sum()
        col_thres_base = len(df) if dynamic else org_rows
        coldrop = colnans.index[colnans >= col_thres_base * configs['col_threshold']]
        df = df.drop(coldrop, axis=1)
        logger.info(f'Columns dropped:\n{coldrop}')
    else:
        logger.warning('No columns dropped – dataframe is empty')
        return pd.DataFrame()
    
    df.columns = [i.split('_')[0] for i in df.columns]
    # NaN-Filling
    if configs['interpolate_fill'] is not None:
        interpol_cols = [col for col in configs['interpolate_fill'] if col in list(df.columns)]
        if interpol_cols:
            df[interpol_cols] = df[interpol_cols].interpolate(limit_direction='both')
            logger.info(f'Interpolated {interpol_cols}')
    
    if configs['mean_fill'] is not None:
        mfill_cols = [col for col in configs['mean_fill'] if col in list(df.columns)]
        if mfill_cols:
            df[mfill_cols] = df[mfill_cols].fillna(df[mfill_cols].mean())
            logger.info(f'Filled {mfill_cols} with their mean')
            
    if drop_rem:
        df = df.dropna()
        logger.info(f'Dropped {org_rows - len(df)} remaining rows')
        if df.empty:
            logger.warning('Dataframe is empty after dropping remaining rows containing NaNs')
            return pd.DataFrame()
    
    return df