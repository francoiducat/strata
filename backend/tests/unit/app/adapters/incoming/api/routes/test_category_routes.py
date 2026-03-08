"""Unit tests for category routes."""
from unittest.mock import MagicMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.adapters.incoming.api.dependencies.categories import (
    get_all_categories_use_case,
    create_category_use_case,
    get_category_use_case,
    delete_category_use_case,
)
from app.domain.exceptions import CategoryNotFound, CategoryHasChildren, DuplicateName


def make_category(name="Test"):
    cat = MagicMock()
    cat.id = uuid4()
    cat.name = name
    cat.parent_id = None
    return cat


def test_get_all_categories():
    mock_use_case = MagicMock()
    mock_use_case.execute.return_value = []
    app.dependency_overrides[get_all_categories_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.get('/api/v1/categories/')
        assert resp.status_code == 200
        assert resp.json() == []
    finally:
        app.dependency_overrides.clear()


def test_create_category():
    mock_use_case = MagicMock()
    mock_use_case.execute.return_value = make_category("Test")
    app.dependency_overrides[create_category_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.post('/api/v1/categories/', json={"name": "Test"})
        assert resp.status_code == 201
        assert resp.json()['name'] == 'Test'
    finally:
        app.dependency_overrides.clear()


def test_get_category_not_found():
    mock_use_case = MagicMock()
    mock_use_case.execute.side_effect = CategoryNotFound("Category not found")
    app.dependency_overrides[get_category_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.get(f'/api/v1/categories/{uuid4()}')
        assert resp.status_code == 404
        assert resp.json()['code'] == 'CATEGORY_NOT_FOUND'
    finally:
        app.dependency_overrides.clear()


def test_delete_category_has_children():
    mock_use_case = MagicMock()
    mock_use_case.execute.side_effect = CategoryHasChildren("Category has children")
    app.dependency_overrides[delete_category_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.delete(f'/api/v1/categories/{uuid4()}')
        assert resp.status_code == 409
        assert resp.json()['code'] == 'CATEGORY_HAS_CHILDREN'
    finally:
        app.dependency_overrides.clear()
