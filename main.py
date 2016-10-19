#!/usr/bin/env python3

from osmparser import fetcher

def main():
    response = fetcher.fetch_bounded_box_map(-123.231508, 49.257094, -123.196980, 49.25777)
    print(response)
    print(response.text)

if __name__ == '__main__':
    main()
