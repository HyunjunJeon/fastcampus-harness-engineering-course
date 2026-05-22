"""개발자 트랙용 기본 테스트. 검색 기능은 강의 중 추가/수정합니다."""

from __future__ import annotations

from app.services import NotesService


def test_create_and_get() -> None:
    service = NotesService()
    created = service.create(title="hello", body="world")
    assert service.get(created["id"]) == created


def test_search_is_case_insensitive() -> None:
    service = NotesService()
    service.create(title="Hello", body="Whatever")
    assert len(service.search("hello")) == 1
    assert len(service.search("HELLO")) == 1


def test_search_matches_body() -> None:
    service = NotesService()
    service.create(title="random", body="contains the word Note inside")
    assert len(service.search("note")) == 1
