#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf8
import http.server
import os
import re
import ssl
import sys
from platform import node
from time import sleep
from epics import PV
from datetime import datetime
from collections import OrderedDict

app_name = 'CLARA Machine Status Server'
author = 'Ben Shepherd'
author_email = 'ben.shepherd@stfc.ac.uk'
version_history = {
    '3.5': ('2022-03-22', 'report Python version'),
    '3.4': ('2021-11-30', 'tidy up code'),
    '3.3': ('2018-06-04', 'option for reset buttons in PVs'),
    '3.2': ('2018-02-01', 'HTML pages in separate files'),
    '3.1': ('2016-01-14', 'fixed issue with non-connected parameters, misinterpretation of NaNs'),
    '3.0': ('2015-06-23', 'converted to Python')}
version = max(version_history.keys())
python_version = '.'.join(str(x) for x in sys.version_info[:3])

if os.name == 'posix':
    # Help pyepics find the right library
    os.environ['PYEPICS_LIBCA'] = '/home/opt/EPICS/base/lib/linux-x86_64/libca.so'
else:  # network broadcast works on anywhere but apsv2
    os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"  # CLARA EPICS gateway

build_date = datetime.fromtimestamp(os.path.getmtime(__file__))
start_date = datetime.now().strftime('%d/%m/%y %H:%M:%S')


class StoppableServer(http.server.HTTPServer):
    def serve_forever(self, poll_interval=0.5):
        """Handle one request at a time until doomsday."""
        self.running = True
        while self.running:
            self.handle_request()


