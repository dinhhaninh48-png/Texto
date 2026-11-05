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

By default, results are isolated under `MyDrive/AI_LAB/VoxCPM2/outputs/vi_female_latenight_03/`, with content-addressed resumable runs and SHA-256 checks. Female03 uses P1-B semantic chunking (maximum 200 characters per chunk): sentence boundaries are preferred, with 0.32-second pauses after sentences, 0.12 seconds after clauses, and no added pause after a forced mid-sentence break. The explicit `--join-mode fixed` switch preserves the historical 0.55-second behavior for comparison. Existing fixed-mode job identities remain unchanged.

## Approved Tập 2 release candidate (2026-11-05)

- Status: **AUDIO_QA_APPROVED by project owner** for the full P1-B female03 render; this is audio approval, not approval to merge or publish.
- Approved WAV (external Drive): `MyDrive/AI_LAB/VoxCPM2/outputs/vi_female_latenight_03/full_tap2_p1b/tap2_full_p1b_74956a9d2ffe1264.wav`.
- WAV SHA-256: `0081cb908d54761bae0280cb314f5422b4b47e293e6c1c50bace078c9f560bab`; 48 kHz, mono, PCM 16-bit, 413.92 seconds, 38/38 chunks.
- Source script SHA-256: `8fd3fe3184890d955789d5828a613ce81fb3b2619fc6b7392298eeb147e04138`.
- Approved release metadata is separate from the frozen technical preset and generated-job manifest: `.../full_tap2_p1b/approved_release_manifest.json`, SHA-256 `da2a49882bbc09bcd4292c9d78cec6a8f87566c63a40056205e1351f73628010`.
- The independent approved release manifest includes the exact reference and script hashes, pinned commit, engine parameters, per-chunk SHA-256 and audio metadata. The accepted audio and model assets remain outside Git.
- See `docs/APPROVED_RELEASE_FEMALE03_P1B.md` for the release gate and rollback boundary.

## Acceptance and safety

- Preflight: input readable; reference filename and SHA match; model config and pinned revision match; distinct output target.
- Unit tests: `pytest -q tests/test_voiceover_pipeline.py tests/test_render_default_female03.py`.
- Unit tests: 13/13 PASS; Colab Tesla T4 smoke, controlled-interruption resume and P1-B full 38/38 render passed. The project owner approved the final audio on 2026-11-05.
- Do not merge, publish, or replace male V3 without separate approval.
