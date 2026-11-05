# Default render on branch `vi_female_latenight_03`

This **review branch** defaults to the female Voice-Locked profile when calling `scripts/render_default.py`. It does not change `voxcpm.cli`, the male V3 preset, or `main`.

## Voice identity and provenance

- Preset: `voice-presets/vi_female_latenight_03/preset.json`
- Engine: VoxCPM2, reference-only voice cloning; seed `42`, CFG `2.0`, timesteps `10`.
- Checkpoint revision: `32279effe8c19989596f05d353d1447f51d9e915`.
- Reference: an 8.29-second uninterrupted crop **51.71–60.00s** from the 50–60s area of the earlier P1-A female02 recording. The exact 50–60s crop crossed a generated-chunk seam and could mix timbres.
- SHA-256: `d5cf87b645c1cf3e3252905790dcce9c8428ed937d70cd9de317a66c1038fd3e`.
- Reference location (external Google Drive): `MyDrive/AI_LAB/VoxCPM2/outputs/vi_female_latenight_02/voice_design/p1a_tap2_voice_locked_50_60/female02_A_single_voice_0051p71_0060_reference.wav`.
- Input scripts, reference and audio outputs remain outside Git. Never commit the reference WAV, rendered segments, or checkpoint.

The source Tập 2 script is in Google Docs, ID `1nBQNVCH8X5cOJFRi2ez0aqy7t5AfWNcMdfn_9mBIw3s`, and must be exported as clean UTF-8 reading text with section separators removed before rendering. The previously generated female02 Voice-Locked technical sample had 45 segments and 427.4 seconds of audio. This is **technical evidence, not a passed listening QA**.

## Colab workflow

1. Open the existing female Colab notebook `VoxCPM2_vi_female_latenight_02.ipynb`; mount Drive.
2. Fetch branch `vi_female_latenight_03` from `dinhhaninh48-png/Texto` into a separate checkout for the female03 default pipeline. Keep the old female02 notebook cells as historical QA evidence.
3. Install dependencies and acquire the pinned VoxCPM2 checkpoint when the Colab runtime is new.
4. Export the production script to an external Drive UTF-8 file, one reading unit per line, then preflight:

```bash
python scripts/render_default.py \
  --input /content/drive/MyDrive/tts-input/tap_02.txt \
  --check
```

5. Render only after preflight passes:

```bash
python scripts/render_default.py \
  --input /content/drive/MyDrive/tts-input/tap_02.txt
```

By default, results are isolated under `MyDrive/AI_LAB/VoxCPM2/outputs/vi_female_latenight_03/`, with content-addressed resumable runs and SHA-256 checks. The script keeps the existing engine implementation (0.55-second pauses; max 200 characters per chunk); it does not claim bitwise reproduction of the earlier female02 prototype's 45-segment, mixed 0.55/0.85-second pause assembly.

## Acceptance and safety

- Preflight: input readable; reference filename and SHA match; model config and pinned revision match; distinct output target.
- Unit tests: `pytest -q tests/test_voiceover_pipeline.py tests/test_render_default_female03.py`.
- GPU QA still required for this new default entrypoint: one-chunk render, resume, full export, and listening to beginning/middle/end for timbre drift, pacing and boundary artifacts.
- Do not merge, publish, or replace male V3 without separate approval.
