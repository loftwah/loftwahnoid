import os
import sys

# Add the src directory to the path when running directly
if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from loftwahnoid.menus import main_menu

if __name__ == '__main__':
    main_menu() 