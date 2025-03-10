from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

# Association table for many-to-many relationships
alliance_members = Table(
    'alliance_members',
    Base.metadata,
    Column('alliance_id', Integer, ForeignKey('alliances.id')),
    Column('nation_id', Integer, ForeignKey('nations.id'))
)

# Association table for treaties
treaty_participants = Table(
    'treaty_participants',
    Base.metadata,
    Column('treaty_id', Integer, ForeignKey('treaties.id')),
    Column('nation_id', Integer, ForeignKey('nations.id'))
)

class Nation(Base):
    __tablename__ = 'nations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    gdp = Column(Float, nullable=False, default=0.0)
    military_power = Column(Float, nullable=False, default=0.0)
    population = Column(Float, nullable=False, default=0.0)
    has_nuclear_weapons = Column(Boolean, default=False)
    
    # Relationships
    leader_id = Column(Integer, ForeignKey('leaders.id'))
    leader = relationship("Leader", back_populates="nation")
    
    alliances = relationship("Alliance", secondary=alliance_members, back_populates="members")
    treaties = relationship("Treaty", secondary=treaty_participants, back_populates="participants")
    
    # Military assets
    ground_forces = Column(Float, default=0.0)
    air_forces = Column(Float, default=0.0)
    naval_forces = Column(Float, default=0.0)
    nuclear_arsenal = Column(Integer, default=0)
    
    # Economic factors
    tax_rate = Column(Float, default=0.25)
    research_spending = Column(Float, default=0.05)
    military_spending = Column(Float, default=0.10)
    
    # Reputation
    global_reputation = Column(Float, default=50.0)  # 0-100 scale
    
    def __repr__(self):
        return f"<Nation(name='{self.name}', gdp={self.gdp}, military_power={self.military_power})>"

class Leader(Base):
    __tablename__ = 'leaders'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    personality_type = Column(String, nullable=False)  # aggressive, diplomatic, opportunistic
    
    # Relationships
    nation = relationship("Nation", back_populates="leader", uselist=False)
    
    # AI behavior parameters
    aggression_factor = Column(Float, default=0.5)  # 0-1 scale
    diplomatic_factor = Column(Float, default=0.5)  # 0-1 scale
    economic_focus = Column(Float, default=0.5)  # 0-1 scale
    military_focus = Column(Float, default=0.5)  # 0-1 scale
    
    def __repr__(self):
        return f"<Leader(name='{self.name}', personality_type='{self.personality_type}')>"

class Alliance(Base):
    __tablename__ = 'alliances'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    formation_date = Column(DateTime, default=datetime.datetime.utcnow)
    alliance_type = Column(String, nullable=False)  # military, economic, research
    
    # Relationships
    members = relationship("Nation", secondary=alliance_members, back_populates="alliances")
    
    def __repr__(self):
        return f"<Alliance(name='{self.name}', type='{self.alliance_type}')>"

class Treaty(Base):
    __tablename__ = 'treaties'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    treaty_type = Column(String, nullable=False)  # peace, trade, arms control
    formation_date = Column(DateTime, default=datetime.datetime.utcnow)
    expiration_date = Column(DateTime, nullable=True)
    
    # Relationships
    participants = relationship("Nation", secondary=treaty_participants, back_populates="treaties")
    
    def __repr__(self):
        return f"<Treaty(name='{self.name}', type='{self.treaty_type}')>"

class GameEvent(Base):
    __tablename__ = 'game_events'
    
    id = Column(Integer, primary_key=True)
    event_type = Column(String, nullable=False)  # war, alliance, disaster, breakthrough
    description = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Foreign keys for involved nations
    primary_nation_id = Column(Integer, ForeignKey('nations.id'), nullable=True)
    secondary_nation_id = Column(Integer, ForeignKey('nations.id'), nullable=True)
    
    def __repr__(self):
        return f"<GameEvent(type='{self.event_type}', date='{self.date}')>"

class ResearchProgress(Base):
    __tablename__ = 'research_progress'
    
    id = Column(Integer, primary_key=True)
    nation_id = Column(Integer, ForeignKey('nations.id'))
    technology_name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # military, economic, intelligence
    progress = Column(Float, default=0.0)  # 0-100 scale
    completed = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<ResearchProgress(tech='{self.technology_name}', progress={self.progress})>" 