"""
Use Case: Get All Assets
"""
from typing import List

from app.domain.entities.asset import Asset
from app.domain.ports.repository import IAssetRepository


class GetAllAssetsUseCase:
    """
    Use case for retrieving all assets.
    """

    def __init__(self, asset_repository: IAssetRepository):
        self.asset_repository = asset_repository

    def execute(self) -> List[Asset]:
        """
        Fetches all assets.
        """
        return self.asset_repository.find_all()
