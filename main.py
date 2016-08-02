#!/usr/bin/env python3

import fetcher


def main():
    response = fetcher.fetch_bounded_box_map(-123.125180, 49.275600, -123.122176, 49.277574)
    print(response)
    print(response.text)

if __name__ == '__main__':
    main()