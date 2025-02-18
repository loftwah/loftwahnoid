import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from loftwahnoid.menus import main_menu

if __name__ == '__main__':
    main_menu() 