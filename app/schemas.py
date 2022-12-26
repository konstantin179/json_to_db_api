from pydantic import BaseModel, validator
from typing import Union, List


class BaseDataAnalyticsByDays(BaseModel):
    api_id: List[Union[str, int]]
    sku_id: List[Union[str, int]]
    sku_name: Union[List[str], None] = None
    date: List[str]

    @validator('api_id')
    def validation_api_id(cls, v):
        if len(v) == 0:
            raise ValueError('api_id must not be empty list')
        return v

    @validator('sku_id')
    def validation_sku_id(cls, v):
        if len(v) == 0:
            raise ValueError('sku_id must not be empty list')
        return v

    @validator('date')
    def validation_date(cls, v):
        if len(v) == 0:
            raise ValueError('date must not be empty list')
        return v


class RequestDataAnalyticsByDays(BaseDataAnalyticsByDays):
    category_id: Union[List[Union[str, int]], None] = None
    category_name: Union[List[str], None] = None
    brand_id: Union[List[Union[str, int]], None] = None
    brand_name: Union[List[str], None] = None
    hits_view_search: Union[List[float], None] = None
    hits_view_pdp: Union[List[float], None] = None
    hits_view: Union[List[float], None] = None
    hits_tocart_search: Union[List[float], None] = None
    hits_tocart_pdp: Union[List[float], None] = None
    hits_tocart: Union[List[float], None] = None
    session_view_search: Union[List[float], None] = None
    session_view_pdp: Union[List[float], None] = None
    session_view: Union[List[float], None] = None
    conv_tocart_search: Union[List[float], None] = None
    conv_tocart_pdp: Union[List[float], None] = None
    conv_tocart: Union[List[float], None] = None
    revenue: Union[List[float], None] = None
    returns: Union[List[float], None] = None
    cancellations: Union[List[float], None] = None
    ordered_units: Union[List[float], None] = None
    delivered_units: Union[List[float], None] = None
    adv_view_pdp: Union[List[float], None] = None
    adv_view_search_category: Union[List[float], None] = None
    adv_view_all: Union[List[float], None] = None
    adv_sum_all: Union[List[float], None] = None
    position_category: Union[List[float], None] = None
    postings: Union[List[float], None] = None
    postings_premium: Union[List[float], None] = None
    region_id: Union[List[Union[str, int]], None] = None
    region_name: Union[List[str], None] = None


class ResponseWriteToDBSuccess(BaseModel):
    message = "Data successfully saved"