class MyHandler(http.server.BaseHTTPRequestHandler):
    params = {}
    pvs = OrderedDict()

    # Read in HTML snippets for status tables 
    # File names should be "status.nn.Region.html"
    # where nn is a number that will be used for sorting
    # Region names will be made into URLs, so no funny characters (like spaces)
    status_files = sorted([file for file in os.listdir('.')
                           if file.startswith('status.') and file.endswith('.html')])
    # A normal dict would do fine, except we want a particular order for the menu
    output = OrderedDict()
    for filename in status_files:
        region = filename.split('.')[2]
        output[region] = open(filename).read()

    # Define HTML headers and footers
    # Note the {{}} here - this will be replaced by the machine region
    # We also add a menu of all the regions, hence the final <p>
    header = open('header.html', 'r').read().format(app_name=app_name)
    footer = open('footer.html', 'r').read().format(**globals())

    # Parse output tables
    # Most PVs contain colon characters (:), but the format string won't parse these correctly.
    # We replace them here with a back tick (`), assuming this will never be found in a PV name.
    # We also replace a dot (.) with a NOT sign (¬)
    # The format code thus always needs to have a final colon, and a specifier
    # Valid examples: {INJ-MAG-DIP-01:SI:.3f}, {INJ-LSR-DLY-01:BCAL:s}
    # Invalid:  {INJ-MAG-DIP-01:SI}
    # (Some special cases exist where formatting is not enough to produce a
    #  nice output - see below.)

    curlyBrackets = re.compile(r'{([^}]*):(.*?)}')  # match PV name and format spec
    # use a new dict to store lower case region names
    # and correctly parsed PV names
    newOutput = {}
    for region, text in output.items():
        header += '<a href="/{0}.html">{0}</a> | '.format(region)
        params[region.lower()] = []
        matchedStrings = curlyBrackets.findall(text)
        for param, formatCode in matchedStrings:
            # add connection to this PV (if not already done)
            escapedParam = param.replace(':', '`')
            escapedParam = escapedParam.replace('.', '¬')
            if escapedParam not in pvs:
                # When formatCode is 'btn', we need to "press a button" to get an updated value for the PVs
                # The PV is stored inside a tuple in the dict to distinguish it from ordinary "get" PVs
                pvs[escapedParam] = (PV(param), 1, 0) if formatCode == 'btn' else PV(param)
            text = text.replace('{' + param + ':' + formatCode + '}',
                                '' if formatCode == 'btn' else ('{' + escapedParam + ':' + formatCode + '}'), 1)
            params[region.lower()].append(escapedParam)
        newOutput[region.lower()] = text
    output = newOutput

    header = header[0:-2] + '</p>'  # chop last |

    returnTypeRE = re.compile(r'\.(json|html)$')

    def do_HEAD(self):
        """Send HTML headers."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Send HTML response."""
        path, ext = os.path.splitext(self.path[1:].lower())  # strip leading /, case insensitive
        if path in self.output:
            output = self.get_status_table(path)
            if ext == '.html':
                output = self.wrap_content(output, path)
            else:
                output = '''elogInsertMachineStatus({{"status": "ok", "area": "{0}",
                            "params": '{1}'}})'''.format(path, output.replace('\n', '').replace('\r', ''))

        elif path == '':
            output = self.wrap_content()

        elif path == 'restart':
            # restart the server
            # serve a redirect page first
            output = open('restart.html', 'r').read().format(app_name=app_name)
            self.server.running = False

        elif path == 'environ':
            # show a list of environment variables
            row_format = '<tr><td>{0}</td><td>{1}</td></tr>'
            env_table = ''.join(row_format.format(key, value) for key, value in sorted(os.environ.items()))
            table_header = '<table><tr><th>Variable</th><th>Value</th></tr>'
            output = self.wrap_content(table_header + env_table + '</table>', path)

        elif path == 'version-history':
            # show the version history
            content = '<ul>' + ''.join('<li><b>' + ver + '</b>: ' + ', '.join(version_history[ver]) + '</li>'
                                       for ver in sorted(version_history.keys())) + '</ul>'
            output = self.wrap_content(content, 'Versions')

        else:
            # Default response
            output = self.wrap_content('<p>Invalid URL: /{}</p>'.format(path))

        self.do_HEAD()
        self.wfile.write(output if isinstance(output, bytes) else output.encode('utf-8'))

    def wrap_content(self, content='', title=''):
        """Add the standard header and footer to the given content."""
        return self.header.format(title + (' - ' if title else '')) + content + self.footer

    def get_status_table(self, path):
        """Compile a machine status table."""
        now_string = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        pv_values = {'timestamp': now_string}
        for param in self.params[path]:
            pv = self.pvs[param]
            print(pv)
            if isinstance(pv, tuple):  # This PV is a 'button' type - we have to set it to the given values
                pv, values = pv[0], pv[1:]
                for val in values:
                    pv.put(val)
                    sleep(0.1)  # short delay to mimic button press
                sleep(1)  # longer delay to let the updated values propagate
            pv_val = pv.get() if pv.connected else float('nan')

            # handle special cases
            # convert frequencies from Hz to MHz, and powers from W to MW
            if param in ('REBECA-LLRF`IN_FREQ', 'REBECA-LLRF`OUT_FREQ') or param.endswith('`power_remote_s¬POWER'):
                pv_val /= 1e6

            pv_values[param] = pv_val
        return self.output[path].format(now_string, **pv_values)


def machine_status_server():
    """Set up an HTTP(S) server to serve machine status pages."""
    port = 27643
    server = StoppableServer(('', port), MyHandler)

    filename = node().replace('.', '-')
    certfile = '/etc/pki/tls/certs/{0}.crt'.format(filename)
    keyfile = '/etc/pki/tls/private/{0}.key'.format(filename)
    try:
        server.socket = ssl.wrap_socket(server.socket, keyfile=keyfile, certfile=certfile, server_side=True)
        protocol = 'https'
    except IOError:
        protocol = 'http'
    print('Started server: try {protocol}://localhost:{port}/'.format(**locals()))
    try:
        server.serve_forever()  # until /restartServer requested
        del server

        # Restart the server
        args = sys.argv[:]
        args.insert(0, sys.executable)
        if sys.platform == 'win32':
            args = ['"%s"' % arg for arg in args]

        os.execv(sys.executable, args)

    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()


if __name__ == '__main__':
    machine_status_server()
