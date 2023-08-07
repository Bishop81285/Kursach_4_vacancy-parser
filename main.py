from utils.user_interface import interact


def main():
    status = interact()

    if status:
        main()


if __name__ == '__main__':
    main()
