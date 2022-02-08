from mailer import Mailer

def main() -> int:
    Mailer().command_line_interface()
    return 0

if __name__ == '__main__':
    status_code = main()
    print(f'{status_code=}')