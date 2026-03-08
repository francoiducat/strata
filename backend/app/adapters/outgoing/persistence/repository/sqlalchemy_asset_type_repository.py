"""
SQLAlchemy AssetType Repository Implementation
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.entities.asset_type import AssetType
from app.domain.ports.repository.asset_type_repository import IAssetTypeRepository
from app.adapters.outgoing.persistence.models import AssetTypeModel
from app.adapters.outgoing.persistence.mappers.persistence_mapper import PersistenceMapper


class SQLAlchemyAssetTypeRepository(IAssetTypeRepository):
    """SQLAlchemy implementation of AssetTypeRepository."""

    def __init__(self, session: Session):
        self._session = session

    def save(self, entity: AssetType) -> AssetType:
        from app.adapters.outgoing.persistence.models.asset_type import AssetTypeModel as ATM
        orm_obj = self._session.get(ATM, str(entity.id))
        if orm_obj:
            orm_obj.code = entity.code
            orm_obj.label = entity.label
        else:
            orm_obj = AssetTypeModel(id=str(entity.id), code=entity.code, label=entity.label)
            self._session.add(orm_obj)
        self._session.flush()
        return entity

    def find_by_id(self, entity_id: str) -> Optional[AssetType]:
        entity_id = str(entity_id)
        orm_obj = self._session.query(AssetTypeModel).filter(AssetTypeModel.id == entity_id).first()
        return PersistenceMapper.asset_type_to_domain(orm_obj) if orm_obj else None

    def find_all(self) -> List[AssetType]:
        return [PersistenceMapper.asset_type_to_domain(at) for at in self._session.query(AssetTypeModel).all()]

    def delete(self, entity_id: str) -> bool:
        entity_id = str(entity_id)
        orm_obj = self._session.query(AssetTypeModel).filter(AssetTypeModel.id == entity_id).first()
        if orm_obj:
            self._session.delete(orm_obj)
            self._session.flush()
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        entity_id = str(entity_id)
        return self._session.query(
            self._session.query(AssetTypeModel).filter(AssetTypeModel.id == entity_id).exists()
        ).scalar()

    def find_by_code(self, code: str) -> Optional[AssetType]:
        orm_obj = self._session.query(AssetTypeModel).filter(AssetTypeModel.code == code).first()
        return PersistenceMapper.asset_type_to_domain(orm_obj) if orm_obj else None

    def find_all_codes(self) -> List[str]:
        rows = self._session.query(AssetTypeModel.code).all()
        return [r[0] for r in rows] if rows else []
