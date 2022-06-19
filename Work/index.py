from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from Library.app import *

if (__name__ == '__main__'):
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())