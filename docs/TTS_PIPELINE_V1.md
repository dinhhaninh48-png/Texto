# VoxCPM2 TTS Pipeline V1 — Review Candidate

## Accepted audio evidence
The user accepted 18/18 segments, 421.25 seconds, 25/25 on audio QA, cloning from segment 13. The accepted WAV and reference stay in Google Drive, not in Git. This acceptance is for that recording; future scripts still need QA.

## Runtime
Use Python 3.12 and compatible CUDA PyTorch on an appropriate GPU (Tesla T4 worked in Colab). Install repo dependencies with `pip install -e .`. Download `openbmb/VoxCPM2` pinned revision `32279effe8c19989596f05d353d1447f51d9e915`; validate downloaded snapshot revision independently. The CLI checks the supplied revision against preset, not remote provenance.

```bash
python -m voxcpm.voiceover \
  --input /content/drive/MyDrive/tts-input/tap_02.txt \
  --reference /content/drive/MyDrive/AI_LAB/VoxCPM2/outputs/cua_so_thien_tap_01/runs/c13233b558673e72/parts/part_013_5dafef746429.wav \
  --preset voice-presets/vi_male_latenight_03_voice_locked/preset.json \
  --model /content/models/VoxCPM2 \
  --model-revision 32279effe8c19989596f05d353d1447f51d9e915 \
  --output-dir /content/drive/MyDrive/AI_LAB/VoxCPM2/outputs/new_episode --name tap_02
```

Each nonempty script line is a reading unit. Lines exceeding `--max-chars` fail explicitly. Each chunk calls `voxcpm.cli clone` with the same verified reference audio and generates locally, then copies to persistent output with SHA-256 read-back. Existing valid chunks are reused; invalid ones stop, not overwritten. A job ID includes source, preset and config. The final WAV uses PCM16 and 0.45-second silence between chunks.

## Verification gates
- Non-GPU unit tests and CLI preflight must pass.
- Review experimental BF16 loader patch; validate Colab CUDA/T4 model load, VRAM/RAM, cloning, resume and full export.
- Listen to every section, boundaries and missing words before release.
- Process crash mid-upload may leave partial file. Quarantine and examine; do not silently overwrite.
- Never commit secrets, WAV or weights. Codex Cloud need not have GPU.

## Limitations
This version reloads the model per chunk (same approach as accepted V3), not optimized batch execution. Audio quality and determinism cannot be guaranteed from a seed alone.
