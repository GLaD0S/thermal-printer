import argparse
import os
import sys

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


def ticket(message: str | None = None, jira_code: str | None = None, time_estimate: str | None = None) -> str:
    ticket_text = ""
    if jira_code:
        ticket_text += f"\n\n{jira_code}:\n"

    if message:
        ticket_text += f"\n{message}\n"

    if time_estimate:
        ticket_text += f"\nTime: {time_estimate}\n\n"

    return build_ornate_box(f"{ticket_text}") + "\n\n\n\n\n\n\n\n\n"


def main() -> None:
    default_host = os.environ.get("THERMAL_PRINTER_HOST", "192.168.1.175")

    parser = argparse.ArgumentParser(
        description="Print a framed ticket on a network ESC/POS thermal printer.",
    )
    parser.add_argument(
        "--host",
        default=default_host,
        help=f"Printer IP or hostname (default: {default_host}, or THERMAL_PRINTER_HOST).",
    )
    parser.add_argument(
        "--profile",
        default="TSP600",
        help="python-escpos printer profile name (default: %(default)s).",
    )
    parser.add_argument("-m", "--message", help="Main ticket text.")
    parser.add_argument("-j", "--jira-code", help="Jira issue key or label printed at the top.")
    parser.add_argument("-t", "--time-estimate", help="Time estimate line.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write ticket text to stdout instead of printing.",
    )
    parser.add_argument(
        "--no-cut",
        action="store_true",
        help="Do not send a cut command after printing.",
    )
    args = parser.parse_args()

    if not any([args.message, args.jira_code, args.time_estimate]):
        parser.error("Provide at least one of: --message, --jira-code, --time-estimate")

    text = ticket(
        message=args.message,
        jira_code=args.jira_code,
        time_estimate=args.time_estimate,
    )

    if args.dry_run:
        sys.stdout.write(text)
        return

    printer = Network(args.host, profile=args.profile, port=9100, timeout=5)
    printer.text(text)
    if not args.no_cut:
        printer.cut()


if __name__ == "__main__":
    main()
