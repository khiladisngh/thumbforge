"""Configuration precedence, validation and the secrets prohibition."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from thumbforge.core.errors import SettingsError
from thumbforge.settings import (
    ConfigSchema,
    default_config_path,
    default_config_toml,
    load_settings,
    set_values,
    write_default_config,
)

if TYPE_CHECKING:
    from pathlib import Path


def write_config(path: Path, body: str) -> Path:
    path.write_text(body, encoding="utf-8")
    return path


def test_user_directories_are_isolated_from_the_real_machine(
    isolate_user_environment: Path,
) -> None:
    """Guards the conftest fixture itself: a regression there silently pollutes real dirs.

    ``GeneralSettings.data_dir`` binds its default factory at class-definition time, so
    patching ``settings.default_data_dir`` would not take effect; the fixture patches
    platformdirs instead, and this asserts that it actually works.
    """
    settings = load_settings(config_path=None)
    assert isolate_user_environment in settings.general.data_dir.parents
    assert isolate_user_environment in settings.state_dir.parents
    assert isolate_user_environment in default_config_path().parents


def test_defaults_apply_when_no_file_exists(tmp_path: Path) -> None:
    settings = load_settings(config_path=tmp_path / "absent.toml")
    assert settings.output.width == 1920
    assert settings.general.default_provider == "fake"
    assert settings.logging.format == "console"


def test_file_overrides_defaults(tmp_path: Path) -> None:
    config = write_config(
        tmp_path / "config.toml",
        "[output]\nwidth = 1280\nheight = 720\n",
    )
    settings = load_settings(config_path=config)
    assert (settings.output.width, settings.output.height) == (1280, 720)
    assert settings.output.quality == 90  # untouched keys keep their default


def test_environment_overrides_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config = write_config(tmp_path / "config.toml", "[output]\nquality = 70\n")
    monkeypatch.setenv("THUMBFORGE_OUTPUT__QUALITY", "55")
    assert load_settings(config_path=config).output.quality == 55


def test_data_dir_flag_overrides_everything(tmp_path: Path) -> None:
    file_dir = (tmp_path / "from-file").as_posix()
    config = write_config(tmp_path / "config.toml", f'[general]\ndata_dir = "{file_dir}"\n')
    override = tmp_path / "from-flag"
    settings = load_settings(config_path=config, data_dir=override)
    assert settings.general.data_dir == override
    assert settings.db_path == override / "thumbforge.sqlite3"
    assert settings.assets_dir == override / "assets"


@pytest.mark.parametrize(
    "body",
    [
        '[providers.openai]\napi_key = "sk-secret"\n',
        '[providers.openai]\naccess_token = "t"\n',
        '[general]\nclient_secret = "s"\n',
    ],
)
def test_secret_looking_keys_are_rejected(tmp_path: Path, body: str) -> None:
    config = write_config(tmp_path / "config.toml", body)
    with pytest.raises(SettingsError) as caught:
        load_settings(config_path=config)
    assert caught.value.exit_code == 2
    assert caught.value.hint is not None
    assert "keyring" in caught.value.hint


def test_unknown_key_is_rejected_rather_than_ignored(tmp_path: Path) -> None:
    config = write_config(tmp_path / "config.toml", "[output]\nwidht = 1280\n")
    with pytest.raises(SettingsError, match="widht"):
        load_settings(config_path=config)


def test_malformed_toml_reports_the_file(tmp_path: Path) -> None:
    config = write_config(tmp_path / "config.toml", "[output\nwidth = 1280\n")
    with pytest.raises(SettingsError, match="not valid TOML"):
        load_settings(config_path=config)


def test_non_16_9_output_is_rejected() -> None:
    with pytest.raises(ValueError, match="16:9"):
        ConfigSchema(output={"width": 1920, "height": 1000})  # pyright: ignore[reportArgumentType]


def test_linked_keys_can_be_set_together(tmp_path: Path) -> None:
    """width and height must change in one call; neither halfway state is 16:9."""
    config = write_config(tmp_path / "config.toml", "[output]\nwidth = 1920\nheight = 1080\n")
    set_values(config, {"output.width": "1280", "output.height": "720"})
    settings = load_settings(config_path=config)
    assert (settings.output.width, settings.output.height) == (1280, 720)


def test_rejected_edit_leaves_the_file_untouched(tmp_path: Path) -> None:
    original = "[output]\nwidth = 1920\nheight = 1080\n"
    config = write_config(tmp_path / "config.toml", original)
    with pytest.raises(SettingsError):
        set_values(config, {"output.width": "1280"})  # 1280x1080 is not 16:9
    assert config.read_text(encoding="utf-8") == original


def test_values_are_parsed_as_toml_scalars_not_strings(tmp_path: Path) -> None:
    config = tmp_path / "config.toml"
    set_values(config, {"output.quality": "85", "providers.antigravity.skip_permissions": "false"})
    settings = load_settings(config_path=config)
    assert settings.output.quality == 85
    assert settings.providers.antigravity.skip_permissions is False


def test_setting_a_secret_key_is_refused(tmp_path: Path) -> None:
    config = tmp_path / "config.toml"
    with pytest.raises(SettingsError, match="secret-looking"):
        set_values(config, {"providers.openai.api_key": '"sk-x"'})
    assert not config.exists()


def test_dotted_key_must_name_a_section(tmp_path: Path) -> None:
    with pytest.raises(SettingsError, match="dotted key"):
        set_values(tmp_path / "config.toml", {"width": "1280"})


def test_init_defaults_ignore_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """A generated config must contain defaults, not whatever the current shell exports."""
    monkeypatch.setenv("THUMBFORGE_OUTPUT__QUALITY", "33")
    rendered = default_config_toml()
    assert "quality = 90" in rendered
    assert "quality = 33" not in rendered


def test_environment_cannot_mask_an_invalid_file_value(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A valid env override must not let an invalid assignment be written to disk."""
    config = tmp_path / "config.toml"
    monkeypatch.setenv("THUMBFORGE_OUTPUT__QUALITY", "80")
    with pytest.raises(SettingsError):
        set_values(config, {"output.quality": "500"})  # out of range regardless of the env
    assert not config.exists()


def test_write_is_atomic_and_leaves_no_temp_files(tmp_path: Path) -> None:
    config = tmp_path / "config.toml"
    write_default_config(config)
    set_values(config, {"output.quality": "75"})
    siblings = {p.name for p in tmp_path.iterdir()}
    assert siblings == {"config.toml"}, f"temp files left behind: {siblings}"


def test_write_default_config_refuses_to_clobber(tmp_path: Path) -> None:
    config = tmp_path / "config.toml"
    write_default_config(config)
    config.write_text("[output]\nquality = 60\n", encoding="utf-8")

    with pytest.raises(SettingsError, match="already exists"):
        write_default_config(config)
    assert "quality = 60" in config.read_text(encoding="utf-8")

    write_default_config(config, force=True)
    assert "quality = 90" in config.read_text(encoding="utf-8")
