# vi_female_latenight_02 — configuration scaffold

Status: **BLOCKED for inference until a new female reference WAV is supplied and verified**.

## Inheritance

This profile intentionally copies the technical generation parameters from
`vi_male_latenight_03_voice_locked` in PR #1:
- VoxCPM2, clone mode
- pinned model revision `32279effe8c19989596f05d353d1447f51d9e915`
- seed 42; CFG 2.0; 10 inference timesteps; 0.45-second inter-chunk pause
- CLI clone flags: offline/local files only, no denoiser, no optimize

Voice identity is **not** inherited: a new female reference WAV, filename and verified SHA-256 are mandatory. Do not reuse the male reference hash.

## Activation gate

1. Obtain the authorized female WAV outside Git.
2. Compute its SHA-256 and inspect that the WAV is readable and nonempty.
3. Replace both null fields in `preset.json` with the exact filename and SHA-256.
4. Update status to indicate reference verified (not audio QA accepted).
5. Run a single-chunk GPU regression and human listening QA.
6. Only then run a full render and complete QA.

Until step 3, the reference-lock check in PR #1's `voiceover.py` prevents successful rendering.

## Isolated storage

Use a distinct output path:

```text
/content/drive/MyDrive/AI_LAB/VoxCPM2/outputs/vi_female_latenight_02/
  runs/<job_id>/manifest.json
  runs/<job_id>/parts/
  <episode_name>_<job_id>.wav
```

Do not use the male V3 output directory. The manifest and job identity include preset and reference SHA-256, so a new reference produces a new job ID. Avoid running concurrent jobs to the same output directory.

## Dependency on PR #1

This branch was created from `main` as requested. As of creation, the reusable `src/voxcpm/voiceover.py` CLI and experimental BF16 loader change exist only in draft PR #1, not `main`. This profile-only branch must be rebased/integrated after PR #1 is approved and merged. Do not merge or claim end-to-end readiness before that gate and GPU verification.
