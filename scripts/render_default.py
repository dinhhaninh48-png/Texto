"""Branch-default female03 voiceover; WAV and scripts stay outside Git.

Usage (Colab): python scripts/render_default.py --input /content/drive/MyDrive/tts-input/tap_02.txt
"""
import argparse
import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("female03_voiceover", REPO / "src/voxcpm/voiceover.py")
voiceover = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(voiceover)
PRESET = REPO / "voice-presets/vi_female_latenight_03/preset.json"
DRIVE = Path("/content/drive/MyDrive/AI_LAB/VoxCPM2")
REFERENCE = (
    DRIVE
    / "outputs/vi_female_latenight_02/voice_design/p1a_tap2_voice_locked_50_60"
    / "female02_A_single_voice_0051p71_0060_reference.wav"
)
OUTPUT_DIR = DRIVE / "outputs/vi_female_latenight_03"
MODEL = Path("/content/models/VoxCPM2")


def config(argv=None):
    parser = argparse.ArgumentParser(description="Default render: vi_female_latenight_03 voice-locked")
    parser.add_argument("--input", required=True, type=Path, help="UTF-8 script, one reading unit per line")
    parser.add_argument("--reference", type=Path, default=REFERENCE)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--model", type=Path, default=MODEL)
    parser.add_argument("--name", default="female03_voiceover")
    parser.add_argument("--max-chars", type=int, default=200)
    parser.add_argument("--scratch", default="/content/voxcpm2-scratch-female03")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--check", action="store_true", help="Preflight, without GPU inference or writes")
    opts = parser.parse_args(argv)
    preset = json.loads(PRESET.read_text(encoding="utf-8"))
    opts.preset = PRESET
    opts.model_revision = preset["model_revision"]
    return opts, preset


def preflight(opts, preset):
    if opts.output_dir.resolve() == (DRIVE / "outputs/vi_female_latenight_02").resolve():
        raise ValueError("Cannot write to female02 baseline output directory")
    if not opts.input.is_file():
        raise FileNotFoundError(f"Script missing: {opts.input}")
    if not opts.reference.is_file():
        raise FileNotFoundError(f"Reference missing: {opts.reference}")
    if opts.reference.name != preset["reference_filename"]:
        raise ValueError("Reference filename mismatch")
    if voiceover.digest(opts.reference) != preset["reference_sha256"]:
        raise ValueError("Reference SHA-256 mismatch")
    if not (opts.model / "config.json").is_file():
        raise FileNotFoundError(f"Model checkpoint missing: {opts.model}")
    pieces = voiceover.chunks_from_script(opts.input.read_text(encoding="utf-8"), opts.max_chars)
    return {"preset": preset["id"], "chunks": len(pieces), "input": str(opts.input)}


def main(argv=None):
    opts, preset = config(argv)
    plan = preflight(opts, preset)
    print("FEMALE03 PREFLIGHT PASS:", json.dumps(plan, ensure_ascii=False), flush=True)
    if opts.check:
        return None
    return voiceover.run(opts)


if __name__ == "__main__":
    main()
