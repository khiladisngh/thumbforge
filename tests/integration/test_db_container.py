"""Integration tests using Testcontainers for database verification (ADR 0004)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from testcontainers.core.container import DockerContainer

from thumbforge.core.enums import ChannelSource
from thumbforge.storage.db import get_engine, init_db, session_factory, session_scope
from thumbforge.storage.models import Channel

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.integration
def test_sqlite_database_in_container(tmp_path: Path) -> None:
    """Verify that a database initialized on host can be mounted and read in a Linux container."""
    db_file = tmp_path / "container_test.sqlite3"
    init_db(db_file)

    engine = get_engine(db_file)
    factory = session_factory(engine)
    with session_scope(factory) as session:
        session.add(
            Channel(
                youtube_id="UC_CONTAINER_1",
                title="Container Channel",
                url="https://youtube.com/@container",
                source=ChannelSource.YTDLP,
            )
        )
    engine.dispose()

    data_dir_str = str(tmp_path.resolve())
    with (
        DockerContainer("alpine:latest")
        .with_volume_mapping(data_dir_str, "/data", "rw")
        .with_command("tail -f /dev/null")
    ) as container:
        container.exec(["apk", "add", "--no-cache", "sqlite"])
        res = container.exec(
            ["sqlite3", "/data/container_test.sqlite3", "SELECT youtube_id, title FROM channel;"]
        )
        assert res.exit_code == 0
        output = res.output.decode("utf-8")
        assert "UC_CONTAINER_1|Container Channel" in output
