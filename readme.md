# (Hopefully someday) Full Socks5 proxy implementation

## Description

- Uses low-level sockets
- Accepts no-auth and user-password without actual authentication
- Spawns threads for incoming and outgoing data after connection
- Tries to resolve FQDNs to ip addresses
- IPv4 only at the moment
- Tries to be RFC1928-compliant. Does NOT, however, support GSSAPI auth

## Usage

1. Run python3 socket_server.py
2. Run curl -x socks5://username:password@127.0.0.1:9090 http://example.com
