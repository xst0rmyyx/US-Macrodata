from pydantic import BaseModel, Field
from typing import Annotated, List


COMMON_SERIES_IDS = [
    'CPIAUCSL', # Consumer Price Index for All Urban Consumers: All Items in U.S. City Average
    'ACOGNO',   # Manufacturer’s New Orders: Consumer Goods
    'RSXFS',    # Advance Retail Sales: Retail Trade
    'PPIACO',   # Producer Price Index by Commodity: All Commodities
    'AMTMNO',   # Manufacturer’s New Orders: Total Manufacturing
    'INDPRO',   # Industrial Production: Total Index
    'PAYEMS',   # All Employees, Total Nonfarm
    'UNRATE',   # Civilian Unemployment Rate
    'ICSA', # Initial Claims
    'JTSJOL',   # Job Openings: Total Nonfarm
    'FEDFUNDS', # Effective Federal Funds Rate
    'M2SL', # M2 Money Stock
    'WALCL',    # Balance Sheet: Assets: Total Assets (Less Eliminations from Consolidation): Wednesday Level
    'ULCBS',    # Business Sector: Unit Labor Cost
    'ULCMFG',   # Manufacturing Sector: Unit Labor Cost
    'CP',   # Corporate Profits After Tax (without IVA and CCAdj)
    'GDP',  # Gross Domestic Product
    'PERMIT',   # New Privatly-Owned Housing Units Authorized in Permit-Issuing Places
    'HOUST',    # New Privatly-Owned Housing Units Started: Total Units
    'MORTGAGE30US', # 30-Year Fixed Rate Mortgage Average in the United States
    'DGS10',    # 10-Year Treasury Constant Maturity Rate
    'DGS2', # 2-Year Treasury Constant Maturity Rate
    'T10Y2Y',   # 10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity
    'BAMLH0A0HYM2', # ICE BofA US High Yield Index Option-Adjusted Spread
    'VIXCLS',   # CBOE Volatility Index: VIX
    'SP500' # S&P 500
]


class FredSchema(BaseModel):
    api_key: Annotated[str, Field(
        pattern='^[a-f0-9]{32}$',
        description='FRED API-Key [https://fredaccount.stlouisfed.org/apikeys]'
    )]