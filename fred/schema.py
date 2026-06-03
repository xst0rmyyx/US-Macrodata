from pydantic import BaseModel, Field
from typing import Annotated, List


COMMON_SERIES_IDS = [
    'PAYEMS',   # All Employees, Total Nonfarm
    'UNRATE',   # Unemployment Rate
    'ICSA', # Initial Claims
    'JTSJOL',   # Job Openings: Total Nonfarm
    'CPIAUCSL', # Consumer Price Index for All Urban Consumers: All Items in U.S. City Average
    'CPILFESL', # Consumer Price Index for all Urban Consumers: All Items Less Food and Energy in U.S. City Average
    'PCEPI',    # Personal Consumption Expenditures: Chain-type Price Index
    'PCEPILFE', # Personal Consumption Expenditures Excluding Food and Energy (Chain-type Price Index)
    'GDPC1',    # Real Gross Domestic Product
    'RSXFS',    # Advance Retail Sales: Retail Trade
    'INDPRO',   # Industrial Production: Total Index
    'FEDFUNDS', # Effective Federal Funds Rate
    'T10Y2Y',   # 10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity
    'WALCL' # Balance Sheet: Total Assets: Total Assets(Less Eliminations from Consolidation)
]


class FredSchema(BaseModel):
    api_key: Annotated[str, Field(
        pattern='^[a-f0-9]{32}$',
        description='FRED API-Key [https://fredaccount.stlouisfed.org/apikeys]'
    )]