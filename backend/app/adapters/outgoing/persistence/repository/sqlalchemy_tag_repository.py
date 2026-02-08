"""
SQLAlchemy Tag Repository Implementation

Concrete implementation of TagRepository using SQLAlchemy.
"""
from typing import Optional, cast, Any
from sqlalchemy.orm import Session

from app.domain.ports.repository.tag_repository import ITagRepository
from app.adapters.outgoing.persistence.models import TagModel, AssetModel


class SQLAlchemyTagRepository(ITagRepository):
    """
    SQLAlchemy implementation of TagRepository.
    """

    def __init__(self, session: Session):
        """Initialize repository with persistence session."""
        self._session = session

    def save(self, entity: TagModel) -> TagModel:
        """Persist a tag and return the saved entity."""
        self._session.add(entity)
        self._session.flush()
        return entity

    def find_by_id(self, entity_id: str) -> Optional[TagModel]:
        """Find tag by id."""
        return self._session.query(TagModel).filter(TagModel.id == entity_id).first()

    def find_all(self) -> list[TagModel]:
        """Return all tags."""
        return cast(list[TagModel], cast(Any, self._session.query(TagModel).all()))

    def delete(self, entity_id: str) -> bool:
        """Delete tag by id."""
        obj = self.find_by_id(entity_id)
        if obj:
            self._session.delete(obj)
            self._session.flush()
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        """Check existence by id."""
        return self._session.query(
            self._session.query(TagModel).filter(TagModel.id == entity_id).exists()
        ).scalar()

    # Domain / interface-specific methods (keep in same order as the port)
    def find_by_name(self, name: str) -> Optional[TagModel]:
        """Find a tag by its exact name."""
        return self._session.query(TagModel).filter(TagModel.name == name).first()

    def find_by_asset(self, asset_id: str) -> list[TagModel]:
        """Return all tags attached to a given asset."""
        asset = self._session.query(AssetModel).options(
            joinedload(AssetModel.tags)
        ).filter(AssetModel.id == asset_id).first()
        return asset.tags if asset else [] # type: ignore

    def attach_to_asset(self, asset_id: str, tag_id: str) -> bool:
        """Attach an existing tag to an asset."""
        asset = self._session.query(AssetModel).filter(AssetModel.id == asset_id).first()
        tag = self.find_by_id(tag_id)
        if asset and tag and tag not in asset.tags:
            asset.tags.append(tag)
            self._session.flush()
            return True
        return False

    def detach_from_asset(self, asset_id: str, tag_id: str) -> bool:
        """Remove a tag from an asset."""
        asset = self._session.query(AssetModel).options(
            joinedload(AssetModel.tags)
        ).filter(AssetModel.id == asset_id).first()
        tag = self.find_by_id(tag_id)
        if asset and tag and tag in asset.tags:
            asset.tags.remove(tag)
            self._session.flush()
            return True
        return False
