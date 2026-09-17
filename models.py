from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, unique=True, nullable=False)
    temperature = Column(Float)
    precipitation = Column(Float)
    wind_speed = Column(Float)

    def __repr__(self):
        return f"<WeatherRecord {self.time} {self.temperature}°C>"

engine = create_engine("sqlite:///weather.db")
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)