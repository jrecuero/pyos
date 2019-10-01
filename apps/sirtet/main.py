import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from _game import TheGame


def main():
    """main implements the full game application.
    """
    game = TheGame()
    game.create()
    game.new_match()
    game.start_match()
    game.play()
    game.end_match()


if __name__ == "__main__":
    main()
