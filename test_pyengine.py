import pytest

base = "pyengine/tests"
modules = ["point.py", "cell.py", "size.py", "grid.py"]

# files = ["pyengine/tests/point.py",
#          "pyengine/tests/cell.py",
#          "pyengine/tests/size.py", ]

files = [f"{base}/{m}" for m in modules]

if __name__ == "__main__":
    for f in files:
        pytest.main(["-vv", "-s", "-x", f])
