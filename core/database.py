"""
EXIMIUS AI — Database Layer
SQLite via SQLAlchemy. Stores startup analyses, founder profiles, and memos.
"""

import json
import os
from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# ── Database setup ────────────────────────────────────────────────────────────

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "eximius.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# ── ORM Models ────────────────────────────────────────────────────────────────

class StartupAnalysis(Base):
    __tablename__ = "startup_analyses"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False, index=True)
    website_url = Column(String(500))
    market_category = Column(String(200))
    business_model = Column(String(200))
    investment_score = Column(Float)
    recommendation = Column(String(20))
    analysis_json = Column(Text)  # full JSON blob
    created_at = Column(DateTime, default=datetime.utcnow)


class FounderProfile(Base):
    __tablename__ = "founder_profiles"

    id = Column(Integer, primary_key=True, index=True)
    founder_name = Column(String(200), index=True)
    overall_score = Column(Float)
    founder_archetype = Column(String(200))
    profile_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class InvestmentMemo(Base):
    __tablename__ = "investment_memos"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False, index=True)
    recommendation = Column(String(20))
    memo_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


# ── Init ──────────────────────────────────────────────────────────────────────

def init_db() -> None:
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


# ── CRUD: Startups ────────────────────────────────────────────────────────────

def save_startup_analysis(data: dict[str, Any], website_url: str = "") -> int:
    """Persist a startup analysis and return its ID."""
    init_db()
    with SessionLocal() as session:
        record = StartupAnalysis(
            company_name=data.get("company_name", "Unknown"),
            website_url=website_url,
            market_category=data.get("market_category", ""),
            business_model=data.get("business_model", ""),
            investment_score=data.get("investment_score", 0),
            recommendation=data.get("recommendation", ""),
            analysis_json=json.dumps(data),
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record.id


def get_all_startup_analyses() -> list[dict[str, Any]]:
    """Return all saved startup analyses, newest first."""
    init_db()
    with SessionLocal() as session:
        records = (
            session.query(StartupAnalysis)
            .order_by(StartupAnalysis.created_at.desc())
            .all()
        )
        return [
            {
                "id": r.id,
                "company_name": r.company_name,
                "market_category": r.market_category,
                "investment_score": r.investment_score,
                "recommendation": r.recommendation,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else "",
                "data": json.loads(r.analysis_json) if r.analysis_json else {},
            }
            for r in records
        ]


def get_startup_analysis(record_id: int) -> dict[str, Any] | None:
    """Retrieve a single startup analysis by ID."""
    init_db()
    with SessionLocal() as session:
        record = session.query(StartupAnalysis).filter_by(id=record_id).first()
        if record and record.analysis_json:
            return json.loads(record.analysis_json)
        return None


# ── CRUD: Founders ────────────────────────────────────────────────────────────

def save_founder_profile(data: dict[str, Any]) -> int:
    """Persist a founder profile and return its ID."""
    init_db()
    with SessionLocal() as session:
        record = FounderProfile(
            founder_name=data.get("founder_name", "Unknown"),
            overall_score=data.get("overall_score", 0),
            founder_archetype=data.get("founder_archetype", ""),
            profile_json=json.dumps(data),
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record.id


def get_all_founder_profiles() -> list[dict[str, Any]]:
    """Return all saved founder profiles, newest first."""
    init_db()
    with SessionLocal() as session:
        records = (
            session.query(FounderProfile)
            .order_by(FounderProfile.created_at.desc())
            .all()
        )
        return [
            {
                "id": r.id,
                "founder_name": r.founder_name,
                "overall_score": r.overall_score,
                "founder_archetype": r.founder_archetype,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else "",
                "data": json.loads(r.profile_json) if r.profile_json else {},
            }
            for r in records
        ]


# ── CRUD: Memos ───────────────────────────────────────────────────────────────

def save_memo(data: dict[str, Any]) -> int:
    """Persist an investment memo and return its ID."""
    init_db()
    with SessionLocal() as session:
        record = InvestmentMemo(
            company_name=data.get("company_name", "Unknown"),
            recommendation=data.get("investment_recommendation", ""),
            memo_json=json.dumps(data),
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record.id


def get_all_memos() -> list[dict[str, Any]]:
    """Return all saved memos, newest first."""
    init_db()
    with SessionLocal() as session:
        records = (
            session.query(InvestmentMemo)
            .order_by(InvestmentMemo.created_at.desc())
            .all()
        )
        return [
            {
                "id": r.id,
                "company_name": r.company_name,
                "recommendation": r.recommendation,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else "",
                "data": json.loads(r.memo_json) if r.memo_json else {},
            }
            for r in records
        ]
