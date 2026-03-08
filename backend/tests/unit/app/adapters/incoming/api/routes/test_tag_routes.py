"""Unit tests for tag routes."""
from unittest.mock import MagicMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.adapters.incoming.api.dependencies.tags import (
    get_all_tags_use_case,
    create_tag_use_case,
    get_tag_use_case,
)
from app.domain.exceptions import TagNotFound, DuplicateName


def make_tag(name="test-tag"):
    tag = MagicMock()
    tag.id = uuid4()
    tag.name = name
    return tag


def test_get_all_tags():
    mock_use_case = MagicMock()
    mock_use_case.execute.return_value = []
    app.dependency_overrides[get_all_tags_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.get('/api/v1/tags/')
        assert resp.status_code == 200
        assert resp.json() == []
    finally:
        app.dependency_overrides.clear()


def test_create_tag():
    mock_use_case = MagicMock()
    mock_use_case.execute.return_value = make_tag("test-tag")
    app.dependency_overrides[create_tag_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.post('/api/v1/tags/', json={"name": "test-tag"})
        assert resp.status_code == 201
        assert resp.json()['name'] == 'test-tag'
    finally:
        app.dependency_overrides.clear()


def test_create_tag_duplicate():
    mock_use_case = MagicMock()
    mock_use_case.execute.side_effect = DuplicateName("Tag already exists")
    app.dependency_overrides[create_tag_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.post('/api/v1/tags/', json={"name": "test-tag"})
        assert resp.status_code == 409
        assert resp.json()['code'] == 'DUPLICATE_NAME'
    finally:
        app.dependency_overrides.clear()


def test_get_tag_not_found():
    mock_use_case = MagicMock()
    mock_use_case.execute.side_effect = TagNotFound("Tag not found")
    app.dependency_overrides[get_tag_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.get(f'/api/v1/tags/{uuid4()}')
        assert resp.status_code == 404
        assert resp.json()['code'] == 'TAG_NOT_FOUND'
    finally:
        app.dependency_overrides.clear()
