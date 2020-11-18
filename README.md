dns_compare
==============
Compare data from a BIND zone file to data returned by an authoritative DNS server.

Now with 2020 Python3 support and deprecated functions fixed.

Purpose
-------
Use this tool to verify the data being returned by an authoritative DNS server matches
the data in a zone file.

Motivation
----------
It is very helpful when migrating from one DNS server to another to be able to
verify that all records imported correctly.

In my case(Joe Miller), I used this tool to help me migrate multiple domains from
Windows 2000 DNS and GoDaddy DNS (which both export BIND zone files) into Amazon's
Route53 DNS service.  With this tool, I could confidently prove that all records
properly imported into Route53 before changing the whois records for each domain.

My case(Dave van Duivenbode) is kind of the same but a little bit more modern moving from
Cloudflare DNS services to Azure DNS, cloudflare supports exporting a BIND zone file
that requires very slight tweaking to get imported by this script. this is covered below in
the `Example cloudflare exported file` section

Installation
------------
    pip install git+https://github.com/Sefiris/dns_compare.git#egg=dns_compare


Example Usage:
--------------
Basic operation:

    $ dns_compare -z example.com --file example.com.zone --server 10.1.1.1
    ............................................X
    (MIS-MATCH) query: nss4.example.com.
     Expected:  300 IN A 142.229.40.28
     Received:  900 IN A 142.229.40.28
    ...X
    (MIS-MATCH) query: www.example.com.
     Expected:  200 IN A 91.139.129.128
     Received:  900 IN A 91.139.129.128
    X
    (MIS-MATCH) query: www.example.com.
     Expected:  300 IN AAAA 2001:4800:1078:2256:78C8:1542:FF04:6BCB
     Received:  900 IN AAAA 2001:4800:1078:2256:78c8:1542:ff04:6bcb
    ......................done

    Results:
    Matches:      69
    Mis-matches:  3

Verbose:

    $ dns_compare -z example.com --file example.com.zone --server 10.1.1.1 --verbose
	----
	(Match) query: www.example.com. ...
	Expected:  0 IN CNAME example.com.
	Received:  0 IN CNAME example.com.
	----
	(MIS-MATCH) query: example.com. ...
	Expected:  60 IN A 10.0.0.1
	Got     :  60 IN A 10.0.0.20

By default, SOA and NS records are ignored because these records are likely
to change when migrating a zone between DNS services..  Specify `--soa` or `--ns` option,
respectively, to enable checking of SOA and NS records.

Comparing TTLs can be disabled with `-t` option. This is useful when transferring DNS to a provider
that offers only specific TTL values.

Example cloudflare exported file:
--------------
    ;;
    ;; Domain:     example.io.
    ;; Exported:   2020-11-17 10:24:21
    ;;
    ;; This file is intended for use for informational and archival
    ;; purposes ONLY and MUST be edited before use on a production
    ;; DNS server.  In particular, you must:
    ;;   -- update the SOA record with the correct authoritative name server
    ;;   -- update the SOA record with the contact e-mail address information
    ;;   -- update the NS record(s) with the authoritative name servers for this domain.
    ;;
    ;; For further information, please consult the BIND documentation
    ;; located on the following website:
    ;;
    ;; http://www.isc.org/
    ;;
    ;; And RFC 1035:
    ;;
    ;; http://www.ietf.org/rfc/rfc1035.txt
    ;;
    ;; Please note that we do NOT offer technical support for any use
    ;; of this zone data, the BIND name server, or any other third-party
    ;; DNS software.
    ;;
    ;; Use at your own risk.
    ;; SOA Record

    $TTL 36000
    example.io. IN      SOA     joan.ns.cloudflare.com. root.example.io. (
                2005081201      ; serial
                28800   ; refresh (8 hours)
                1800    ; retry (30 mins)
                2592000 ; expire (30 days)
                86400 ) ; minimum (1 day)

    example.io. 86400 NS joan.ns.cloudflare.com
    example.io. 86400 NS aiden.ns.cloudflare.com

    ;;example.io.	3600	IN	SOA	example.io. root.example.io. 2035727526 7200 3600 86400 3600

    ;; A Records
    example.io.	1	IN	A	37.97.254.27
    test-api.example.io.	1	IN	A	195.177.214.37

    ;; CNAME Records
    status.example.io.	1	IN	CNAME	status.azurewebsites.net.

    ;; MX Records
    example.io.	1	IN	MX	0 example-io.mail.protection.outlook.com.

    ;; SRV Records
    _sipfederationtls._tcp.example.io.	1	IN	SRV	100 1 5061 sipfed.online.lync.com.
    _sip._tls.example.io.	1	IN	SRV	100 1 443 sipdir.online.lync.com.

    ;; TXT Records
    example.io.	1	IN	TXT	"v=spf1 include:spf.protection.outlook.com ip4:1.1.1.1/26 -all"
    status.example.io.	1	IN	TXT	"status.azurewebsites.net"

When an export is made from cloudflare they purposefully do not include a default global TTL, SOA and NS records. These will have to be added manually.
All other records are correctly exported in the BIND format. the only problems i've encountered so far are lines being too long in TXT SPF records

Authors
------
Joe Miller [Github](http://github.com/joemiller) [Joe Miller](http://joemiller.me) [Twitter](https://twitter.com/miller_joe)

Dave van Duivenbode [Github](https://github.com/Sefiris) [Twitter](https://twitter.com/Sefiris)
