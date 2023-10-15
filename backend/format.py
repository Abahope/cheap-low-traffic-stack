import subprocess


def main():
    subprocess.run(["isort", ".", "-v"])


if __name__ == "__main__":
    main()
