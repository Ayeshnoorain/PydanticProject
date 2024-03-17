import pandas as pd
import pyodbc
from pydantic import BaseModel, ValidationError, StringConstraints,ConfigDict, Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Mapped
from typing_extensions import Annotated

# Define your Pydantic model (similar to the one you provided)
Base = declarative_base()

class Asics(Base):
    __tablename__ = '[dbo].[Asics_SM_2020_Dec_Set1]'

    user_id: Mapped[str] = Column(String, primary_key=True, nullable=False, unique=True)
    gender: Mapped[int] = Column(Integer,nullable=False)
    age: Mapped[int] = Column(Integer)
    q123_4: Mapped[int] = Column(Integer, nullable=False)



class SurveyRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: Annotated[str, StringConstraints(max_length=10)]
    gender: int
    age: int
    q123_4: int = Field(default=5, validate_default=True)




def main():
    # Database connection details
    server = '10.190.30.51'
    database = 'Asics_SportsMarketing_Dev'
    username = 'username'
    password = 'password'
    driver = '{ODBC Driver 17 for SQL Server}'

    # Establish a database connection
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM Asics_SM_2020_Dec_Set1")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    df = pd.DataFrame.from_records(rows, columns=columns)
    #print(df)


    # Apply validations
    try:
        records = [SurveyRecord(user_id=row.user_id, gender=row.gender, age=row.age, q123_4=row.q123_4) for row in rows]
    except ValidationError as e:
        print(f"Validation error: {e}")
    # Close the database connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

