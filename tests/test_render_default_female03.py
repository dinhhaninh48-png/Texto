"""Female03 default render checks that do not require the GPU checkpoint."""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
SOURCE = ROOT / "scripts/render_default.py"
spec = importlib.util.spec_from_file_location("render_default_female03", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_default_profile_is_voice_locked_and_separate_from_male():
    opts, preset = module.config(["--input", "script.txt"])
    male = json.loads((ROOT / "voice-presets/vi_male_latenight_03_voice_locked/preset.json").read_text())
    assert preset["id"] == "vi_female_latenight_03"
    assert preset["seed"] == 42
    assert preset["cfg_value"] == 2.0
    assert preset["inference_timesteps"] == 10
    assert preset["reference_sha256"] != male["reference_sha256"]
    assert "vi_female_latenight_03" in str(opts.output_dir)
    assert "vi_female_latenight_02" in str(opts.reference)
    assert opts.preset == module.PRESET
    assert opts.join_mode == "semantic"


def test_preflight_accepts_matching_reference_without_running_gpu(tmp_path):
    source = tmp_path / "script.txt"
    source.write_text("Xin chào.\nHôm nay thật bình yên.", encoding="utf-8")
    reference = tmp_path / "reference.wav"
    sf.write(reference, np.zeros(48000, dtype="float32"), 48000)
    model = tmp_path / "checkpoint"
    model.mkdir()
    (model / "config.json").write_text("{}")
    opts, preset = module.config(["--input", str(source), "--reference", str(reference), "--model", str(model), "--check"])
    preset = {**preset, "reference_filename": reference.name, "reference_sha256": module.voiceover.digest(reference)}
    assert module.preflight(opts, preset)["chunks"] == 1


def test_preflight_rejects_wrong_voice(tmp_path):
    source = tmp_path / "script.txt"
    source.write_text("Một câu thử.", encoding="utf-8")
    reference = tmp_path / "reference.wav"
    sf.write(reference, np.zeros(48000, dtype="float32"), 48000)
    model = tmp_path / "checkpoint"
    model.mkdir()
    (model / "config.json").write_text("{}")
    opts, preset = module.config(["--input", str(source), "--reference", str(reference), "--model", str(model), "--check"])
    with pytest.raises(ValueError, match="filename mismatch"):
        module.preflight(opts, preset)


def test_female03_check_mode_has_no_render(monkeypatch, tmp_path):
    source = tmp_path / "script.txt"
    source.write_text("Một câu thử.", encoding="utf-8")
    monkeypatch.setattr(module, "preflight", lambda *_: {"chunks": 1})
    monkeypatch.setattr(module.voiceover, "run", lambda *_: pytest.fail("GPU render must not execute"))
    assert module.main(["--input", str(source), "--check"]) is None


def test_female03_fixed_mode_remains_available():
    opts, _ = module.config(["--input", "script.txt", "--join-mode", "fixed"])
    assert opts.join_mode == "fixed"
