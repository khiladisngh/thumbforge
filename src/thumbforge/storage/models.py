"""SQLAlchemy 2.0 ORM models for thumbforge persistence (PLAN.md §3, ADR 0004)."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Text,
    UniqueConstraint,
    event,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Mapper,
    mapped_column,
    relationship,
)

from thumbforge.core.ids import new_id


def utcnow_iso() -> str:
    """Return the current UTC timestamp formatted as ISO-8601 string."""
    return datetime.now(UTC).isoformat()


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Base class for all thumbforge declarative ORM models."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


@event.listens_for(Base, "before_insert", propagate=True)
def _set_created_and_updated_at(_mapper: Mapper[Any], _connection: Any, target: Any) -> None:
    now = utcnow_iso()
    if getattr(target, "id", None) is None:
        target.id = new_id()
    if getattr(target, "created_at", None) is None:
        target.created_at = now
    if getattr(target, "updated_at", None) is None:
        target.updated_at = now


@event.listens_for(Base, "before_update", propagate=True)
def _set_updated_at(_mapper: Mapper[Any], _connection: Any, target: Any) -> None:
    target.updated_at = utcnow_iso()


class ChannelSource(StrEnum):
    """Origin of channel metadata."""

    YTDLP = "ytdlp"
    API = "api"


class RunKind(StrEnum):
    """Lifecycle classification of a generation run."""

    HERO = "hero"
    ITERATE = "iterate"
    BATCH = "batch"


class RunStatus(StrEnum):
    """Execution status for runs and iterations."""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AssetKind(StrEnum):
    """Functional role of a stored image asset."""

    RAW = "raw"
    FINAL = "final"
    REFERENCE = "reference"
    PREVIEW = "preview"


class Channel(Base):
    """A YouTube channel that owns playlists and videos."""

    __tablename__ = "channel"
    __table_args__ = (CheckConstraint("source IN ('ytdlp', 'api')", name="ck_channel_source"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    youtube_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    fetched_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    created_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    updated_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    playlists: Mapped[list[Playlist]] = relationship(
        back_populates="channel", passive_deletes="all"
    )
    videos: Mapped[list[Video]] = relationship(back_populates="channel", passive_deletes="all")


class Playlist(Base):
    """A YouTube playlist containing videos in a defined order."""

    __tablename__ = "playlist"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    youtube_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    channel_id: Mapped[str] = mapped_column(
        String, ForeignKey("channel.id", ondelete="RESTRICT"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    url: Mapped[str] = mapped_column(String, nullable=False)
    item_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    fetched_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    created_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    updated_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)

    channel: Mapped[Channel] = relationship(back_populates="playlists")
    items: Mapped[list[PlaylistItem]] = relationship(
        back_populates="playlist", cascade="all, delete-orphan"
    )
    runs: Mapped[list[Run]] = relationship(back_populates="playlist", passive_deletes="all")


class Video(Base):
    """A YouTube video tracked for thumbnail generation."""

    __tablename__ = "video"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    youtube_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    channel_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("channel.id", ondelete="RESTRICT"), nullable=True
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    duration_s: Mapped[int | None] = mapped_column(Integer, nullable=True)
    published_at: Mapped[str | None] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    source_thumbnail_url: Mapped[str | None] = mapped_column(String, nullable=True)
    fetched_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    created_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    updated_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)

    channel: Mapped[Channel | None] = relationship(back_populates="videos")
    playlist_items: Mapped[list[PlaylistItem]] = relationship(
        back_populates="video", passive_deletes="all"
    )
    runs: Mapped[list[Run]] = relationship(back_populates="video", passive_deletes="all")
    iterations: Mapped[list[Iteration]] = relationship(
        back_populates="video", passive_deletes="all"
    )


class PlaylistItem(Base):
    """Link between a playlist and a video with sequence and part numbering."""

    __tablename__ = "playlist_item"
    __table_args__ = (
        UniqueConstraint("playlist_id", "video_id", name="uq_playlist_item_playlist_video"),
        UniqueConstraint("playlist_id", "position", name="uq_playlist_item_playlist_position"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    playlist_id: Mapped[str] = mapped_column(
        String, ForeignKey("playlist.id", ondelete="CASCADE"), nullable=False
    )
    video_id: Mapped[str] = mapped_column(
        String, ForeignKey("video.id", ondelete="RESTRICT"), nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    part_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    part_label: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    updated_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)

    playlist: Mapped[Playlist] = relationship(back_populates="items")
    video: Mapped[Video] = relationship(back_populates="playlist_items")


class Template(Base):
    """Versioned thumbnail layout specification and Jinja prompt template."""

    __tablename__ = "template"
    __table_args__ = (UniqueConstraint("name", "version", name="uq_template_name_version"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    prompt_template: Mapped[str] = mapped_column(Text, nullable=False)
    layout_spec_json: Mapped[str] = mapped_column(Text, nullable=False)
    spec_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_builtin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    updated_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    runs: Mapped[list[Run]] = relationship(back_populates="template", passive_deletes="all")


class ProviderProfile(Base):
    """Snapshot of provider identity and parameters used by runs."""

    __tablename__ = "provider_profile"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    provider_key: Mapped[str] = mapped_column(String, nullable=False)
    provider_version: Mapped[str] = mapped_column(String, nullable=False)
    params_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    updated_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    runs: Mapped[list[Run]] = relationship(back_populates="provider_profile", passive_deletes="all")


class Run(Base):
    """A batch or hero execution that produces thumbnail iterations."""

    __tablename__ = "run"
    __table_args__ = (
        CheckConstraint("kind IN ('hero', 'iterate', 'batch')", name="ck_run_kind"),
        CheckConstraint(
            "status IN ('pending', 'running', 'paused', 'completed', 'failed', 'cancelled')",
            name="ck_run_status",
        ),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    kind: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    template_id: Mapped[str] = mapped_column(
        String, ForeignKey("template.id", ondelete="RESTRICT"), nullable=False
    )
    provider_profile_id: Mapped[str] = mapped_column(
        String, ForeignKey("provider_profile.id", ondelete="RESTRICT"), nullable=False
    )
    video_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("video.id", ondelete="RESTRICT"), nullable=True
    )
    playlist_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("playlist.id", ondelete="RESTRICT"), nullable=True
    )
    reference_asset_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("asset.id", ondelete="RESTRICT"), nullable=True
    )
    parent_run_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("run.id", ondelete="RESTRICT"), nullable=True
    )
    params_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    started_at: Mapped[str | None] = mapped_column(String, nullable=True)
    finished_at: Mapped[str | None] = mapped_column(String, nullable=True)
    error_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    updated_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)

    template: Mapped[Template] = relationship(back_populates="runs")
    provider_profile: Mapped[ProviderProfile] = relationship(back_populates="runs")
    video: Mapped[Video | None] = relationship(back_populates="runs")
    playlist: Mapped[Playlist | None] = relationship(back_populates="runs")
    reference_asset: Mapped[Asset | None] = relationship(foreign_keys=[reference_asset_id])
    parent_run: Mapped[Run | None] = relationship(
        remote_side="Run.id",
        back_populates="child_runs",
        foreign_keys=[parent_run_id],
    )
    child_runs: Mapped[list[Run]] = relationship(
        back_populates="parent_run",
        foreign_keys=[parent_run_id],
        passive_deletes="all",
    )
    iterations: Mapped[list[Iteration]] = relationship(
        back_populates="run", cascade="all, delete-orphan"
    )


class Iteration(Base):
    """One generated thumbnail attempt slot."""

    __tablename__ = "iteration"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'running', 'paused', 'completed', 'failed', 'cancelled')",
            name="ck_iteration_status",
        ),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    run_id: Mapped[str] = mapped_column(
        String, ForeignKey("run.id", ondelete="CASCADE"), nullable=False
    )
    video_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("video.id", ondelete="RESTRICT"), nullable=True
    )
    ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    seed: Mapped[int | None] = mapped_column(Integer, nullable=True)
    raw_asset_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("asset.id", ondelete="RESTRICT"), nullable=True
    )
    final_asset_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("asset.id", ondelete="RESTRICT"), nullable=True
    )
    picked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    provider_request_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    provider_response_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    started_at: Mapped[str | None] = mapped_column(String, nullable=True)
    finished_at: Mapped[str | None] = mapped_column(String, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cost_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    updated_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)

    run: Mapped[Run] = relationship(back_populates="iterations")
    video: Mapped[Video | None] = relationship(back_populates="iterations")
    raw_asset: Mapped[Asset | None] = relationship(foreign_keys=[raw_asset_id])
    final_asset: Mapped[Asset | None] = relationship(foreign_keys=[final_asset_id])


class Asset(Base):
    """Content-addressed image file stored in the local asset directory."""

    __tablename__ = "asset"
    __table_args__ = (
        CheckConstraint(
            "kind IN ('raw', 'final', 'reference', 'preview')",
            name="ck_asset_kind",
        ),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    sha256: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    rel_path: Mapped[str] = mapped_column(String, nullable=False)
    mime: Mapped[str] = mapped_column(String, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    kind: Mapped[str] = mapped_column(String, nullable=False)
    compliant: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    compliance_report_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    updated_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
