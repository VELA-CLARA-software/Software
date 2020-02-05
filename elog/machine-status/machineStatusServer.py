#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf8
app_name = 'CLARA Machine Status Server'
author = 'Ben Shepherd'
version_history = {
    '3.3': ('2018-06-04', 'option for reset buttons in PVs'),
    '3.2': ('2018-02-01', 'HTML pages in separate files'),
    '3.1': ('2016-01-14', 'fixed issue with non-connected parameters, misinterpretation of NaNs'),
    '3.0': ('', 'converted to Python')}
version = max(version_history.keys())

import http.server
import os
import re
import ssl
import sys
from time import sleep
# import h5py
# import numpy as np
# import png
# from io import BytesIO
# import colorcet
# import imageio
# from PIL import Image

if os.name == 'posix':
    # Help pyepics find the right library
    os.environ['PYEPICS_LIBCA'] = '/home/opt/EPICS/base/lib/linux-x86_64/libca.so'
else:  # network broadcast works on anywhere but apsv2
    os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"  # CLARA EPICS gateway

from epics import PV
from datetime import datetime
from collections import OrderedDict

try:
    from urllib import parse
except ImportError:  # for Python 2
    import urlparse as parse

build_date = datetime.fromtimestamp(os.path.getmtime(__file__))
start_date = datetime.now().strftime('%d/%m/%y %H:%M:%S')

# fire = np.array([list(int(h[i:i + 2], 16) for i in (1, 3, 5)) for h in colorcet.fire], dtype='uint8').tobytes()


