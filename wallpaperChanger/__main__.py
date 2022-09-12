from .mainScript import main, refresh
from .settings import GENERATED_DIR
import argparse


if __name__ == '__main__':
    # create required directories
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("mode")
    args = parser.parse_args()

    if args.mode == "refresh":
        refresh()
    else:
        main()
