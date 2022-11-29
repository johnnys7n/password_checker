import requests
import hashlib
import sys
import os

input = sys.argv[1]

# converts text file into list of passwords to test


def read_txt_file(file):
    try:
        with open(file, mode='r', encoding='utf-8') as my_file:
            lines = my_file.read().splitlines()
            return lines
    except:
        print('this is not working')


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {res.status_code}, check the api and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    # use tuple comprehension to split the line into hash and count
    # this outputs a generator object that can be looped through
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    # check password if it exists in API response
    sha1password = hashlib.sha1(password.encode(
        'utf-8')).hexdigest().upper()  # converts password to sha1
    # we only need the first five characters
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(
                f'{password} was found {count} times... you need to change password ASAP!')
        else:
            print(f'{password} was NOT found!...yet')
    return 'done!'


if __name__ == '__main__':
    sys.exit(main(read_txt_file(input)))
