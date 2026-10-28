# Repository agent instructions

- Follow existing VoxCPM source and tests; avoid core behavior changes without review and GPU regression tests.
- Accepted reference WAV, exports, model checkpoints, credentials and private scripts belong outside Git.
- Work in review branches and PRs; do not merge or deploy without explicit approval.
- Preserve UTF-8 script content, chunk order, checksum and manifest; never silently replace an existing WAV.
- Report GPU inference as unverified unless genuinely executed.
