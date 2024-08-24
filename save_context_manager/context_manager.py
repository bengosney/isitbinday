# Standard Library
from types import TracebackType
from typing import Self


class SaveContextManagerMixin:
    def save(self) -> bool:
        raise NotImplementedError("save method is not implemented")

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if exc_type is None:
            return self.save()
        return False
