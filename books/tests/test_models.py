# Django
from django.db.utils import IntegrityError

# Third Party
import pytest

# Locals
from ..models import Author, FailedScan, SyncMetadata, SyncSetting


@pytest.mark.django_db
def test_author_unique_constraint(user, another_user):
    Author.objects.create(name="Unique Author", owner=user)
    Author.objects.create(name="Unique Author", owner=another_user)

    with pytest.raises(IntegrityError):
        Author.objects.create(name="Unique Author", owner=user)


@pytest.mark.django_db
def test_author_creation(user):
    author = Author.objects.create(name="Jane Doe", owner=user)
    assert author.name == "Jane Doe"
    assert author.owner == user


@pytest.mark.django_db
def test_author_str(author):
    assert str(author) == "John Doe"


@pytest.mark.django_db
def test_failed_scan_creation(user):
    failed_scan = FailedScan.objects.create(isbn="0987654321", owner=user)
    assert failed_scan.isbn == "0987654321"
    assert failed_scan.owner == user


@pytest.mark.django_db
def test_failed_scan_unique_constraint(user, another_user):
    FailedScan.objects.create(isbn="1234567890", owner=user)
    FailedScan.objects.create(isbn="1234567890", owner=another_user)

    with pytest.raises(IntegrityError):
        FailedScan.objects.create(isbn="1234567890", owner=user)


@pytest.mark.django_db
def test_failed_scan_str(failed_scan):
    assert str(failed_scan) == "1234567890"


@pytest.mark.django_db
def test_sync_setting_unique_constraint(user, another_user):
    SyncSetting.objects.create(
        owner=user, server="test_server", database="test_database", username="test_user", password="test_password"
    )
    SyncSetting.objects.create(
        owner=another_user,
        server="test_server",
        database="test_database",
        username="test_user",
        password="test_password",
    )
    with pytest.raises(IntegrityError):
        SyncSetting.objects.create(
            owner=user,
            server="test_server",
            database="test_database",
            username="another_user",
            password="another_password",
        )


@pytest.mark.django_db
def test_sync_setting_str(sync_setting):
    assert str(sync_setting) == f"{sync_setting.server}/{sync_setting.database}"


@pytest.mark.django_db
def test_sync_setting_connection_string(sync_setting):
    expected_connection_string = f"https://{sync_setting.username}:{sync_setting.password}@{sync_setting.server}"
    assert sync_setting.connection_string() == expected_connection_string


@pytest.mark.django_db
def test_sync_metadata_creation(user, sync_setting, book):
    sync_metadata = SyncMetadata.objects.create(
        owner=user, server=sync_setting, book=book, _id="test_id", _rev="test_rev"
    )
    assert sync_metadata.owner == user
    assert sync_metadata.server == sync_setting
    assert sync_metadata.book == book
    assert sync_metadata._id == "test_id"
    assert sync_metadata._rev == "test_rev"


@pytest.mark.django_db
def test_sync_metadata_str(sync_metadata):
    assert str(sync_metadata) == "test_id - test_rev"


@pytest.mark.django_db
def test_sync_metadata_ensure(user, sync_setting):
    sync_metadata = SyncMetadata.ensure(id="test_id", rev="new_rev", server=sync_setting)
    assert sync_metadata is not None
    assert sync_metadata._id == "test_id"
    assert sync_metadata._rev == "new_rev"
    assert sync_metadata.server == sync_setting
    assert sync_metadata.owner == sync_setting.owner
