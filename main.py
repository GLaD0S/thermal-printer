from escpos.printer import Network


def build_ornate_box(message: str, width: int = 68) -> str:
    inner_width = width - 2
    centered_message = f"{message}".center(inner_width)

    lines = [
        "+" + "=" * inner_width + "+",
        "|" + "*" * inner_width + "|",
        "|" + ("*~" * (inner_width // 2)).ljust(inner_width, "*") + "|",
        centered_message,
        "|" + ("~*" * (inner_width // 2)).ljust(inner_width, "*") + "|",
        "|" + "*" * inner_width + "|",
        "+" + "=" * inner_width + "+",
    ]
    return "\n".join(lines) + "\n\n"


def main():
    printer = Network("192.168.1.175", profile="TSP600")  # Printer IP Address
    printer.text(build_ornate_box("\nBIG-8500:\n\naudit-logs pre-commit conda-lock pipeline issue\n") + "\n\n\n\n\n\n\n\n\n")
    printer.cut()


if __name__ == "__main__":
    main()
