# Female03 P1-B — approved audio release record

This record tracks an **accepted audio artifact**, not an automatically approved repository merge or public deployment.

## Identity and immutable evidence

| Field | Value |
| --- | --- |
| Profile | `vi_female_latenight_03` |
| Engine | VoxCPM2, reference-locked clone |
| Accepted source | Full Tập 2 script from Google Doc `1nBQNVCH8X5cOJFRi2ez0aqy7t5AfWNcMdfn_9mBIw3s` |
| Source SHA-256 | `8fd3fe3184890d955789d5828a613ce81fb3b2619fc6b7392298eeb147e04138` |
| Reference SHA-256 | `d5cf87b645c1cf3e3252905790dcce9c8428ed937d70cd9de317a66c1038fd3e` |
| Checkpoint revision | `32279effe8c19989596f05d353d1447f51d9e915` |
| Generation | seed `42`, CFG `2.0`, timesteps `10`, semantic P1-B |
| Code commit | `69fd9dcccd0a7c9a729d507c6b685fb76f526a29` |
| Job ID | `74956a9d2ffe1264` |
| Output | 38 WAV parts; final 48 kHz, mono, PCM 16-bit; 413.92 seconds |
| Final WAV SHA-256 | `0081cb908d54761bae0280cb314f5422b4b47e293e6c1c50bace078c9f560bab` |
| QA decision | `AUDIO_QA_APPROVED` by project owner, 2026-11-05 |

Approved WAV (external Drive):

`MyDrive/AI_LAB/VoxCPM2/outputs/vi_female_latenight_03/full_tap2_p1b/tap2_full_p1b_74956a9d2ffe1264.wav`

Canonical approval metadata (external Drive):

`MyDrive/AI_LAB/VoxCPM2/outputs/vi_female_latenight_03/full_tap2_p1b/approved_release_manifest.json`

Manifest SHA-256: `da2a49882bbc09bcd4292c9d78cec6a8f87566c63a40056205e1351f73628010`.

The manifest was read back and checked against all 38 part files, the original script, the reference, and the final WAV. Existing job identity `runs/74956a9d2ffe1264/manifest.json` is preserved. Do not change the preset's metadata fields merely to change approval status: the engine hashes the entire preset into the job identity, so changing it would create a new job ID and break existing resume continuity.

## Release checklist

- [x] Reference/source/preset/model revision pinned.
- [x] GPU smoke and controlled interruption/resume validated.
- [x] P1-B full Tập 2 render completed and 38/38 chunks verified.
- [x] Final WAV SHA-256 and immutable release manifest verified.
- [x] Human audio QA approved by project owner.
- [x] Male V3 and `main` left unchanged.
- [ ] PR review and current CI/status check completed on final head.
- [ ] Explicit repository merge authorization recorded.
- [ ] Public publication separately authorized (not requested).

## Merge / rollback boundary

The female03 default changes live in review branch `vi_female_latenight_03`, PR #2 against `main`. Do not merge merely because audio QA passed. Before merging, review the final diff and CI/status, then obtain explicit approval. If regression occurs, keep the approved WAV and manifest intact; revert only the repository merge through a new reviewable change. Never replace the approved WAV in place.
