# run v2.6
from starboard import *


def main():
    DAS = Dashboard()
    while True:
        try:
            try:
                DAS.render_board()
            except requests.exceptions.ConnectionError:
                connection_error()
                continue
            time.sleep(600)
        except KeyboardInterrupt:
            usr_interrupt()
            continue


if __name__ == '__main__':
    main()
