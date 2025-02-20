from src import *


def main():
    root = APP()
    root.title("Foucsing")
    root.iconbitmap(default="build/icon.ico")
    root.iconbitmap("build/icon.ico")
    root.mainloop()


if __name__ == "__main__":
    main()
