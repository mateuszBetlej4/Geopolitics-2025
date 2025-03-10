import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:admin@localhost:5433/geopolitics_2025"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database (create tables)
def init_db():
    from .models import Base
    Base.metadata.create_all(bind=engine)

# Populate database with initial data
def populate_initial_data():
    from .models import Nation, Leader, Alliance
    from sqlalchemy.orm import Session
    
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(Nation).count() > 0:
        db.close()
        return
    
    # Create leaders
    trump = Leader(
        name="Donald Trump",
        personality_type="aggressive",
        aggression_factor=0.8,
        diplomatic_factor=0.3,
        economic_focus=0.7,
        military_focus=0.8
    )
    
    li_qiang = Leader(
        name="Li Qiang",
        personality_type="diplomatic",
        aggression_factor=0.5,
        diplomatic_factor=0.7,
        economic_focus=0.9,
        military_focus=0.6
    )
    
    putin = Leader(
        name="Vladimir Putin",
        personality_type="opportunistic",
        aggression_factor=0.9,
        diplomatic_factor=0.4,
        economic_focus=0.5,
        military_focus=0.9
    )
    
    # Add leaders to session
    db.add_all([trump, li_qiang, putin])
    db.commit()
    
    # Create nations
    usa = Nation(
        name="United States",
        gdp=25000.0,
        military_power=100.0,
        population=330.0,
        has_nuclear_weapons=True,
        leader=trump,
        ground_forces=90.0,
        air_forces=100.0,
        naval_forces=100.0,
        nuclear_arsenal=5500,
        global_reputation=75.0
    )
    
    china = Nation(
        name="China",
        gdp=18000.0,
        military_power=85.0,
        population=1400.0,
        has_nuclear_weapons=True,
        leader=li_qiang,
        ground_forces=95.0,
        air_forces=80.0,
        naval_forces=70.0,
        nuclear_arsenal=350,
        global_reputation=60.0
    )
    
    russia = Nation(
        name="Russia",
        gdp=4000.0,
        military_power=70.0,
        population=145.0,
        has_nuclear_weapons=True,
        leader=putin,
        ground_forces=85.0,
        air_forces=75.0,
        naval_forces=65.0,
        nuclear_arsenal=6000,
        global_reputation=40.0
    )
    
    # Add nations to session
    db.add_all([usa, china, russia])
    db.commit()
    
    # Create alliances
    nato = Alliance(
        name="NATO",
        alliance_type="military",
        members=[usa]
    )
    
    shanghai_pact = Alliance(
        name="Shanghai Cooperation Organization",
        alliance_type="economic",
        members=[china, russia]
    )
    
    # Add alliances to session
    db.add_all([nato, shanghai_pact])
    db.commit()
    
    db.close() 