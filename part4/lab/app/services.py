"""In-memory notes service used by the hook practice tests."""

from __future__ import annotations

type Note = dict[str, int | str]


class NotesService:
    def __init__(self) -> None:
        self._notes: dict[int, Note] = {}
        self._next_id = 1

    def create(self, title: str, body: str) -> Note:
        note_id = self._next_id
        self._next_id += 1
        note: Note = {"id": note_id, "title": title, "body": body}
        self._notes[note_id] = note
        return dict(note)

    def get(self, note_id: int) -> Note | None:
        note = self._notes.get(note_id)
        return dict(note) if note is not None else None

    def search(self, query: str) -> list[Note]:
        needle = query.casefold()
        return [
            dict(note)
            for note in self._notes.values()
            if needle in str(note["title"]).casefold()
            or needle in str(note["body"]).casefold()
        ]
