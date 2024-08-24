# Third Party
import pytest

# Locals
from . import SaveContextManagerMixin


class MockSaveContextManager(SaveContextManagerMixin):
    def save(self):
        return True


def test_calls_save(mocker):
    save = mocker.spy(MockSaveContextManager, "save")

    with MockSaveContextManager():
        pass

    save.assert_called_once()


def test_calls_save_with_exception(mocker):
    save = mocker.spy(MockSaveContextManager, "save")

    with pytest.raises(Exception):
        with MockSaveContextManager():
            raise Exception

    save.assert_not_called()
