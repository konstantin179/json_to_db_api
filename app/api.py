import pandas as pd
from app import logger
from fastapi import APIRouter, HTTPException
from app.schemas import RequestDataAnalyticsByDays, ResponseWriteToDBSuccess
from app.database import engine, psql_insert_copy, delete_duplicates_from_data_analytics_bydays_main_table
from sqlalchemy.exc import SQLAlchemyError


logger = logger.init_logger(__name__)

router = APIRouter()


@router.post("/db/data_analytics_bydays", tags=['market_db'],
             response_model=ResponseWriteToDBSuccess)
async def write_to_data_analytics_bydays(data: RequestDataAnalyticsByDays):
    """Write data to data_analytics_bydays_main table in db."""
    data_dict = {}
    for key, value in data:
        if value is not None:
            data_dict[key] = value
    df = pd.DataFrame.from_dict(data_dict)
    if df.isnull().values.any():
        logger.warning("400 Bad file structure")
        raise HTTPException(status_code=400, detail="Bad file structure.")
    try:
        df.to_sql('data_analytics_bydays_main', engine, if_exists='append', method=psql_insert_copy, index=False)
        delete_duplicates_from_data_analytics_bydays_main_table(engine)
        logger.info("Data successfully saved")
    except (Exception, SQLAlchemyError) as e:
        logger.error(repr(e))

    return ResponseWriteToDBSuccess()
