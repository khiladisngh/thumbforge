"""Unit tests for SQLAlchemy models, constraints, and relationships (PLAN.md §3, ADR 0004)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sqlalchemy.exc import IntegrityError

from thumbforge.storage.db import get_engine, init_db, session_factory, session_scope
from thumbforge.storage.models import (
    Asset,
    AssetKind,
    Channel,
    ChannelSource,
    Iteration,
    Playlist,
    PlaylistItem,
    ProviderProfile,
    Run,
    RunKind,
    RunStatus,
    Template,
    Video,
)

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def db_session(tmp_path: Path):
    db_file = tmp_path / "models.sqlite3"
    init_db(db_file)
    engine = get_engine(db_file)
    factory = session_factory(engine)
    with session_scope(factory) as session:
        yield session
    engine.dispose()


def test_insert_all_nine_models_and_verify_relations(db_session) -> None:
    # 1. Channel
    channel = Channel(
        youtube_id="UC_CHAN_1",
        title="Channel One",
        url="https://youtube.com/@channel1",
        source=ChannelSource.YTDLP,
    )
    db_session.add(channel)
    db_session.flush()

    assert len(channel.id) == 26  # ULID length
    assert channel.created_at is not None
    assert channel.updated_at is not None

    # 2. Playlist
    playlist = Playlist(
        youtube_id="PL_LIST_1",
        channel_id=channel.id,
        title="Playlist One",
        url="https://youtube.com/playlist?list=PL_LIST_1",
        item_count=1,
    )
    db_session.add(playlist)
    db_session.flush()

    # 3. Video
    video = Video(
        youtube_id="VID_1",
        channel_id=channel.id,
        title="Video One",
        url="https://youtube.com/watch?v=VID_1",
        duration_s=360,
    )
    db_session.add(video)
    db_session.flush()

    # 4. PlaylistItem
    item = PlaylistItem(
        playlist_id=playlist.id,
        video_id=video.id,
        position=1,
        part_number=1,
        part_label="Part 1",
    )
    db_session.add(item)
    db_session.flush()

    # 5. Template
    template = Template(
        name="bold-title",
        version=1,
        prompt_template="Create thumbnail for {{ title }}",
        layout_spec_json='{"width": 1920}',
        spec_hash="a1b2c3d4",
        is_builtin=True,
    )
    db_session.add(template)
    db_session.flush()

    # 6. ProviderProfile
    profile = ProviderProfile(
        name="fake_default",
        provider_key="fake",
        provider_version="1.0.0",
        params_json="{}",
    )
    db_session.add(profile)
    db_session.flush()

    # 7. Asset
    asset = Asset(
        sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        rel_path="assets/e3/e3b0c4.png",
        mime="image/png",
        width=1920,
        height=1080,
        bytes=123456,
        kind=AssetKind.FINAL,
        compliant=True,
    )
    db_session.add(asset)
    db_session.flush()

    # 8. Run
    run = Run(
        kind=RunKind.HERO,
        status=RunStatus.PENDING,
        template_id=template.id,
        provider_profile_id=profile.id,
        video_id=video.id,
        reference_asset_id=asset.id,
    )
    db_session.add(run)
    db_session.flush()

    # 9. Iteration
    iteration = Iteration(
        run_id=run.id,
        video_id=video.id,
        ordinal=1,
        idempotency_key="idemp_key_001",
        status=RunStatus.PENDING,
        prompt_text="Create thumbnail",
        final_asset_id=asset.id,
    )
    db_session.add(iteration)
    db_session.flush()

    # Verify relationships navigation
    assert playlist.channel.id == channel.id
    assert channel.playlists[0].id == playlist.id
    assert channel.videos[0].id == video.id
    assert playlist.items[0].video.id == video.id
    assert run.template.id == template.id
    assert run.provider_profile.id == profile.id
    assert run.reference_asset is not None
    assert run.reference_asset.id == asset.id
    assert run.iterations[0].id == iteration.id
    assert iteration.run.id == run.id


def test_check_constraint_channel_source(db_session) -> None:
    channel = Channel(
        youtube_id="UC_BAD",
        title="Bad Channel",
        url="https://youtube.com/@bad",
        source="invalid_source",
    )
    db_session.add(channel)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_check_constraint_run_kind(db_session) -> None:
    template = Template(
        name="t1",
        version=1,
        prompt_template="p",
        layout_spec_json="{}",
        spec_hash="h1",
    )
    profile = ProviderProfile(
        name="p1",
        provider_key="fake",
        provider_version="1.0",
    )
    db_session.add_all([template, profile])
    db_session.flush()

    run = Run(
        kind="invalid_kind",
        status=RunStatus.PENDING,
        template_id=template.id,
        provider_profile_id=profile.id,
    )
    db_session.add(run)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_unique_constraint_channel_youtube_id(db_session) -> None:
    c1 = Channel(
        youtube_id="UC_DUP",
        title="Channel 1",
        url="https://youtube.com/@c1",
        source=ChannelSource.YTDLP,
    )
    c2 = Channel(
        youtube_id="UC_DUP",
        title="Channel 2",
        url="https://youtube.com/@c2",
        source=ChannelSource.YTDLP,
    )
    db_session.add(c1)
    db_session.flush()
    db_session.add(c2)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_unique_constraint_template_name_version(db_session) -> None:
    t1 = Template(
        name="minimal",
        version=1,
        prompt_template="p1",
        layout_spec_json="{}",
        spec_hash="h1",
    )
    t2 = Template(
        name="minimal",
        version=1,
        prompt_template="p2",
        layout_spec_json="{}",
        spec_hash="h2",
    )
    db_session.add(t1)
    db_session.flush()
    db_session.add(t2)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_unique_constraint_playlist_item(db_session) -> None:
    channel = Channel(
        youtube_id="UC_C1",
        title="C1",
        url="https://youtube.com/@c1",
        source=ChannelSource.YTDLP,
    )
    db_session.add(channel)
    db_session.flush()

    playlist = Playlist(
        youtube_id="PL_P1",
        channel_id=channel.id,
        title="P1",
        url="https://youtube.com/playlist?list=PL_P1",
    )
    v1 = Video(
        youtube_id="V_1",
        channel_id=channel.id,
        title="V1",
        url="https://youtube.com/watch?v=V_1",
    )
    v2 = Video(
        youtube_id="V_2",
        channel_id=channel.id,
        title="V2",
        url="https://youtube.com/watch?v=V_2",
    )
    db_session.add_all([playlist, v1, v2])
    db_session.flush()

    # Same position conflict
    item1 = PlaylistItem(playlist_id=playlist.id, video_id=v1.id, position=1)
    item2 = PlaylistItem(playlist_id=playlist.id, video_id=v2.id, position=1)
    db_session.add(item1)
    db_session.flush()
    db_session.add(item2)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_on_delete_restrict_on_parent_run(db_session) -> None:
    template = Template(
        name="t_hero",
        version=1,
        prompt_template="p",
        layout_spec_json="{}",
        spec_hash="h",
    )
    profile = ProviderProfile(
        name="p_hero",
        provider_key="fake",
        provider_version="1.0",
    )
    db_session.add_all([template, profile])
    db_session.flush()

    parent = Run(
        kind=RunKind.HERO,
        status=RunStatus.COMPLETED,
        template_id=template.id,
        provider_profile_id=profile.id,
    )
    db_session.add(parent)
    db_session.flush()

    child = Run(
        kind=RunKind.BATCH,
        status=RunStatus.PENDING,
        template_id=template.id,
        provider_profile_id=profile.id,
        parent_run_id=parent.id,
    )
    db_session.add(child)
    db_session.flush()

    # Deleting parent must fail with IntegrityError because child references it with RESTRICT
    db_session.delete(parent)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_on_delete_restrict_on_reference_asset(db_session) -> None:
    template = Template(
        name="t_ref",
        version=1,
        prompt_template="p",
        layout_spec_json="{}",
        spec_hash="h",
    )
    profile = ProviderProfile(
        name="p_ref",
        provider_key="fake",
        provider_version="1.0",
    )
    asset = Asset(
        sha256="ref_asset_hash",
        rel_path="assets/re/ref.png",
        mime="image/png",
        width=1920,
        height=1080,
        bytes=999,
        kind=AssetKind.REFERENCE,
    )
    db_session.add_all([template, profile, asset])
    db_session.flush()

    run = Run(
        kind=RunKind.BATCH,
        status=RunStatus.PENDING,
        template_id=template.id,
        provider_profile_id=profile.id,
        reference_asset_id=asset.id,
    )
    db_session.add(run)
    db_session.flush()

    # Deleting referenced asset must fail with IntegrityError
    db_session.delete(asset)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()
