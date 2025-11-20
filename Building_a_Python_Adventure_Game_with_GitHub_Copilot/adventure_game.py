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
    while True:
        response = input(prompt).strip()
        if response.lower() in {"q", "quit"}:
            raise SystemExit("Goodbye!")

        if valid is None:
            return response

        if response.lower() in set(valid):
            return response

        print("Invalid input. Please try again (or type 'q' to quit).")


class Game:
    """Encapsulates the adventure game state and logic."""

    def __init__(self, fast: bool = False) -> None:
        self.fast = fast

    def intro(self) -> None:
        slow_print("Welcome to the Adventure Game!", enabled=not self.fast)
        slow_print(
            "You find yourself in a mysterious land filled with challenges and treasures.",
            enabled=not self.fast,
        )
        slow_print("Your quest is to find the hidden treasure and return safely.", enabled=not self.fast)
        slow_print("Good luck, adventurer!\n", enabled=not self.fast)

    def choose_path(self) -> str:
        slow_print("You are at a crossroads. Where would you like to go?", enabled=not self.fast)
        slow_print("1. The Dark Forest", enabled=not self.fast)
        slow_print("2. The Ancient Ruins", enabled=not self.fast)
        slow_print("3. The Mystic Lake", enabled=not self.fast)
        return prompt_input("Enter the number of your choice: ", valid={"1", "2", "3"})

    def dark_forest(self) -> bool:
        slow_print("\nYou venture into the Dark Forest. The trees are tall and the path is narrow.", enabled=not self.fast)
        slow_print("Suddenly, a wild beast appears!", enabled=not self.fast)
        action = prompt_input("Do you want to (1) Fight or (2) Run? ", valid={"1", "2"})
        if action == "1":
            # 50/50 outcome
            if random.random() > 0.5:
                slow_print("You bravely fight the beast and win!", enabled=not self.fast)
                return True
            slow_print("The beast overpowers you. You have to retreat.", enabled=not self.fast)
            return False

        slow_print("You run away safely, but you lose some time.", enabled=not self.fast)
        return False

    def ancient_ruins(self) -> bool:
        slow_print("\nYou arrive at the Ancient Ruins. The air is thick with mystery.", enabled=not self.fast)
        slow_print("You find a locked chest. It requires a code to open.", enabled=not self.fast)
        code = prompt_input("Enter a 3-digit code to unlock the chest: ")
        if code.isdigit() and len(code) == 3 and code == "123":
            slow_print("The chest opens! You find a precious gem inside.", enabled=not self.fast)
            return True

        slow_print("The code is incorrect. The chest remains locked.", enabled=not self.fast)
        return False

    def mystic_lake(self) -> bool:
        slow_print("\nYou reach the Mystic Lake. The water is crystal clear.", enabled=not self.fast)
        slow_print("A magical creature appears and offers you a riddle.", enabled=not self.fast)
        riddle_answer = prompt_input("What has keys but can't open locks? ")
        if riddle_answer.lower() in {"piano", "keyboard"}:
            slow_print("Correct! The creature grants you a magical artifact.", enabled=not self.fast)
            return True

        slow_print("Wrong answer. The creature vanishes.", enabled=not self.fast)
        return False

    def run(self) -> None:
        """Run the main game loop."""
        self.intro()
        while True:
            try:
                choice = self.choose_path()
            except SystemExit as e:
                slow_print(str(e), enabled=not self.fast)
                return

            if choice == "1":
                success = self.dark_forest()
            elif choice == "2":
                success = self.ancient_ruins()
            else:
                success = self.mystic_lake()

            if success:
                slow_print("\nCongratulations! You have made progress on your quest.", enabled=not self.fast)
            else:
                slow_print("\nYou need to try again to make progress.", enabled=not self.fast)

            try:
                continue_game = prompt_input("Do you want to continue your adventure? (yes/no) ", valid={"yes", "no"})
            except SystemExit as e:
                slow_print(str(e), enabled=not self.fast)
                return

            if continue_game.lower() != "yes":
                slow_print("Thank you for playing the Adventure Game! Goodbye!", enabled=not self.fast)
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
