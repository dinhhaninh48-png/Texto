"""Unit tests without downloading model weights or requiring GPU."""
from pathlib import Path
import importlib.util
import pytest

SOURCE = Path(__file__).resolve().parents[1] / "src" / "voxcpm" / "voiceover.py"
spec = importlib.util.spec_from_file_location("voiceover_under_test", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_chunk_preserves_text_and_order():
    script = "Xin chào.\nMột câu nữa.\n\nKết thúc."
    result = module.chunks_from_script(script, 25)
    assert " ".join(result) == "Xin chào. Một câu nữa. Kết thúc."
    assert all(len(x) <= 25 for x in result)


def test_long_unit_must_be_split():
    with pytest.raises(ValueError, match="Split this line"):
        module.chunks_from_script("x" * 40, 20)


def test_blank_script_fails():
    with pytest.raises(ValueError, match="empty"):
        module.chunks_from_script("  \n ")


def test_semantic_chunks_avoid_mid_sentence_boundary():
    script = "Một buổi tối yên bình.\nTa ngồi bên cửa sổ.\nÁnh đèn vẫn sáng."
    chunks = module.semantic_chunks_from_script(script, 42)
    assert " ".join(chunks) == script.replace("\n", " ")
    assert all(len(chunk) <= 42 for chunk in chunks)
    assert all(chunk.endswith(".") for chunk in chunks[:-1])


def test_semantic_chunk_falls_back_at_clause_then_word():
    script = "Một lời rất dài, được nói thật chậm để người nghe có thể hiểu."
    chunks = module.semantic_chunks_from_script(script, 32)
    assert " ".join(chunks) == script
    assert all(len(chunk) <= 32 for chunk in chunks)
    assert chunks[0].endswith(",")


def test_pause_is_contextual_and_legacy_unchanged():
    preset = {"pause_seconds": 0.55}
    assert module.boundary_pause_seconds("giữa mạch câu", preset, "semantic") == 0
    assert module.boundary_pause_seconds("ngừng nhẹ,", preset, "semantic") == 0.12
    assert module.boundary_pause_seconds("hết câu.", preset, "semantic") == 0.32
    assert module.boundary_pause_seconds("giữa mạch câu", preset, "fixed") == 0.55


def test_digest_changes_on_different_content(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.write_bytes(b"hello")
    b.write_bytes(b"world")
    assert module.digest(a) != module.digest(b)


def test_existing_mismatched_target_not_overwritten(tmp_path):
    import soundfile as sf
    import numpy as np
    source, target = tmp_path / "source.wav", tmp_path / "target.wav"
    sf.write(str(source), np.zeros(4800, dtype=np.float32), 48000)
    sf.write(str(target), np.ones(4800, dtype=np.float32) * .1, 48000)
    original = module.digest(target)
    with pytest.raises(FileExistsError):
        module.copy_exclusive_verified(source, target)
    assert module.digest(target) == original
