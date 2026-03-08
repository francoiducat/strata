"""
SQLAlchemy Tag Repository Implementation
"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

from app.domain.entities.tag import Tag
from app.domain.ports.repository.tag_repository import ITagRepository
from app.adapters.outgoing.persistence.models import TagModel, AssetModel
from app.adapters.outgoing.persistence.mappers.persistence_mapper import PersistenceMapper


class SQLAlchemyTagRepository(ITagRepository):
    """SQLAlchemy implementation of TagRepository."""

    def __init__(self, session: Session):
        self._session = session

    def save(self, entity: Tag) -> Tag:
        orm_obj = self._session.get(TagModel, str(entity.id))
        if orm_obj:
            orm_obj.name = entity.name
        else:
            orm_obj = PersistenceMapper.tag_to_orm(entity)
            self._session.add(orm_obj)
        self._session.flush()
        return entity

    def find_by_id(self, entity_id: str) -> Optional[Tag]:
        orm_obj = self._session.query(TagModel).filter(TagModel.id == entity_id).first()
        return PersistenceMapper.tag_to_domain(orm_obj) if orm_obj else None

    def find_all(self) -> List[Tag]:
        return [PersistenceMapper.tag_to_domain(t) for t in self._session.query(TagModel).all()]

    def delete(self, entity_id: str) -> bool:
        orm_obj = self._session.query(TagModel).filter(TagModel.id == entity_id).first()
        if orm_obj:
            self._session.delete(orm_obj)
            self._session.flush()
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        return self._session.query(
            self._session.query(TagModel).filter(TagModel.id == entity_id).exists()
        ).scalar()

    def find_by_name(self, name: str) -> Optional[Tag]:
        orm_obj = self._session.query(TagModel).filter(TagModel.name == name).first()
        return PersistenceMapper.tag_to_domain(orm_obj) if orm_obj else None

    def find_by_asset(self, asset_id: str) -> List[Tag]:
        asset = self._session.query(AssetModel).options(
            joinedload(AssetModel.tags)
        ).filter(AssetModel.id == str(asset_id)).first()
        return [PersistenceMapper.tag_to_domain(t) for t in asset.tags] if asset else []

    def attach_to_asset(self, asset_id: str, tag_id: str) -> bool:
        asset = self._session.query(AssetModel).filter(AssetModel.id == str(asset_id)).first()
        tag_orm = self._session.query(TagModel).filter(TagModel.id == str(tag_id)).first()
        if asset and tag_orm and tag_orm not in asset.tags:
            asset.tags.append(tag_orm)
            self._session.flush()
            return True
        return False

    def detach_from_asset(self, asset_id: str, tag_id: str) -> bool:
        asset = self._session.query(AssetModel).options(
            joinedload(AssetModel.tags)
        ).filter(AssetModel.id == str(asset_id)).first()
        tag_orm = self._session.query(TagModel).filter(TagModel.id == str(tag_id)).first()
        if asset and tag_orm and tag_orm in asset.tags:
            asset.tags.remove(tag_orm)
            self._session.flush()
            return True
        return False
