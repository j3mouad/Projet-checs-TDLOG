
import subprocess
import sys

def ensure_pygame_installed():
    try:
        import pygame
        print("Pygame is already installed.")
    except ImportError:
        print("Pygame is not installed. Installing now...")
        # Install pygame using pip.
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        # Optionally, you can try importing it again to confirm installation.
        try:
            import pygame
            print("Pygame installation was successful.")
        except ImportError:
            print("Failed to install pygame. Please install it manually.")
            sys.exit(1)
