from .mainScript import main
from .settings import GENERATED_DIR


if __name__ == '__main__':
    # create required directories
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    main()
