# Original female voice 02 — reference recording brief

## Identity and tone

Create a **new, non-impersonating Vietnamese female narrator voice** for
`vi_female_latenight_02`. The desired listening experience is reassuring,
warm, unhurried, gentle and grounded. This is a descriptive creative direction,
**not a request to reproduce a named person's identifiable voice**.

- Adult female voice, naturally warm lower-mid register; avoid forced low pitch.
- Gentle Northern Vietnamese accent; clear consonants and full vowels.
- Natural, rounded pronunciation and restrained, conversational expression.
- Thoughtful pauses; calm cadence without whispering or exaggerated breathiness.
- No theatrical sadness, devotional mimicry, sales intonation or artificial sweetness.
- Read steadily with subtle emotional variation, preserving the narrator's own voice.

## Recording guidance

- Record 60–120 seconds of clean, continuous speech, ideally across several
  sentences with varied vowels and punctuation.
- Single speaker, no music, no ambience, no overlapping voices or effects.
- Quiet room and consistent microphone position; avoid clipping and aggressive
  denoise/compression. Export uncompressed WAV.
- Narrator should read naturally, not imitate any celebrity, teacher or public figure.
- Review the recording by listening before using it for voice cloning.

## Original calibration text (Vietnamese)

> Đêm xuống thật chậm. Ngoài hiên, tiếng gió khẽ lay những chiếc lá.
> Ta có thể đặt xuống những lo toan của một ngày dài, ngồi yên và lắng nghe hơi thở.
> Không cần vội vàng để đến một nơi nào khác.
> Một tách trà ấm, một trang sách mở, và vài phút bình an cũng đã là đủ.
> Có những điều trong cuộc sống không thể giữ mãi.
> Khi hiểu được điều ấy, lòng mình có thể nhẹ hơn, dịu hơn, và rộng mở hơn.
> Ngày mai sẽ đến theo cách của ngày mai.
> Còn lúc này, xin hãy dành cho mình một chút nghỉ ngơi.

This script is newly authored for calibration; the narrator may use another
original or licensed text with a comparable range of sounds.

## Permission and provenance

Before any upload or model inference, record:
- narrator name or approved pseudonym and file provenance;
- explicit permission to use the recording as a **voice-cloning reference**
  for synthetic narration and its intended distribution;
- scope, term, revocation conditions and any compensation;
- confirmation the narrator is an adult and the audio is not impersonation.

Keep consent records and WAV outside Git. Do not commit personal information
or a reference clip.

## Technical activation

The profile inherits the V3 model revision, seed 42, CFG 2.0, 10 timesteps,
0.45-second pause and offline clone flags. When an authorized WAV is selected:
1. Inspect audio duration, sample rate, channels, peak/clipping and audibility.
2. Compute SHA-256 and update the profile's `reference_filename` and
   `reference_sha256` values (currently null).
3. Render a short phrase on Colab, listen for pronunciation, pacing, artifacts
   and unintended identity similarity, then approve or reject the reference.
4. Store outputs under
   `/content/drive/MyDrive/AI_LAB/VoxCPM2/outputs/vi_female_latenight_02/`.
5. Do not mark the profile production-ready until the shared CLI from PR #1 is
   integrated and GPU regression, resume and audio QA are completed.
