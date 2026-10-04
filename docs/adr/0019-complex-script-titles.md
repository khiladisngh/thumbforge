# ADR 0019: Complex-script titles: HarfBuzz shaping and a bundled fallback font

## Status

`Accepted` — 2026-10-04

Extends [ADR 0007](0007-pillow-imaging.md) and [ADR 0008](0008-deterministic-text-overlay.md); neither is superseded. Pillow still draws every pixel with the BASIC layout engine, the fonts are still bundled, and the goldens still compare exact pixels on every OS. This ADR adds how characters the layout's font cannot draw are shaped and drawn.

## Context

A Hindi playlist whose titles are bilingual (`… Hindi Audiobook | महाभारत भाग 01 - हिंदी ऑडियोबुक`) rendered the Devanagari as "NO GLYPH" boxes. Two separate facts cause it, and both must be fixed for Hindi to be right:

- The bundled Inter Bold has no Devanagari glyphs.
- Pillow's BASIC engine maps one character to one glyph. Devanagari needs shaping: conjuncts (`क्ष`), half forms, vowel signs placed before or above the consonant (`हिंदी`), and `ऑ`. A Devanagari font under BASIC would still draw them wrong.

Pillow's own shaping engine, libraqm, cannot be relied on. Measured on 2026-10-04 with Pillow 12.3.0, CPython 3.14.7 and FreeType 2.14.3, `PIL.features.check("raqm")` is `False` in the Windows venv and in the Linux container venv (`features.version("harfbuzz")` is `None`, `check("fribidi")` is `False`). The Pillow documentation says the wheels carry a modified libraqm that loads `libfribidi` at runtime only if it is installed, and that on Windows this needs a `fribidi.dll` on the DLL search path. Whether raqm is on therefore depends on the machine, and output would differ between two machines running the same wheel. That is the reason ADR 0008 pins BASIC. What a GitHub Ubuntu or Windows runner has installed was not tested; the decision does not depend on it.

Pillow 12.3.0 has no public way to draw a glyph by id (`FreeTypeFont.getmask2` takes text), so shaping output from another engine cannot be handed to Pillow directly.

## Decision

1. The layout's `font` stays the primary font. A title whose characters the primary font covers is drawn exactly as before: the same measuring and the same `ImageDraw.text` call, so every existing golden is byte-identical.
2. One fallback font is bundled: Noto Sans Devanagari Bold, version 2.007 (`full/ttf` build from the Noto project, 1,117 glyphs, ttfautohint-ed; sha256 `6caddbb6add29ac171bc243181647fe427f4a7ed35c47cad42e3f79b37305373`), SIL Open Font License 1.1, with its licence text beside the existing one: `src/thumbforge/imaging/fonts/NotoSansDevanagari-Bold.ttf` and `OFL-NotoSansDevanagari.txt`.
3. `imaging/runs.py` (pure logic) splits a title into runs by the font that covers each character: the primary font draws what it covers, the fallback draws the rest it covers, and a character neither covers stays with the primary (its missing-glyph box). Joiners (U+200C, U+200D) and combining marks stay with the character they attach to when that character's font covers them, so a conjunct is never cut between fonts. The fallback is attached only when the title needs it, so Latin-only titles never touch it.
4. `imaging/shaping.py` shapes a Devanagari run with **uharfbuzz** (HarfBuzz), pinned to the OpenType shaper, script `Deva`, language `hi`, direction left to right and the default features. `guess_segment_properties` is not used: it reads the machine's locale, which would let the glyphs depend on the environment. Coverage checks use the same HarfBuzz font (`get_nominal_glyph`).
5. Drawing goes through Pillow, never a second rasteriser. `imaging/glyphfont.py` uses **fontTools** to make an in-memory copy of the fallback font whose only change is the character map: glyph id `n` is the code point U+F0000 + n (Supplementary Private Use Area-A). Pillow's BASIC engine then draws `chr(0xF0000 + gid)` at the position HarfBuzz gave (`x_offset`, `y_offset`, summed `x_advance`, all in font units scaled by `size / upem`). It is the same FreeType, the same stroke code and the same compositing as for Latin, so the pixels are identical on every OS and no system library is involved.
6. A title with fallback runs lays its runs end to end on one baseline per line. The line's ascent and descent are the larger of the two fonts'. Wrapping, shrinking in 4 px steps, `max_lines`, `min_size_px`, the stroke inset, anchors and case work as for Latin, because they only need `getlength`, `getmetrics` and a size, which `imaging/face.py`'s `Face` provides for both cases.
7. Strokes are drawn for every glyph first and fills second. Drawing glyph by glyph with Pillow's per-call stroke would let a glyph's stroke cover its neighbour's fill and cut notches into the Devanagari headline; Pillow does the same two passes inside one `text` call.
8. Truncation (`…`) never leaves a trailing virama or joiner behind the cut.
9. Characters neither font covers (Arabic, CJK, emoji) are drawn as the primary font's missing-glyph box, with one `fonts.uncovered` warning carrying a count and never the title. Other scripts are not supported by this decision.
10. Dependencies, added to `pyproject.toml` and locked: `uharfbuzz>=0.56.2` (0.56.2 locked; Apache-2.0; HarfBuzz is MIT) and `fonttools>=4.66.1` (4.66.1 locked; MIT). Both install from wheels on Python 3.14: verified with `uv pip install --only-binary :all:` in throwaway venvs on the Windows node and the Linux container. uharfbuzz ships `cp310-abi3` wheels (the stable ABI covers 3.14) for Windows `win_amd64` and `win32`, macOS universal2, and manylinux and musllinux x86-64 and aarch64. fontTools has `cp314` wheels for the same platforms plus a universal `py3-none-any` wheel. `fonttools` is imported only when a title reaches the fallback.
11. uharfbuzz ships no type information, so `typings/uharfbuzz/__init__.pyi` declares the few names used and pyright (strict) reads it. fontTools ships none either; the one module that uses it, `imaging/glyphfont.py`, is checked in basic mode.
12. No configuration key, template field or CLI option is added. User fonts in `<config_dir>/fonts/` keep working as documented. A layout font that itself covers Devanagari is drawn as before, character by character without shaping; `NotoSansDevanagari-Bold` is the fallback and is not meant to be chosen as a layout font.