class StoppableServer(http.server.HTTPServer):
    def serve_forever(self):
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
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        path = self.path[1:].lower()  # strip leading /, case insensitive
        path_split = self.returnTypeRE.split(path)
        return_type = path_split[1] if len(path_split) > 1 else ''
        path = path_split[0]
        html_output = (return_type == 'html' or path == '')

        if path in self.output:
            now_string = datetime.now().strftime('%d/%m/%y %H:%M:%S')
            pv_values = {'timestamp': now_string}
            for param in self.params[path]:
                #                print(param)
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
                # report a nicely formatted value for the train length
                # in micro- or nanoseconds
                # if param == 'INJ-LSR-DLY-01`BCAL':
                # if pv_val < 1:
                # pv_val = '{:.0f} ns'.format(pv_val * 1000)
                # elif pv_val >= 1:
                # pv_val = '{:.0f} &mu;s'.format(pv_val)
                # else:
                # pv_val = 'N/A'

                # status of burst generator
                # elif param == 'INJ-LSR-POC-01`RRUN':
                # if pv_val == -1:
                # pv_val = 'On'
                # elif pv_val == 0:
                # pv_val = 'Off'
                # else:
                # pv_val = 'N/A'

                pv_values[param] = pv_val

            #            print(self.output[path])
            #            print(pv_values)
            output = self.output[path].format(now_string, **pv_values)
            if html_output:
                self.sendOutput("text/html", self.header.format(path + ' - ') + output + self.footer)
            else:
                output = '''elogInsertMachineStatus(
                            {{"status": "ok",
                              "area": "{0}",
                              "params": '{1}'}})'''.format(path, output.replace('\n', '').replace('\r', ''))
                self.sendOutput("text/html", output)

        elif path == '':
            self.sendOutput("text/html", self.header.format('') + self.footer)

        # elif path.startswith('cameraimages/'):
            # parsed = parse.urlparse(path)
            # file_path = '//claraserv3/' + parse.unquote(parsed.path)
            # file_path = 'c:/users/bjs54/' + parse.unquote(parsed.path)  # for debugging
            # query = dict(parse.parse_qsl(parsed.query))
            # if file_path.endswith('.hdf5'):
                # # Read an HDF5 image file and return it as a browser-friendly format
                # content_type = 'image/gif'
                # with h5py.File(file_path, 'r') as h5file:
                    # dataset_names = [k for k in h5file.keys() if k.startswith('Capture')]
                    # return_width = None
                    # min_level, max_level = 2**16 - 1, 0
                    # for i, name in enumerate(dataset_names):
                        # dataset = np.array(h5file[name])
                        # if return_width is None:
                            # height, width = dataset.shape
                            # try:
                                # width_param = query['width']
                                # return_width = width if width_param == 'o' else min(width, int(width_param))
                            # except (KeyError, ValueError):
                                # return_width = 32
                            # step = width // return_width  # how many rows/cols to skip along
                        # min_level = min(min_level, np.min(dataset[::step, ::step]))
                        # max_level = max(max_level, np.percentile(dataset[::step, ::step], 99.9))
                        # print(min_level, max_level)

                    # factor = 255.0 / (max_level - min_level)
                    # print(min_level, max_level, factor)
                    # self.sendOutput('image/gif', '')
                    # for name in dataset_names:
                        # print(name)
                        # dataset = np.array(h5file[name])
                        # icon_data = np.asarray(np.clip(dataset[::step, ::step] * factor, 0, 255), 'uint8')
                        # frame = Image.fromarray(icon_data, mode='P')  # palette mode
                        # str_buffer = BytesIO()
                        # frame.save(str_buffer, format='gif', palette=fire, loop=0, append=True)
                        # self.sendOutput('', str_buffer.getvalue())
                        
                # # Compress the range to (0, 255) for an 8-bit icon
                # # min_val = np.min(data)
                # # subtracted = data - min_val
                # # factor = np.percentile(subtracted, 99.9) / 256  # 0.1% of pixels are saturated
                # # icon_data = np.asarray(np.clip(subtracted / factor, 0, 255), 'uint8')
                # # str_buffer = BytesIO()
                # # frames = [Image.fromarray(frame, mode='P') for frame in icon_data]  # palette mode
                # # # loop forever
                # # frames[0].save(str_buffer, format='gif', save_all=True, append_images=frames[1:], palette=fire, loop=0)
                # # # png.Writer(*reversed(icon_data.shape), palette=fire).write(str_buffer, icon_data)
                # # # imageio.imwrite(str_buffer, icon_data, format='gif')
                # # output = str_buffer.getvalue()
                # # str_buffer.close()
            # else:  # must be a folder
                # # List HDF5 files in specified work folder, in JSON format
                # # This is used to provide the eLog with a built-in image browser
                # files = os.listdir(file_path)
                # output = '''elogWorkFolderListing(
                            # {{"status": "ok",
                              # "folder": "{0}",
                              # "files": [\n'''.format(file_path.replace('\\', '/'))
                # for filename in files:
                    # if filename.lower().endswith('.hdf5'):
                        # output += '\t\t\t\t\t"{0}", \n'.format(filename)
                # output = output[:-3] + ']})'
                # self.sendOutput('text/javascript', output)

        elif path == 'restart':
            # restart the server
            # serve a redirect page first
            self.sendOutput("text/html", open('restart.html', 'r').read().format(app_name=app_name))
            self.server.running = False

        #        elif path == 'favicon.ico':
        #            # Serve a favicon (this doesn't work)
        #            content_type = "image/ico"
        #            output = open('Alice_Logo.ico', 'rb').read()
        elif path == 'environ':
            # show a list of environment variables
            row_format = '<tr><td>{0}</td><td>{1}</td></tr>'
            env_table = ''.join([row_format.format(key, value) for key, value in sorted(os.environ.items())])
            table_header = '<table><tr><th>Variable</th><th>Value</th></tr>'
            output = self.header.format(path + ' - ') + table_header + env_table + '</table>' + self.footer
            self.sendOutput("text/html", output)

        else:
            # Default response
            self.sendOutput("text/html", (self.header.format('') + '<p>Invalid URL: /{}</p>'.format(path) + self.footer))

    def sendOutput(self, content_type, output):
        if content_type:
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
        self.wfile.write(output if isinstance(output, bytes) else output.encode('utf-8'))


port = 27643
server = StoppableServer(('', port), MyHandler)

certfile = '/etc/pki/tls/certs/apsv2-dl-ac-uk.crt'
keyfile = '/etc/pki/tls/private/apsv2-dl-ac-uk.key'
try:
    server.socket = ssl.wrap_socket(server.socket, keyfile=keyfile, certfile=certfile, server_side=True)
    protocol = 'https'
except IOError:
    protocol = 'http'
print('Started server: try {protocol}://localhost:{port}/'.format(**locals()))
try:
    server.serve_forever()  # until /restartServer requested
    del(server)

    # Restart the script
    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]

    os.execv(sys.executable, args)

except KeyboardInterrupt:
    print('^C received, shutting down server')
    server.socket.close()
