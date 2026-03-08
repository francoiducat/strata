"""
SQLAlchemy Asset Repository Implementation
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload, subqueryload

from app.domain.entities.asset import Asset
from app.domain.ports.repository.asset_repository import IAssetRepository
from app.adapters.outgoing.persistence.models.asset import AssetModel
from app.adapters.outgoing.persistence.models import CategoryModel, TagModel
from app.adapters.outgoing.persistence.mappers.persistence_mapper import PersistenceMapper


class SQLAlchemyAssetRepository(IAssetRepository):
    """SQLAlchemy implementation of AssetRepository."""

    def __init__(self, session: Session):
        self._session = session

    def _load_full(self, asset_id: str) -> Optional[AssetModel]:
        """Load an AssetModel with all required eager relationships."""
        return self._session.query(AssetModel).options(
            joinedload(AssetModel.portfolio),
            joinedload(AssetModel.asset_type),
            joinedload(AssetModel.tags),
            joinedload(AssetModel.categories).joinedload(CategoryModel.parent),
        ).filter(AssetModel.id == str(asset_id)).first()

    def save(self, entity: Asset) -> Asset:
        orm_obj = self._session.get(AssetModel, str(entity.id))
        if orm_obj:
            orm_obj.name = entity.name
            orm_obj.portfolio_id = str(entity.portfolio.id)
            orm_obj.asset_type_id = str(entity.asset_type.id)
            orm_obj.quantity = entity.quantity
            orm_obj.disposed = entity.disposed
            orm_obj.updated_at = entity.updated_at
            orm_obj.updated_by = entity.updated_by
        else:
            orm_obj = PersistenceMapper.asset_to_orm(entity)
            self._session.add(orm_obj)
        self._session.flush()
        return entity

    def find_by_id(self, entity_id: str) -> Optional[Asset]:
        orm_obj = self._load_full(str(entity_id))
        return PersistenceMapper.asset_to_domain(orm_obj) if orm_obj else None

    def find_all(self) -> List[Asset]:
        rows = self._session.query(AssetModel).options(
            joinedload(AssetModel.portfolio),
            joinedload(AssetModel.asset_type),
            subqueryload(AssetModel.tags),
            subqueryload(AssetModel.categories).joinedload(CategoryModel.parent),
        ).all()
        return [PersistenceMapper.asset_to_domain(r) for r in rows]

    def delete(self, entity_id: str) -> bool:
        orm_obj = self._session.query(AssetModel).filter(
            AssetModel.id == str(entity_id)
        ).first()
        if orm_obj:
            self._session.delete(orm_obj)
            self._session.flush()
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        entity_id = str(entity_id)
        return self._session.query(
            self._session.query(AssetModel).filter(AssetModel.id == entity_id).exists()
        ).scalar()

    def find_by_portfolio(self, portfolio_id: str) -> List[Asset]:
        rows = self._session.query(AssetModel).options(
            joinedload(AssetModel.portfolio),
            joinedload(AssetModel.asset_type),
            subqueryload(AssetModel.tags),
            subqueryload(AssetModel.categories).joinedload(CategoryModel.parent),
        ).filter(AssetModel.portfolio_id == str(portfolio_id)).all()
        return [PersistenceMapper.asset_to_domain(r) for r in rows]

    def find_by_type(self, asset_type_code: str) -> List[Asset]:
        rows = self._session.query(AssetModel).options(
            joinedload(AssetModel.portfolio),
            joinedload(AssetModel.asset_type),
        ).filter(AssetModel.asset_type.has(code=asset_type_code)).all()
        return [PersistenceMapper.asset_to_domain(r) for r in rows]

    def find_by_category(self, category_id: str) -> List[Asset]:
        rows = self._session.query(AssetModel).options(
            joinedload(AssetModel.portfolio),
            joinedload(AssetModel.asset_type),
        ).join(AssetModel.categories).filter(CategoryModel.id == str(category_id)).all()
        return [PersistenceMapper.asset_to_domain(r) for r in rows]

    def find_by_tag(self, tag_id: str) -> List[Asset]:
        rows = self._session.query(AssetModel).options(
            joinedload(AssetModel.portfolio),
            joinedload(AssetModel.asset_type),
        ).join(AssetModel.tags).filter(TagModel.id == str(tag_id)).all()
        return [PersistenceMapper.asset_to_domain(r) for r in rows]

    def find_active(self, portfolio_id: str) -> List[Asset]:
        rows = self._session.query(AssetModel).options(
            joinedload(AssetModel.portfolio),
            joinedload(AssetModel.asset_type),
        ).filter(
            AssetModel.portfolio_id == str(portfolio_id),
            AssetModel.disposed == False,
        ).all()
        return [PersistenceMapper.asset_to_domain(r) for r in rows]

    def find_disposed(self, portfolio_id: str) -> List[Asset]:
        rows = self._session.query(AssetModel).options(
            joinedload(AssetModel.portfolio),
            joinedload(AssetModel.asset_type),
        ).filter(
            AssetModel.portfolio_id == str(portfolio_id),
            AssetModel.disposed == True,
        ).all()
        return [PersistenceMapper.asset_to_domain(r) for r in rows]

    def find_with_snapshots(
        self,
        asset_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Optional[Asset]:
        from app.adapters.outgoing.persistence.models import AssetSnapshotModel

        orm_obj = self._load_full(str(asset_id))
        if not orm_obj:
            return None

        snapshot_query = self._session.query(AssetSnapshotModel).filter(
            AssetSnapshotModel.asset_id == str(asset_id)
        )
        if start_date:
            snapshot_query = snapshot_query.filter(AssetSnapshotModel.observed_at >= start_date)
        if end_date:
            snapshot_query = snapshot_query.filter(AssetSnapshotModel.observed_at <= end_date)

        orm_obj.snapshots = snapshot_query.all()

        domain_asset = PersistenceMapper.asset_to_domain(orm_obj, load_snapshots=True)
        return domain_asset

    def add_category(self, asset_id: str, category_id: str) -> bool:
        asset = self._session.query(AssetModel).options(
            joinedload(AssetModel.categories)
        ).filter(AssetModel.id == str(asset_id)).first()
        if asset:
            if category_id in {c.id for c in asset.categories}:
                return True
            cat = self._session.query(CategoryModel).filter(
                CategoryModel.id == str(category_id)
            ).first()
            if cat:
                asset.categories.append(cat)
                self._session.flush()
                return True
        return False

    def remove_category(self, asset_id: str, category_id: str) -> bool:
        asset = self._session.query(AssetModel).options(
            joinedload(AssetModel.categories)
        ).filter(AssetModel.id == str(asset_id)).first()
        if asset:
            cat = next((c for c in asset.categories if c.id == str(category_id)), None)
            if cat:
                asset.categories.remove(cat)
                self._session.flush()
                return True
        return False

    def add_tag(self, asset_id: str, tag_id: str) -> bool:
        asset = self._session.query(AssetModel).options(
            joinedload(AssetModel.tags)
        ).filter(AssetModel.id == str(asset_id)).first()
        if asset:
            if str(tag_id) not in {t.id for t in asset.tags}:
                tag = self._session.query(TagModel).filter(
                    TagModel.id == str(tag_id)
                ).first()
                if not tag:
                    return False
                asset.tags.append(tag)
                self._session.flush()
            return True
        return False

    def remove_tag(self, asset_id: str, tag_id: str) -> bool:
        asset = self._session.query(AssetModel).options(
            joinedload(AssetModel.tags)
        ).filter(AssetModel.id == str(asset_id)).first()
        if asset:
            tag = next((t for t in asset.tags if t.id == str(tag_id)), None)
            if tag:
                asset.tags.remove(tag)
                self._session.flush()
                return True
        return False
