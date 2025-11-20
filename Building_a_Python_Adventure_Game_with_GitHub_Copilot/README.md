# Adventure Game

Small text-based adventure game used to practice functions, conditionals and I/O.

Features:
- Interactive CLI with multiple locations (Dark Forest, Ancient Ruins, Mystic Lake)
- Input validation and a global quit option (`q`/`quit`)
- `--fast` flag to disable slow printing for tests/demos

Running

PowerShell examples (from project root):

```powershell
# Normal run (slow printing enabled)
python ./adventure_game.py

# Fast run (skip delays)
python ./adventure_game.py --fast

# If `python` isn't on PATH, use the launcher
py -3 ./adventure_game.py --fast
```

Testing

The project uses `pytest`. From the project root run:

```powershell
pip install pytest
pytest -q
```

Notes

- At any prompt you can type `q` or `quit` to exit immediately.
- Use `--fast` to make runs deterministic and fast for CI or demos.
