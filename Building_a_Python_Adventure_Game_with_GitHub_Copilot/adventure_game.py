"""A small, refactored text-based adventure game.

Improvements over the original:
- Encapsulated game logic in a `Game` class
- Added type hints and docstrings
- Input validation and a global quit option (`q` / `quit`)
- `--fast` CLI flag to skip printed delays (helpful for testing)
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from typing import Iterable, Optional


def slow_print(text: str, delay: float = 0.03, enabled: bool = True) -> None:
    """Print text slowly to the console when `enabled` is True.

    Setting `enabled=False` prints immediately (useful for tests / fast mode).
    """
    if not enabled:
        print(text)
        return

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def prompt_input(prompt: str, valid: Optional[Iterable[str]] = None) -> str:
    """Prompt the user until they enter a valid response.

    - If `valid` is provided, the user's response (stripped/lowercased) must
      be in that set.
    - The user can type `q` or `quit` to exit immediately.
    """
    valid_set = None if valid is None else {v.lower() for v in valid}
    while True:
        response = input(prompt).strip()
        low = response.lower()
        if low in {"q", "quit"}:
            raise SystemExit("Goodbye!")

        if valid_set is None:
            return response

        if low in valid_set:
            return response

        print("Invalid input. Please try again (or type 'q' to quit).")


class Game:
    """Encapsulates the adventure game state and logic."""

    def __init__(self, fast: bool = False) -> None:
        self.fast = fast
        # Convenience wrapper to call slow_print with the game's fast flag
        # Use as: self.sp("text") instead of repeating enabled=not self.fast
        def _sp(text: str, delay: float = 0.03) -> None:
            slow_print(text, delay=delay, enabled=not self.fast)

        self.sp = _sp

    def intro(self) -> None:
        self.sp("Welcome to the Adventure Game!")
        self.sp("You find yourself in a mysterious land filled with challenges and treasures.")
        self.sp("Your quest is to find the hidden treasure and return safely.")
        self.sp("Good luck, adventurer!\n")

    def choose_path(self) -> str:
        self.sp("You are at a crossroads. Where would you like to go?")
        self.sp("1. The Dark Forest")
        self.sp("2. The Ancient Ruins")
        self.sp("3. The Mystic Lake")
        return prompt_input("Enter the number of your choice: ", valid={"1", "2", "3"})

    def dark_forest(self) -> bool:
        self.sp("\nYou venture into the Dark Forest. The trees are tall and the path is narrow.")
        self.sp("Suddenly, a wild beast appears!")
        action = prompt_input("Do you want to (1) Fight or (2) Run? ", valid={"1", "2"})
        if action == "1":
            # 50/50 outcome
            if random.random() > 0.5:
                self.sp("You bravely fight the beast and win!")
                return True
            self.sp("The beast overpowers you. You have to retreat.")
            return False

        self.sp("You run away safely, but you lose some time.")
        return False

    def ancient_ruins(self) -> bool:
        self.sp("\nYou arrive at the Ancient Ruins. The air is thick with mystery.")
        self.sp("You find a locked chest. It requires a code to open.")
        code = prompt_input("Enter a 3-digit code to unlock the chest: ")
        if code.isdigit() and len(code) == 3 and code == "123":
            self.sp("The chest opens! You find a precious gem inside.")
            return True

        self.sp("The code is incorrect. The chest remains locked.")
        return False

    def mystic_lake(self) -> bool:
        self.sp("\nYou reach the Mystic Lake. The water is crystal clear.")
        self.sp("A magical creature appears and offers you a riddle.")
        riddle_answer = prompt_input("What has keys but can't open locks? ")
        if riddle_answer.lower() in {"piano", "keyboard"}:
            self.sp("Correct! The creature grants you a magical artifact.")
            return True

        self.sp("Wrong answer. The creature vanishes.")
        return False

    def run(self) -> None:
        """Run the main game loop."""
        self.intro()
        while True:
            try:
                choice = self.choose_path()
            except SystemExit as e:
                self.sp(str(e))
                return

            if choice == "1":
                success = self.dark_forest()
            elif choice == "2":
                success = self.ancient_ruins()
            else:
                success = self.mystic_lake()

            if success:
                self.sp("\nCongratulations! You have made progress on your quest.")
            else:
                self.sp("\nYou need to try again to make progress.")

            try:
                continue_game = prompt_input("Do you want to continue your adventure? (yes/no) ", valid={"yes", "no"})
            except SystemExit as e:
                self.sp(str(e))
                return

            if continue_game.lower() != "yes":
                self.sp("Thank you for playing the Adventure Game! Goodbye!")
                break


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Play a tiny text-based adventure game.")
    parser.add_argument("--fast", action="store_true", help="Disable slow printing for faster runs/testing")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    # seed randomness for more varied runs; keep it non-deterministic by default
    random.seed()
    game = Game(fast=args.fast)
    try:
        game.run()
    except KeyboardInterrupt:
        slow_print("\nInterrupted. Goodbye!", enabled=not game.fast)


if __name__ == "__main__":
    main()
