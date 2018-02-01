#!python
# -*- coding: utf-8 -*-
# encoding=utf8
app_name = 'CLARA Machine Status Server'
author = 'Ben Shepherd'
version_history = {
    '3.2': ('2018-02-01', 'HTML pages in separate files'),
    '3.1': ('2016-01-14', 'fixed issue with non-connected parameters, misinterpretation of NaNs'),
    '3.0': ('', 'converted to Python')}
version = max(version_history.keys())

import http.server
import ssl
import re
import sys, os
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"  # CLARA EPICS gateway
if os.name == 'posix':
    # Help pyepics find the right library
    os.environ['PYEPICS_LIBCA'] = '/home/opt/EPICS/base/lib/linux-x86_64/libca.so'
from epics import PV
from datetime import datetime
from time import sleep
from collections import OrderedDict
#from SysTrayIcon import SysTrayIcon
try:
    from urllib import parse
except ImportError:  # for Python 2
    import urlparse as parse

build_date = datetime.fromtimestamp(os.path.getmtime(__file__))
start_date = datetime.now().strftime('%d/%m/%y %H:%M:%S')


class StoppableServer(http.server.HTTPServer):
    def serve_forever(self):
        """Handle one request at a time until doomsday."""
        self.running = True
        while self.running:
            self.handle_request()


class MyHandler(http.server.BaseHTTPRequestHandler):

    params = {}
    pvs = {}

    # Read in HTML snippets for status tables 
    # Filenames should be "status.nn.Region.html"
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
    # We replace them here with a backtick (`), assuming this will never be found in a PV name.
    # We also replace a dot (.) with a NOT sign (¬)
    # The format code thus always needs to have a final colon, and a specifier
    # Valid examples: {INJ-MAG-DIP-01:SI:.3f}, {INJ-LSR-DLY-01:BCAL:s}
    # Invalid:  {INJ-MAG-DIP-01:SI}
    # (Some special cases exist where formatting is not enough to produce a
    #  nice output - see below.)

    curlyBrackets = re.compile(r'{([^}]*):(.*?)}') #match PV name and format spec
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
            if not escapedParam in pvs:
                pvs[escapedParam] = PV(param)
            text = text.replace('{' + param + ':' + formatCode + '}',
                                '{' + escapedParam + ':' + formatCode + '}', 1)
            params[region.lower()].append(escapedParam)
        newOutput[region.lower()] = text
    output = newOutput

    header = header[0:-2] + '</p>' #chop last |

    returnTypeRE = re.compile(r'\.(json|html)$')

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_GET(self):
        path = self.path[1:].lower() #strip leading /, case insensitive
        pathSplit = self.returnTypeRE.split(path)
        returnType = pathSplit[1] if len(pathSplit) > 1 else ''
        path = pathSplit[0]
        htmlOutput = (returnType == 'html' or path == '')

        if path in self.output:
            nowString = datetime.now().strftime('%d/%m/%y %H:%M:%S')
            pvValues = {'timestamp': nowString}
            for param in self.params[path]:
#                print(param)
                pv = self.pvs[param]
                print(pv)
                if not pv.connected:
                    pvVal = float('nan')
                else:
                    pvVal = pv.get()
                # handle special cases
                # report a nicely formatted value for the train length
                # in micro- or nanoseconds
                # if param == 'INJ-LSR-DLY-01`BCAL':
                    # if pvVal < 1:
                        # pvVal = '{:.0f} ns'.format(pvVal * 1000)
                    # elif pvVal >= 1:
                        # pvVal = '{:.0f} &mu;s'.format(pvVal)
                    # else:
                        # pvVal = 'N/A'

                # status of burst generator
                # elif param == 'INJ-LSR-POC-01`RRUN':
                    # if pvVal == -1:
                        # pvVal = 'On'
                    # elif pvVal == 0:
                        # pvVal = 'Off'
                    # else:
                        # pvVal = 'N/A'

                pvValues[param] = pvVal

#            print(self.output[path])
#            print(pvValues)
            output = self.output[path].format(nowString, **pvValues)
            if htmlOutput:
                contentType = "text/html"
                output = self.header.format(path + ' - ') + output + self.footer
            else:
#                contentType = 'text/javascript'
                contentType = "text/html"
                output = '''elogInsertMachineStatus(
                            {{"status": "ok",
                              "area": "{0}",
                              "params": '{1}'}})'''.format(path, output.replace('\n', ''))

        elif path == '':
            contentType = "text/html"
            output = self.header.format('') + self.footer

        elif path[0:5] == 'work/':
            contentType = 'text/javascript'
            # List PNG files in specified work folder, in JSON format
            # This is used to provide the eLog with a built-in image browser
            folder = parse.unquote('//dlfiles03/alice/' + path)
            files = os.listdir(folder)
            output = '''elogWorkFolderListing(
                        {{"status": "ok",
                      "folder": "{0}",
                      "files": [  '''.format(folder.replace('\\', '/'))
            for file in files:
                if file[-4:].lower() == '.png':
                    output += '\t\t"{0}", \n'.format(file)
            output = output[0:-3] + ']})'

        elif path == 'restart':
            # restart the server
            # serve a redirect page first
            contentType = "text/html"
            output = open('restart.html', 'r').read().format(app_name=app_name)
            self.server.running = False

#        elif path == 'favicon.ico':
#            # Serve a favicon (this doesn't work)
#            contentType = "image/ico"
#            output = open('Alice_Logo.ico', 'rb').read()

        else:
            # Default response
            contentType = "text/html"
            output = (self.header.format('') +
                      '<p>Invalid URL: /{0}</p>'.format(path) + self.footer)

        self.send_response(200)
        self.send_header("Content-type", contentType)
        self.end_headers()
        self.wfile.write(output.encode('utf-8'))

try:
    port = 27643
    server = StoppableServer(('', port), MyHandler)
    certfile = '/etc/pki/tls/certs/apsv2-dl-ac-uk.crt'
    keyfile = '/home/bjs54/apsv2-dl-ac-uk.key'
    try:
        server.socket = ssl.wrap_socket(server.socket, keyfile=keyfile, certfile=certfile, server_side=True)
        protocol = 'https'
    except IOError:
        protocol = 'http'
    print('Started server: try {protocol}://localhost:{port}/'.format(**locals()))
    server.serve_forever()  # until /restartServer requested
    sleep(2)

    # Restart the script
    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]

    os.execv(sys.executable, args)

except KeyboardInterrupt:
    print('^C received, shutting down server')
    server.socket.close()

