Adventure Game
===============

A small text-based adventure game implemented in `adventure_game.py`.

Features
- Simple, interactive adventure with three locations.
- `--fast` flag to disable slow printing for faster runs and testing.
- Unit tests under `tests/`.

Requirements
- Python 3.7+

Quick start

Run the game:

```powershell
python .\adventure_game.py
```

Run the game in fast (no delays) mode:

```powershell
python .\adventure_game.py --fast
```

Run tests

```powershell
python -m unittest -v
```

Notes
- During prompts you can type `q` or `quit` to exit immediately.
- The `--fast` flag is useful for CI or automated testing to skip delays.
