"""
Database repository for the Pharma Bottle Vision System.

Uses MySQL through SQLModel / SQLAlchemy.
"""

from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine, select

from app.config import settings
from storage.models import (
    AuditLog,
    Batch,
    Defect,
    Evidence,
    Inspection,
    Product,
    Recipe,
    SystemEvent,
)


class Database:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

        self.engine = create_engine(
            self.database_url,
            echo=False,
            pool_pre_ping=True,
        )

    def create_tables(self) -> None:
        SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return Session(self.engine)

    def session(self) -> Generator[Session, None, None]:
        with Session(self.engine) as session:
            yield session


database = Database(settings.database_url)


def initialize_database() -> None:
    database.create_tables()


def add_product(product: Product) -> Product:
    with database.get_session() as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product


def get_product_by_code(product_code: str) -> Product | None:
    with database.get_session() as session:
        statement = select(Product).where(
            Product.product_code == product_code
        )
        return session.exec(statement).first()


def add_recipe(recipe: Recipe) -> Recipe:
    with database.get_session() as session:
        session.add(recipe)
        session.commit()
        session.refresh(recipe)
        return recipe


def add_batch(batch: Batch) -> Batch:
    with database.get_session() as session:
        session.add(batch)
        session.commit()
        session.refresh(batch)
        return batch


def add_inspection(inspection: Inspection) -> Inspection:
    with database.get_session() as session:
        session.add(inspection)
        session.commit()
        session.refresh(inspection)
        return inspection


def add_defect(defect: Defect) -> Defect:
    with database.get_session() as session:
        session.add(defect)
        session.commit()
        session.refresh(defect)
        return defect


def add_evidence(evidence: Evidence) -> Evidence:
    with database.get_session() as session:
        session.add(evidence)
        session.commit()
        session.refresh(evidence)
        return evidence


def add_system_event(event: SystemEvent) -> SystemEvent:
    with database.get_session() as session:
        session.add(event)
        session.commit()
        session.refresh(event)
        return event


def add_audit_log(audit_log: AuditLog) -> AuditLog:
    with database.get_session() as session:
        session.add(audit_log)
        session.commit()
        session.refresh(audit_log)
        return audit_log