## Consequences

- Hindi, and Latin mixed with Hindi, render correctly in the overlay, and the goldens for them are the same pixels on Windows and Linux. The golden tests render real finals through `render_final` for the three titles of the playlist that prompted this ADR.
- Hindi pixels now depend on the locked uharfbuzz and fonttools versions and on the bundled font file. A HarfBuzz upgrade can move glyph placement; the goldens fail, the new image is looked at, and it is regenerated deliberately.
- The first title in a process that uses the fallback builds the glyph-addressed font once: about 150 ms on the Linux container and about 500 ms on the Windows node, measured. Later titles reuse it.
- A native dependency is added. uharfbuzz publishes no Windows ARM64 wheel, so installing on Windows on ARM needs a C++ build toolchain. Pillow itself has such a wheel. Nothing else of Thumbforge changes there.
- The wheel and sdist grow by about 275 KB for the font.
- The fallback covers Devanagari only. A second script means another bundled font and its own script and language settings; that generalisation waits for a second user (nothing is abstracted over several fallback fonts today).
- The Part badge text keeps the plain font; a Hindi `format` in a layout's `[part]` still shows boxes. Titles are what the overlay needs shaped today.
- Long bilingual titles are cut by the template's own limits: the built-in `bold-title` (two lines, minimum 96 px) ends such a title with an ellipsis inside the Hindi part, while `series-parts` fits it at 80 px. That is layout behaviour and is unchanged.

## Alternatives considered

- **Pillow's raqm engine** — rejected: it is available only where `libfribidi` is installed, so the same wheel renders differently on two machines, and ADR 0008 chose BASIC to prevent exactly that. Requiring a system library also breaks the install-from-wheels rule.
- **HarfBuzz for shaping, outlines from fontTools drawn with Pillow's polygon routines** — rejected: it rasterises with different anti-aliasing and no hinting from the FreeType used for Latin, and the stroke would have to be rebuilt by hand, so Hindi and Latin would not look like one title.
- **freetype-py to draw glyphs by id** — rejected: a second FreeType build next to Pillow's with its own stroker and compositing, so determinism would rest on two libraries agreeing, for no gain over Pillow's own FreeType.
- **A hand-written Devanagari shaper** — rejected: reordering, conjunct and half-form rules are the work HarfBuzz and the font's OpenType tables already do, and a partial version fails on exactly the strings users have.
- **Committing a pre-modified copy of the font with the glyph-addressed character map** — rejected: a derived binary is harder to trace to the upstream release than a documented runtime transformation of the upstream file.
- **Drawing the title in a headless browser** — rejected, as for SVG in ADR 0008: a heavy runtime dependency for text, and no byte-identical output across machines.
- **A configuration key naming the fallback font** — rejected as a knob nobody has asked for; one fallback covers what is needed.
