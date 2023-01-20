from datetime import datetime


class TeminalColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Logger:
    def header(self, msg):
        print(f"{TeminalColors.HEADER} {msg} {TeminalColors.ENDC}")

    def info(self, msg):
        print(
            f"{TeminalColors.OKCYAN}[INFO] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}{TeminalColors.ENDC}"
        )

    def none(self, msg):
        print(
            f"{TeminalColors.ENDC}[INFO] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}{TeminalColors.ENDC}"
        )

    def warning(self, msg):
        print(
            f"{TeminalColors.WARNING}[WARNING] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}{TeminalColors.ENDC}"
        )

    def fail(self, msg):
        print(
            f"{TeminalColors.FAIL}[FAIL] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}{TeminalColors.ENDC}"
        )

    def green(self, msg):
        print(
            f"{TeminalColors.OKGREEN}[SUCCESS] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}{TeminalColors.ENDC}"
        )

    def print_line(self):
        print(
            f"{TeminalColors.HEADER}=================================================================================={TeminalColors.ENDC}"
        )
