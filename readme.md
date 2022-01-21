# (Hopefully someday) Full Socks5 proxy implementation

## Description

- Uses low-level sockets
- Accepts no-auth and user-password without actual authentication
- Spawns threads for incoming and outgoing data after connection
- Tries to resolve FQDNs to ip addresses
- IPv4 only at the moment
- Tries to be RFC1928-compliant. Does NOT, however, support GSSAPI auth

## Usage

1. Run python3 fivesocks.py
2. Run curl -x socks5://username:password@127.0.0.1:9090 http://example.com

## RFC Compliance
- MUST support GSSAPI authentication
+ SHOULD support Username/Password
- requests MUST be encapsulated in the method-dependent encapsulation
- server MUST terminate TCP connection shortly after detecting failure condition
- the server MUST encapsulate the data as appropriate for the authentication method in use
- The UDP relay server MUST acquire from the SOCKS server the expected IP address of the client that will send datagrams to the BND.PORT given in the reply to UDP ASSOCIATE
- It MUST drop any datagrams arriving from any source IP address other than the one recorded for the particular association.

## Roadmap
- Authentication NONE - done
- Authentication GSSAPI
- Authentication Username/Password
  - Support connections using this - done
  - Actually do authentication
- Request command:
  - CONNECT - done
  - BIND
  - UDP ASSOCIATE
- Request address type:
  - IPv4 - done
  - DOMAINNAME - done
  - IPv6
- Reply field:
  - X'00' succeeded - done
  - X'01' general SOCKS server failure
  - X'02' connection not allowed by ruleset
  - X'03' Network unreachable
  - X'04' Host unreachable
  - X'05' Connection refused
  - X'06' TTL expired
  - X'07' Command not supported
  - X'08' Address type not supported
- Stay within the python3 standard library
  - or at least OS standard libraries
