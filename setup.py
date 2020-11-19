from distutils.core import setup

setup(
    name='dns_compare',
    version='0.0.4',
    author='Joe Miller, Dave van Duivenbode',
    author_email='joeym@joeym.net, dave.v.duivenbode@gmail.com',
    scripts=['dns_compare'],
    url='https://github.com/Sefiris/dns_compare',
    license='LICENSE',
    description="Compare data from a BIND zone file to data returned from a DNS server",
    long_description=open('README.md').read()
)
