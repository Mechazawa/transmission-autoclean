from os import getenv
from time import sleep
from transmission_rpc import Client
from argparse import ArgumentParser, ArgumentTypeError


def main(args=None):
    if args is None:
        args = parse_arguments()
    else:
        args = {**parse_arguments(), **args}

    client = Client(**args)

    while True:
        print("Checking torrents...")
        unregistered = [t for t in client.get_torrents() if t.errorString == 'Unregistered torrent']
        print(f"Found {len(unregistered)} unregistered torrents")

        if len(unregistered) > 0:
            print("Deleting torrents")
            client.remove_torrent([t.id for t in unregistered], delete_data=args['delete'])

        if args['interval'] is None:
            break

        print(f"Sleeping for {args['interval']} minutes")
        sleep(args['interval'] * 60)


def check_interval(value):
    # value is probably already an int, but I'm too lazy to check
    ivalue = int(value)
    if ivalue < 1:
        raise ArgumentTypeError("Must be a positive integer greater then zero")
    return ivalue


def parse_arguments():
    parser = ArgumentParser()

    connection_group = parser.add_argument_group('connection')
    connection_group.add_argument('--secure', dest="protocol", action='store_const',
                                  const='https', default='http',
                                  help='Use https to connect to transmission')
    connection_group.add_argument('-u', '--username', dest='username', metavar='USER',
                                  help='username for authentication', default=getenv("USERNAME"))
    connection_group.add_argument('-p', '--password', dest='password', metavar='PASS',
                                  help='password for authentication', default=getenv("PASSWORD"))
    connection_group.add_argument('-H', '--host', dest='host', default=getenv("USERNAME", "127.0.0.1"),
                                  help='transmission rpc host')
    connection_group.add_argument('-P', '--port', dest='port', default=int(getenv("PORT", 9091)),
                                  help='transmission rpc port')
    connection_group.add_argument('--path', dest='path', default=getenv('URL_PATH', '/transmission/'),
                                  help='transmission rpc path')
    connection_group.add_argument('-t', '--timeout', dest='timeout', default=int(getenv('timeout', 30)))

    parser.add_argument('--delete', help='delete removed torrent files', action='store_true')
    parser.add_argument('-i', '--interval', type=int, default=int(getenv('INTERVAL')),
                        help='interval between runs in minutes, only runs once if not set')
    parser.add_argument('--debug', help='enable debug logging', action='store_true')

    args = vars(parser.parse_args())

    # apply flags
    if getenv('SECURE').lower().strip() == 'true':
        args['protocol'] = 'https'
    if getenv('DELETE').lower().strip() == 'true':
        args['delete'] = True

    return args


if __name__ == '__main__':
    main()
