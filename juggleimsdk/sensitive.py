"""Sensitive word API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.util import ApiCode


@dataclass
class SensitiveWord:
    id: str = ""
    word: str = ""
    word_type: int = 0


@dataclass
class SensitiveWords:
    items: Optional[List[SensitiveWord]] = None
    total: int = 0
    is_finished: bool = False


@dataclass
class DelSensitiveWordsReq:
    words: List[str] = field(default_factory=list)


class SensitiveApiMixin:
    def qry_sensitive_words(
        self: HttpClient, size: int, page: int, word: str, word_type: int
    ) -> Tuple[Optional[SensitiveWords], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/sensitivewords/list?size={size}&page={page}&word={word}&word_type={word_type}",
            SensitiveWords,
        )

    def add_sensitive_words(
        self: HttpClient, words: SensitiveWords
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/sensitivewords/add", words)

    def delete_sensitive_words(
        self: HttpClient, req: DelSensitiveWordsReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/sensitivewords/del", req)
