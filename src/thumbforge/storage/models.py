"""SQLAlchemy 2.0 ORM models for thumbforge persistence (PLAN.md §3, ADR 0004)."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import (
    Enum as sa_Enum,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from thumbforge.core.enums import AssetKind, ChannelSource, RunKind, RunStatus
from thumbforge.core.ids import new_id


def utcnow_iso() -> str:
    """Return the current UTC timestamp formatted as ISO-8601 string."""
    return datetime.now(UTC).isoformat()


def _enum_values[E: Enum](enum_cls: type[E]) -> list[str]:
    """Extract serialized string values from an Enum class."""
    return [str(e.value) for e in enum_cls]


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


_CHANNEL_SOURCES = ", ".join(repr(s.value) for s in ChannelSource)
_RUN_KINDS = ", ".join(repr(k.value) for k in RunKind)
_RUN_STATUSES = ", ".join(repr(s.value) for s in RunStatus)
_ASSET_KINDS = ", ".join(repr(k.value) for k in AssetKind)


class Channel(Base):
    """A YouTube channel that owns playlists and videos."""

    __tablename__ = "channel"
    __table_args__ = (CheckConstraint(f"source IN ({_CHANNEL_SOURCES})", name="source"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    youtube_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[ChannelSource] = mapped_column(
        sa_Enum(
            ChannelSource,
            native_enum=False,
            create_constraint=False,
            values_callable=_enum_values,
        ),
        nullable=False,
    )
    fetched_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    created_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, default=utcnow_iso, onupdate=utcnow_iso
    )

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
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, default=utcnow_iso, onupdate=utcnow_iso
    )

    channel: Mapped[Channel] = relationship(back_populates="playlists")
    items: Mapped[list[PlaylistItem]] = relationship(
        back_populates="playlist", cascade="all, delete-orphan", passive_deletes=True
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
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, default=utcnow_iso, onupdate=utcnow_iso
    )

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
        UniqueConstraint("playlist_id", "video_id", name="playlist_video"),
        UniqueConstraint("playlist_id", "position", name="playlist_position"),
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
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, default=utcnow_iso, onupdate=utcnow_iso
    )

    playlist: Mapped[Playlist] = relationship(back_populates="items")
    video: Mapped[Video] = relationship(back_populates="playlist_items")


class Template(Base):
    """Versioned thumbnail layout specification and Jinja prompt template."""

    __tablename__ = "template"
    __table_args__ = (UniqueConstraint("name", "version", name="name_version"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    prompt_template: Mapped[str] = mapped_column(Text, nullable=False)
    layout_spec_json: Mapped[str] = mapped_column(Text, nullable=False)
    spec_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_builtin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, default=utcnow_iso, onupdate=utcnow_iso
    )

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
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, default=utcnow_iso, onupdate=utcnow_iso
    )

    runs: Mapped[list[Run]] = relationship(back_populates="provider_profile", passive_deletes="all")


class Run(Base):
    """A batch or hero execution that produces thumbnail iterations."""

    __tablename__ = "run"
    __table_args__ = (
        CheckConstraint(f"kind IN ({_RUN_KINDS})", name="kind"),
        CheckConstraint(f"status IN ({_RUN_STATUSES})", name="status"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    kind: Mapped[RunKind] = mapped_column(
        sa_Enum(
            RunKind,
            native_enum=False,
            create_constraint=False,
            values_callable=_enum_values,
        ),
        nullable=False,
    )
    status: Mapped[RunStatus] = mapped_column(
        sa_Enum(
            RunStatus,
            native_enum=False,
            create_constraint=False,
            values_callable=_enum_values,
        ),
        nullable=False,
    )
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
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, default=utcnow_iso, onupdate=utcnow_iso
    )

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
        back_populates="run", cascade="all, delete-orphan", passive_deletes=True
    )


class Iteration(Base):
    """One generated thumbnail attempt slot."""

    __tablename__ = "iteration"
    __table_args__ = (CheckConstraint(f"status IN ({_RUN_STATUSES})", name="status"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    run_id: Mapped[str] = mapped_column(
        String, ForeignKey("run.id", ondelete="CASCADE"), nullable=False
    )
    video_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("video.id", ondelete="RESTRICT"), nullable=True
    )
    ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    status: Mapped[RunStatus] = mapped_column(
        sa_Enum(
            RunStatus,
            native_enum=False,
            create_constraint=False,
            values_callable=_enum_values,
        ),
        nullable=False,
    )
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
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, default=utcnow_iso, onupdate=utcnow_iso
    )

    run: Mapped[Run] = relationship(back_populates="iterations")
    video: Mapped[Video | None] = relationship(back_populates="iterations")
    raw_asset: Mapped[Asset | None] = relationship(foreign_keys=[raw_asset_id])
    final_asset: Mapped[Asset | None] = relationship(foreign_keys=[final_asset_id])


class Asset(Base):
    """Content-addressed image file stored in the local asset directory."""

    __tablename__ = "asset"
    __table_args__ = (CheckConstraint(f"kind IN ({_ASSET_KINDS})", name="kind"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=new_id)
    sha256: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    rel_path: Mapped[str] = mapped_column(String, nullable=False)
    mime: Mapped[str] = mapped_column(String, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    kind: Mapped[AssetKind] = mapped_column(
        sa_Enum(
            AssetKind,
            native_enum=False,
            create_constraint=False,
            values_callable=_enum_values,
        ),
        nullable=False,
    )
    compliant: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    compliance_report_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False, default=utcnow_iso)
    updated_at: Mapped[str] = mapped_column(
        String, nullable=False, default=utcnow_iso, onupdate=utcnow_iso
    )
