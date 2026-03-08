"""
SQLAlchemy Category Repository Implementation
"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

from app.domain.entities.category import Category
from app.domain.ports.repository.category_repository import ICategoryRepository
from app.adapters.outgoing.persistence.models import CategoryModel, AssetModel
from app.adapters.outgoing.persistence.mappers.persistence_mapper import PersistenceMapper


class SQLAlchemyCategoryRepository(ICategoryRepository):
    """SQLAlchemy implementation of CategoryRepository."""

    def __init__(self, session: Session):
        self._session = session

    def save(self, entity: Category) -> Category:
        orm_obj = self._session.get(CategoryModel, str(entity.id))
        if orm_obj:
            orm_obj.name = entity.name
            orm_obj.parent_id = str(entity.parent.id) if entity.parent else None
        else:
            orm_obj = PersistenceMapper.category_to_orm(entity)
            self._session.add(orm_obj)
        self._session.flush()
        return entity

    def find_by_id(self, entity_id: str) -> Optional[Category]:
        entity_id = str(entity_id)
        orm_obj = self._session.query(CategoryModel).options(
            joinedload(CategoryModel.parent)
        ).filter(CategoryModel.id == entity_id).first()
        return PersistenceMapper.category_to_domain(orm_obj) if orm_obj else None

    def find_all(self) -> List[Category]:
        return [
            PersistenceMapper.category_to_domain(c)
            for c in self._session.query(CategoryModel).options(
                joinedload(CategoryModel.parent)
            ).all()
        ]

    def delete(self, entity_id: str) -> bool:
        entity_id = str(entity_id)
        orm_obj = self._session.query(CategoryModel).filter(CategoryModel.id == entity_id).first()
        if orm_obj:
            self._session.delete(orm_obj)
            self._session.flush()
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        entity_id = str(entity_id)
        return self._session.query(
            self._session.query(CategoryModel).filter(CategoryModel.id == entity_id).exists()
        ).scalar()

    def find_by_name(self, name: str) -> Optional[Category]:
        orm_obj = self._session.query(CategoryModel).options(
            joinedload(CategoryModel.parent)
        ).filter(CategoryModel.name == name).first()
        return PersistenceMapper.category_to_domain(orm_obj) if orm_obj else None

    def find_by_asset(self, asset_id: str) -> List[Category]:
        asset = self._session.query(AssetModel).options(
            joinedload(AssetModel.categories).joinedload(CategoryModel.parent)
        ).filter(AssetModel.id == str(asset_id)).first()
        return [PersistenceMapper.category_to_domain(c) for c in asset.categories] if asset else []

    def attach_to_asset(self, asset_id: str, category_id: str) -> bool:
        asset = self._session.query(AssetModel).filter(AssetModel.id == str(asset_id)).first()
        cat = self._session.query(CategoryModel).filter(CategoryModel.id == str(category_id)).first()
        if asset and cat and cat not in asset.categories:
            asset.categories.append(cat)
            self._session.flush()
            return True
        return False

    def detach_from_asset(self, asset_id: str, category_id: str) -> bool:
        asset = self._session.query(AssetModel).options(
            joinedload(AssetModel.categories)
        ).filter(AssetModel.id == str(asset_id)).first()
        cat = self._session.query(CategoryModel).filter(CategoryModel.id == str(category_id)).first()
        if asset and cat and cat in asset.categories:
            asset.categories.remove(cat)
            self._session.flush()
            return True
        return False

    def find_root_categories(self) -> List[Category]:
        rows = self._session.query(CategoryModel).filter(
            CategoryModel.parent_id == None
        ).all()
        return [PersistenceMapper.category_to_domain(c) for c in rows]

    def find_children(self, parent_id) -> List[Category]:
        rows = self._session.query(CategoryModel).options(
            joinedload(CategoryModel.parent)
        ).filter(CategoryModel.parent_id == str(parent_id)).all()
        return [PersistenceMapper.category_to_domain(c) for c in rows]

    def count_assets(self, category_id) -> int:
        return self._session.query(AssetModel).join(
            AssetModel.categories
        ).filter(CategoryModel.id == str(category_id)).count()
