# Spike results — terminal image preview (closed 2026-10-03)

## S10 — `rich-pixels` tiles in a terminal, and the two-column grid

### Environment

- Linux container (WSL2 kernel 6.18), output captured through a pseudo-terminal with `script`, **not** Windows Terminal.
- Python 3.14.7, `rich 15.0.0`, `rich-pixels 3.0.1`, `pillow 12.3.0` (the same versions in the ephemeral `uv run --with` environment and in the project lock).
- The host shell exports `TERM=dumb` and `NO_COLOR=1`; the pty runs reset them to a colour terminal: `TERM=xterm-256color COLORTERM=truecolor COLUMNS=100`, `NO_COLOR` unset, plus `UV_NO_PROGRESS=1` so uv's spinner does not land in the capture.

### Run 1 — the S10 command

- Script (`s10.sh`), the command from `OPEN_QUESTIONS.md` verbatim:
    ```sh
    cd /tmp/s10
    uv run --with rich --with rich-pixels --with pillow python -c "from PIL import Image; from rich.console import Console; from rich_pixels import Pixels; c=Console(); Image.new('RGB',(1920,1080),(200,40,40)).save('preview.png'); w=max(c.width//2-2,20); c.print(Pixels.from_image_path('preview.png',resize=(w,w*9//16)))"
    ```
- Runner: `script -qec /tmp/s10/s10.sh /dev/null > /tmp/s10/s10.out` with the environment above.
- Result: exit `0`; **14 lines, each 48 columns** (`w = 100 // 2 - 2 = 48`, height `48 * 9 // 16 = 27` rounded up to 28 pixels, two pixel rows per line). The only glyph is `▄`; the only SGR codes are `38;2;200;40;40;48;2;200;40;40` (truecolor foreground and background) and the reset `0`. ANSI-stripped excerpt:
    ```text
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    ```

### Run 2 — two tiles through `preview()` versus `rich.columns.Columns`

- Script (`preview_spike.py`, run with `uv run python` in the worktree under the same pty settings): writes a red `(200,40,40)` and a blue `(40,60,200)` 1920×1080 PNG, builds a plain `Console()` so Rich detects the pty itself, then either calls `preview(AppContext(console=console, json_mode=False), [red, blue])` or prints `Columns([Pixels.from_image_path(p, resize=(w, w * 9 // 16)) for p in (red, blue)])` with `w = (console.width - 1) // 2`.
    ```sh
    script -qec "uv run python /tmp/s10/preview_spike.py preview" /dev/null > /tmp/s10/preview.out
    script -qec "uv run python /tmp/s10/preview_spike.py columns" /dev/null > /tmp/s10/columns.out
    ```
- `preview()` (`Table.grid`): **15 lines, each 99 columns**: 14 pixel lines (tile width `(100 - 1) // 2 = 49`, height `round(49 * 1080 / 1920) = 28` pixels) and one caption line. Red (`38;2;200;40;40;48;2;200;40;40`) and blue (`38;2;40;60;200;48;2;40;60;200`) both occupy lines 0–13, **14 of 14 lines shared**, so the tiles sit side by side. The captions use the dim SGR `2`. Excerpt:
    ```text
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    red.png                                           blue.png
    ```
- `Columns`: **28 lines** — red on lines 0–13, blue on lines 14–27, **0 lines shared**; each red line is padded with spaces to the full 100 columns. `Pixels` defines no `__rich_measure__`, so `Columns` measures every tile as full width and puts one per row. This is why `preview` lays tiles out with `Table.grid` (one fixed-width column per tile) and why the unit test asserts that both colours appear on the same lines.

### Run 3 — the fallback in the host's own terminal settings

- Same `preview()` call with `TERM=dumb NO_COLOR=1` (`script -qec … > /tmp/s10/fallback.out`).
- Result: no SGR codes and no half-block glyphs; a numbered `# | path` table listing `/tmp/s10/red.png` and `/tmp/s10/blue.png`, then `Copy images out with: thumbforge thumb export <run|iteration> --to PATH`.

### Verdict

- `rich-pixels` produces correctly sized truecolor half-block tiles under a pty, and `Table.grid` gives a real two-column grid. P5.4 ships `preview()` on that basis, with the path-table fallback for consoles that cannot show colour and for unreadable images.
- **Not verified:** legibility in Windows Terminal (that a real thumbnail's title and composition are recognisable). That is a manual check, listed as the `thumb show` acceptance criterion (Phase 5 spec, implemented in P6.x), and it was **not** performed for this spike; only synthetic solid-colour tiles were rendered.
