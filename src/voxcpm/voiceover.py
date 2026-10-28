"""Reference-locked, resumable VoxCPM2 voiceover. Run: python -m voxcpm.voiceover."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def chunks_from_script(script, max_chars=420):
    if max_chars < 1:
        raise ValueError("max_chars must be positive")
    units = [s.strip() for s in script.splitlines() if s.strip()]
    if not units:
        raise ValueError("Script is empty")
    chunks, current = [], []
    for unit in units:
        if len(unit) > max_chars:
            raise ValueError(f"Reading unit exceeds max_chars: {len(unit)}. Split this line.")
        candidate = " ".join(current + [unit])
        if current and len(candidate) > max_chars:
            chunks.append(" ".join(current))
            current = [unit]
        else:
            current.append(unit)
    if current:
        chunks.append(" ".join(current))
    assert " ".join(chunks) == " ".join(units)
    return chunks


def audio_info(path):
    import soundfile as sf
    p = Path(path)
    if not p.is_file() or p.stat().st_size == 0:
        raise ValueError(f"Missing/empty WAV: {p}")
    info = sf.info(str(p))
    if info.frames <= 0 or info.samplerate <= 0:
        raise ValueError(f"Invalid WAV: {p}")
    return info


def copy_exclusive_verified(src, dst):
    src, dst = Path(src), Path(dst)
    audio_info(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if digest(src) != digest(dst):
            raise FileExistsError(f"Existing artifact differs: {dst}")
        return
    with src.open("rb") as reader, dst.open("xb") as writer:
        shutil.copyfileobj(reader, writer)
    if digest(src) != digest(dst):
        raise RuntimeError(f"Checksum mismatch: {dst}")


def run(args):
    import numpy as np
    import soundfile as sf

    preset = json.loads(Path(args.preset).read_text(encoding="utf-8"))
    for field in ("model_revision", "reference_sha256", "seed", "cfg_value",
                  "inference_timesteps", "pause_seconds"):
        if field not in preset:
            raise ValueError(f"Missing preset field: {field}")
    reference = Path(args.reference)
    audio_info(reference)
    if digest(reference) != preset["reference_sha256"]:
        raise ValueError("Reference SHA-256 mismatch: wrong voice")
    model = Path(args.model)
    if not (model / "config.json").is_file():
        raise FileNotFoundError("Model config.json missing")
    if args.model_revision != preset["model_revision"]:
        raise ValueError("Model revision mismatch")
    script = Path(args.input).read_text(encoding="utf-8")
    pieces = chunks_from_script(script, args.max_chars)

    identity = {
        "script_sha256": hashlib.sha256(script.encode("utf-8")).hexdigest(),
        "preset": preset,
        "reference_sha256": digest(reference),
        "max_chars": args.max_chars,
        "model_revision": args.model_revision,
    }
    job_id = hashlib.sha256(json.dumps(identity, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
    output_dir = Path(args.output_dir)
    job = output_dir / "runs" / job_id
    parts = job / "parts"
    job.mkdir(parents=True, exist_ok=True)
    manifest = job / "manifest.json"
    if manifest.exists():
        if json.loads(manifest.read_text(encoding="utf-8")) != identity:
            raise RuntimeError("Existing manifest differs")
    else:
        with manifest.open("x", encoding="utf-8") as f:
            json.dump(identity, f, ensure_ascii=False, indent=2)
    parts.mkdir(parents=True, exist_ok=True)
    scratch = Path(args.scratch) / job_id
    scratch.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["HF_HUB_OFFLINE"] = "1"
    env["PYTHONUNBUFFERED"] = "1"

    for i, piece in enumerate(pieces, 1):
        name = f"part_{i:03d}_{hashlib.sha256(piece.encode('utf-8')).hexdigest()[:12]}.wav"
        target = parts / name
        if target.exists():
            audio_info(target)
            print(f"[{i}/{len(pieces)}] Resume: existing audio (requires human QA)", flush=True)
            continue
        local = scratch / name
        local.unlink(missing_ok=True)
        command = [
            sys.executable, "-m", "voxcpm.cli", "clone",
            "--model-path", str(model), "--device", args.device,
            "--local-files-only", "--no-denoiser", "--no-optimize",
            "--reference-audio", str(reference), "--text", piece,
            "--seed", str(preset["seed"]),
            "--cfg-value", str(preset["cfg_value"]),
            "--inference-timesteps", str(preset["inference_timesteps"]),
            "--output", str(local),
        ]
        print(f"[{i}/{len(pieces)}] CLONING...", flush=True)
        subprocess.run(command, env=env, check=True)
        copy_exclusive_verified(local, target)
        local.unlink(missing_ok=True)
        print(f"[{i}/{len(pieces)}] PERSISTED & VERIFIED", flush=True)

    ordered = [parts / f"part_{i:03d}_{hashlib.sha256(piece.encode('utf-8')).hexdigest()[:12]}.wav"
               for i, piece in enumerate(pieces, 1)]
    infos = [audio_info(p) for p in ordered]
    rate, channels = infos[0].samplerate, infos[0].channels
    if any(x.samplerate != rate or x.channels != channels for x in infos):
        raise ValueError("Inconsistent sample rate/channels")

    assembled = scratch / "full.wav"
    pause = np.zeros((round(rate * float(preset["pause_seconds"])), channels), dtype="float32")
    with sf.SoundFile(str(assembled), "w", samplerate=rate, channels=channels, subtype="PCM_16") as out:
        for i, part in enumerate(ordered):
            for block in sf.blocks(str(part), blocksize=65536, dtype="float32", always_2d=True):
                out.write(block)
            if i + 1 < len(ordered):
                out.write(pause)
    audio_info(assembled)
    final = output_dir / f"{args.name}_{job_id}.wav"
    copy_exclusive_verified(assembled, final)
    print(f"VOICEOVER COMPLETED\\nDRIVE SAVE VERIFIED: {final}\\nPARTS: {len(ordered)}\\nSHA256: {digest(final)}")
    return final


def main():
    parser = argparse.ArgumentParser(description="Resumable VoxCPM2 reference-locked voiceover")
    parser.add_argument("--input", required=True, help="UTF-8 script; one reading unit per line")
    parser.add_argument("--reference", required=True, help="External reference WAV")
    parser.add_argument("--preset", required=True)
    parser.add_argument("--model", required=True, help="Downloaded local VoxCPM2 checkpoint")
    parser.add_argument("--model-revision", required=True, help="Verified HF checkpoint SHA")
    parser.add_argument("--output-dir", required=True, help="Persistent output path (e.g. mounted Drive)")
    parser.add_argument("--scratch", default="/content/voxcpm2-scratch")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--name", default="voiceover")
    parser.add_argument("--max-chars", type=int, default=420)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
