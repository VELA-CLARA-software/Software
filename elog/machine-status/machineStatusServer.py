# Machine Status Server, v3.1
# Ben Shepherd, 2015
# version history:
# 3.1 (14/1/16): fixed issue with non-connected parameters, misinterpretation of NaNs
# 3.0: converted to Python

import http.server
import ssl
import re
import sys, os
from epics import PV
from datetime import datetime
from time import sleep
from collections import OrderedDict
#from SysTrayIcon import SysTrayIcon
from urllib import parse

class StoppableServer(http.server.HTTPServer):
    def serve_forever(self):
        """Handle one request at a time until doomsday."""
        self.running = True
        while self.running:
            self.handle_request()


class MyHandler(http.server.BaseHTTPRequestHandler):

    params = {}
    pvs = {}

    # A normal dict would do fine, except we want a particular order for the menu
    # Region names will be made into URLs, so no funny characters (like spaces)
    output = OrderedDict([
    ('Gun', '''<table class="machine-status gun">
        <tr><th class="msTitle" colspan="5">Gun Status</th><th class="msDateTime" colspan="6">{timestamp}</th></tr>
        <tr><td>Gun HV<br><strong>{INJ-GUN-HVPSU-01-IncV:.0f}kV</strong></td><td>Laser Att.<br><strong>{INJ-LSR-ATT-01:S2TI:.2f}</strong></td>
        <td>Burst Gen<br><strong>{INJ-LSR-POC-01:RRUN:s}, &divide; {INJ-LSR-POC-01:RDIV:.0f}</strong></td><td>Train<br><strong>{INJ-LSR-DLY-01:BCAL:s}</strong></td>
        <td colspan="2">Laser H/V<br><strong>{INJ-LSR-HTM-01:RPOS:.0f}</strong> / <strong>{INJ-LSR-VTM-01:RPOS:.0f} steps</strong></td>
        <td>SOL-01<br><strong>{INJ-MAG-SOL-01:SI:.3f}</strong></td><td>SOL-02<br><strong>{INJ-MAG-SOL-02:SI:.3f}</strong></td>
        <td>VHCOR-01<br><strong>{INJ-MAG-VCOR-01:SI:.3f}</strong> / <strong>{INJ-MAG-HCOR-01:SI:.3f}</strong></td><td>VHCOR-06<br><strong>{INJ-MAG-VCOR-06:SI:.3f}</strong> / <strong>{INJ-MAG-HCOR-06:SI:.3f}</strong></td>
        <td>VHCOR-02<br><strong>{INJ-MAG-VCOR-02:SI:.3f}</strong> / <strong>{INJ-MAG-HCOR-02:SI:.3f}</strong></td></tr></table>'''),

    ('Injector', '''<table class="machine-status injector">
        <tr><th class="msTitle" colspan="6">Injector Status</th><th class="msDateTime" colspan="6">{timestamp}</th></tr>
        <tr><td>Q-01<br><strong>{INJ-MAG-QUAD-01:SI:.3f}</strong></td><td>Q-02<br><strong>{INJ-MAG-QUAD-02:SI:.3f}</strong></td><td>Q-03<br><strong>{INJ-MAG-QUAD-03:SI:.3f}</strong></td>
        <td>Q-04<br><strong>{INJ-MAG-QUAD-04:SI:.3f}</strong></td><td>Q-05<br><strong>{INJ-MAG-QUAD-05:SI:.3f}</strong></td><td>Q-06<br><strong>{INJ-MAG-QUAD-06:SI:.3f}</strong></td>
        <td>Q-07<br><strong>{INJ-MAG-QUAD-07:SI:.3f}</strong></td><td>Q-08<br><strong>{INJ-MAG-QUAD-08:SI:.3f}</strong></td><td>Q-09<br><strong>{INJ-MAG-QUAD-09:SI:.3f}</strong></td>
        <td>Q-10<br><strong>{INJ-MAG-QUAD-10:SI:.3f}</strong></td><td>Q-11<br><strong>{INJ-MAG-QUAD-11:SI:.3f}</strong></td><td>Q-12<br><strong>{INJ-MAG-QUAD-12:SI:.3f}</strong></td></tr>
        <tr><td colspan="2">DIP-01<br><strong>{INJ-MAG-DIP-01:SI:.3f}</strong></td><td colspan="2">DIP-02<br><strong>{INJ-MAG-DIP-02:SI:.3f}</strong></td>
        <td colspan="2">DIP-03<br><strong>{INJ-MAG-DIP-03:SI:.3f}</strong></td><td colspan="2">ST4-DIP-01<br><strong>{ST4-MAG-DIP-01:SI:.3f}</strong></td>
        <td colspan="2">DIP-02<br><strong>{ST4-MAG-DIP-02:SI:.3f}</strong></td><td colspan="2">DIP-03<br><strong>{ST4-MAG-DIP-03:SI:.3f}</strong></td></tr>
        <tr><td colspan="4">VHCOR-03<br><strong>{INJ-MAG-VCOR-03:SI:.3f}</strong> / <strong>{INJ-MAG-HCOR-03:SI:.3f}</strong></td>
        <td colspan="4">VHCOR-04<br><strong>{INJ-MAG-VCOR-04:SI:.3f}</strong> / <strong>{INJ-MAG-HCOR-04:SI:.3f}</strong></td>
        <td colspan="4">VHCOR-05<br><strong>{INJ-MAG-VCOR-05:SI:.3f}</strong> / <strong>{INJ-MAG-HCOR-05:SI:.3f}</strong></td></tr></table>'''),

    ('ST1', '''<table class="machine-status st1">
        <tr><th class="msTitle" colspan="5">Straight 1 Status</th><th class="msDateTime" colspan="4">{timestamp}</th></tr>
        <tr><td>Q-01<br><strong>{ST1-MAG-QUAD-01:SI:.3f}</strong></td><td>Q-02<br><strong>{ST1-MAG-QUAD-02:SI:.3f}</strong></td><td>Q-03<br><strong>{ST1-MAG-QUAD-03:SI:.3f}</strong></td>
        <td>Q-04<br><strong>{ST1-MAG-QUAD-04:SI:.3f}</strong></td><td>DIP-01<br><strong>{ST1-MAG-DIP-01:SI:.3f}</strong></td><td>DIP-02<br><strong>{ST1-MAG-DIP-02:SI:.3f}</strong></td>
        <td>DIP-03<br><strong>{ST1-MAG-DIP-03:SI:.3f}</strong></td><td>VHCOR-01<br><strong>{ST1-MAG-VCOR-01:SI:.3f}</strong> / <strong>{ST1-MAG-HCOR-01:SI:.3f}</strong></td>
        <td>VHCOR-02<br><strong>{ST1-MAG-VCOR-02:SI:.3f}</strong> / <strong>{ST1-MAG-HCOR-02:SI:.3f}</strong></td></tr></table>'''),

    ('ARC1', '''<table class="machine-status arc1">
        <tr><th class="msTitle" colspan="5">Arc 1 Status</th><th class="msDateTime" colspan="6">{timestamp}</th></tr>
        <tr><td>Q-01<br><strong>{AR1-MAG-QUAD-01:SI:.3f}</strong></td><td>Q-02<br><strong>{AR1-MAG-QUAD-02:SI:.3f}</strong></td><td>Q-03<br><strong>{AR1-MAG-QUAD-03:SI:.3f}</strong></td>
        <td>Q-04<br><strong>{AR1-MAG-QUAD-04:SI:.3f}</strong></td><td>DIP-01<br><strong>{AR1-MAG-DIP-01:SI:.3f}</strong></td><td>DIP-02<br><strong>{AR1-MAG-DIP-02:SI:.3f}</strong></td>
        <td>DIP-03<br><strong>{AR1-MAG-DIP-03:SI:.3f}</strong></td><td>VC-01<br><strong>{AR1-MAG-VCOR-01:SI:.3f}</strong></td>
        <td>VC-02<br><strong>{AR1-MAG-VCOR-02:SI:.3f}</strong></td><td>SEXT-01<br><strong>{AR1-MAG-SEXT-01:SI:.3f}</strong></td><td>SEXT-02<br><strong>{AR1-MAG-SEXT-02:SI:.3f}</strong></td></tr></table>'''),

    ('ST2', '''<table class="machine-status st2">
        <tr><th class="msTitle" colspan="5">Straight 2 Status</th><th class="msDateTime" colspan="6">{timestamp}</th></tr>
        <tr><td>Q-01<br><strong>{ST2-MAG-QUAD-01:SI:.3f}</strong></td><td>Q-02<br><strong>{ST2-MAG-QUAD-02:SI:.3f}</strong></td><td>Q-03<br><strong>{ST2-MAG-QUAD-03:SI:.3f}</strong></td>
        <td>Q-04<br><strong>{ST2-MAG-QUAD-04:SI:.3f}</strong></td><td>Q-05<br><strong>{ST2-MAG-QUAD-05:SI:.3f}</strong></td><td>Q-06<br><strong>{ST2-MAG-QUAD-06:SI:.3f}</strong></td>
        <td>Q-07<br><strong>{ST2-MAG-QUAD-07:SI:.3f}</strong></td><td>DIP-01<br><strong>{ST2-MAG-DIP-01:SI:.3f}</strong></td><td>DIP-02<br><strong>{ST2-MAG-DIP-02:SI:.3f}</strong></td>
        <td>DIP-03<br><strong>{ST2-MAG-DIP-03:SI:.3f}</strong></td><td>DIP-04<br><strong>{ST2-MAG-DIP-04:SI:.3f}</strong></td></tr>
        <tr><td colspan="3">VHCOR-01<br><strong>{ST2-MAG-VCOR-01:SI:.3f}</strong> / <strong>{ST2-MAG-HCOR-01:SI:.3f}</strong></td>
        <td colspan="3">VHCOR-02<br><strong>{ST2-MAG-VCOR-02:SI:.3f}</strong> / <strong>{ST2-MAG-HCOR-02:SI:.3f}</strong></td>
        <td>VCOR-03<br><strong>{ST2-MAG-VCOR-03:SI:.3f}</strong></td><td colspan="2">VHCOR-04<br><strong>{ST2-MAG-VCOR-04:SI:.3f}</strong> / <strong>{ST2-MAG-HCOR-04:SI:.3f}</strong></td>
        <td colspan="2">VHCOR-05<br><strong>{ST2-MAG-VCOR-05:SI:.3f}</strong> / <strong>{ST2-MAG-HCOR-05:SI:.3f}</strong></td></tr></table>'''),

    ('ST3', '''<table class="machine-status st3">
        <tr><th class="msTitle" colspan="3">Straight 3 Status</th><th class="msDateTime" colspan="3">{timestamp}</th></tr>
        <tr><td>Q-01<br><strong>{ST3-MAG-QUAD-01:SI:.3f}</strong></td><td>Q-02<br><strong>{ST3-MAG-QUAD-02:SI:.3f}</strong></td><td>Q-03<br><strong>{ST3-MAG-QUAD-03:SI:.3f}</strong></td>
        <td>Q-04<br><strong>{ST3-MAG-QUAD-04:SI:.3f}</strong></td><td>VHCOR-01<br><strong>{ST3-MAG-VCOR-01:SI:.3f}</strong> / <strong>{ST3-MAG-HCOR-01:SI:.3f}</strong></td>
        <td>VHCOR-02<br><strong>{ST3-MAG-VCOR-02:SI:.3f}</strong> / <strong>{ST3-MAG-HCOR-02:SI:.3f}</strong></td></tr></table>'''),

    ('ARC2', '''<table class="machine-status arc2">
        <tr><th class="msTitle" colspan="5">Arc 2 Status</th><th class="msDateTime" colspan="6">{timestamp}</th></tr>
        <tr><td>Q-01<br><strong>{AR2-MAG-QUAD-01:SI:.3f}</strong></td><td>Q-02<br><strong>{AR2-MAG-QUAD-02:SI:.3f}</strong></td><td>Q-03<br><strong>{AR2-MAG-QUAD-03:SI:.3f}</strong></td>
        <td>Q-04<br><strong>{AR2-MAG-QUAD-04:SI:.3f}</strong></td><td>DIP-01<br><strong>{AR2-MAG-DIP-01:SI:.3f}</strong></td><td>DIP-02<br><strong>{AR2-MAG-DIP-02:SI:.3f}</strong></td>
        <td>DIP-03<br><strong>{AR2-MAG-DIP-03:SI:.3f}</strong></td><td>VC-01<br><strong>{AR2-MAG-VCOR-01:SI:.3f}</strong></td>
        <td>VC-02<br><strong>{AR2-MAG-VCOR-02:SI:.3f}</strong></td><td>SEXT-01<br><strong>{AR2-MAG-SEXT-01:SI:.3f}</strong></td><td>SEXT-02<br><strong>{AR2-MAG-SEXT-02:SI:.3f}</strong></td></tr></table>'''),

    ('ST4', '''<table class="machine-status st4">
        <tr><th class="msTitle" colspan="5">Straight 4 Status</th><th class="msDateTime" colspan="5">{timestamp}</th></tr>
        <tr><td>Q-01<br><strong>{ST4-MAG-QUAD-01:SI:.3f}</strong></td><td>Q-02<br><strong>{ST4-MAG-QUAD-02:SI:.3f}</strong></td><td>Q-03<br><strong>{ST4-MAG-QUAD-03:SI:.3f}</strong></td>
        <td>Q-04<br><strong>{ST4-MAG-QUAD-04:SI:.3f}</strong></td><td>Q-05<br><strong>{ST4-MAG-QUAD-05:SI:.3f}</strong></td><td>DIP-01<br><strong>{ST4-MAG-DIP-01:SI:.3f}</strong></td>
        <td>DIP-02<br><strong>{ST4-MAG-DIP-02:SI:.3f}</strong></td><td>DIP-03<br><strong>{ST4-MAG-DIP-03:SI:.3f}</strong></td>
        <td>VHCOR-01<br><strong>{ST4-MAG-VCOR-01:SI:.3f}</strong> / <strong>{ST4-MAG-HCOR-01:SI:.3f}</strong></td>
        <td>VHCOR-02<br><strong>{ST4-MAG-VCOR-02:SI:.3f}</strong> / <strong>{ST4-MAG-HCOR-02:SI:.3f}</strong></td></tr></table>'''),

    ('RF', '''<table class="machine-status rf">
        <tr><th class="msTitle" colspan="3">RF Status</th><th class="msDateTime" colspan="3">{timestamp}</th></tr>
        <tr><td>&nbsp;</td><td>Buncher</td><td>BC1</td><td>BC2</td><td>LC1</td><td>LC2</td>
        <tr><td>Gradient Demand</td><td><strong>{BUN:LLRF:Aset:WR:.0f}</strong></td><td><strong>{INJ-RF-CAVGS-02:SS:.2f}</strong></td>
            <td><strong>{INJ-RF-CAVGS-03:SS:.2f}</strong></td><td><strong>{LIN1:LLRF:A2set:WR:.2f}</strong></td><td><strong>{LIN2:LLRF:A2set:WR:.2f}</strong></td></tr>
        <tr><td>Forward Power</td><td><strong>{ERLP-RFPSU:0636xd:.2f} kW</strong></td><td><strong>{ERLP-RFPSU:0388xd:.2f} kW</strong></td>
            <td><strong>{ERLP-RFPSU:0400xd:.2f} kW</strong></td><td><strong>{ERLP-RFPSU:0412xd:.2f} kW</strong></td><td><strong>{ERLP-RFPSU:0424xd:.2f} kW</strong></td></tr>
        <tr><td>Station Phase</td><td><strong>{BUN:LLRF:Phi:WR:.2f}</strong></td><td><strong>{INJ-RF-PHS-02:SS:.2f}</strong></td><td><strong>{INJ-RF-PLS-03:SS:.2f}</strong></td>
            <td><strong>{LIN1:LLRF:Phi:WR:.2f}</strong></td><td><strong>{LIN2:LLRF:Phi:WR:.2f}</strong></td></tr>
        <tr><td>Phase</td><td></td><td><strong>{INJ-RF-CAVPS-02:SS:+.2f}</strong></td><td><strong>{INJ-RF-CAVPS-03:SS:+.2f}</strong></td>
            <td></td><td></td></tr>
        <tr><td>Gradient (MV)</td><td></td><td><strong>{ERLP-RFPSU:0396CAG:.2f}</strong></td><td><strong>{ERLP-RFPSU:0408CAG:.2f}</strong></td>
            <td><strong>{ERLP-RFPSU:0420CAG:.2f}</strong></td><td><strong>{ERLP-RFPSU:0432CAG:.2f}</strong></td></tr></table>'''),

    ('RFSliders', '''<table class="machine-status rfsliders">
        <tr><th class="msTitle" colspan="3">RF Sliders</th><th class="msDateTime" colspan="3">{timestamp}</th></tr>
        <tr><td>&nbsp;</td><td>Buncher</td><td>BC1</td><td>BC2</td><td>LC1</td><td>LC2</td>
        <tr><td>Gradient</td><td><strong>{BUN:LLRF:Aset:WR:.0f}</strong></td><td><strong>{INJ-RF-CAVGS-02:SS:.2f}</strong></td><td><strong>{INJ-RF-CAVGS-03:SS:.2f}</strong></td>
            <td><strong>{LIN1:LLRF:A2set:WR:.2f}</strong></td><td><strong>{LIN2:LLRF:A2set:WR:.2f}</strong></td></tr>
        <tr><td>Open Loop Gradient</td><td><strong>{INJ-RF-CAVAS-01:SS:.2f}</strong></td><td><strong>{INJ-RF-CAVAS-02:SS:.2f}</strong></td><td><strong>{INJ-RF-CAVAS-03:SS:.2f}</strong></td>
            <td><strong>{LIN-RF-CAVAS-01:SS:.2f}</strong></td><td><strong>{LIN-RF-CAVAS-02:SS:.2f}</strong></td></tr>
        <tr><td>Phase</td><td><strong>{BUN:LLRF:Phi:WR:.2f}</strong></td><td><strong>{INJ-RF-CAVPS-02:SS:.2f}</strong></td><td><strong>{INJ-RF-CAVPS-03:SS:.2f}</strong></td>
            <td><strong>{LIN1:LLRF:Phi:WR:.2f}</strong></td><td><strong>{LIN2:LLRF:Phi:WR:.2f}</strong></td></tr>
        <tr><td>Open Loop Phase</td><td><strong>{INJ-RF-CAVSS-01:SS:.2f}</strong></td><td><strong>{INJ-RF-CAVSS-02:SS:.2f}</strong></td><td><strong>{INJ-RF-CAVSS-03:SS:.2f}</strong></td>
            <td><strong>{LIN-RF-CAVSS-01:SS:.2f}</strong></td><td><strong>{LIN-RF-CAVSS-02:SS:.2f}</strong></td></tr>
        <tr><td>Station Phase</td><td><strong>{INJ-RF-PHS-01:SS:.3f}</strong></td><td><strong>{INJ-RF-PHS-02:SS:.3f}</strong></td><td><strong>{INJ-RF-PHS-03:SS:.3f}</strong></td>
            <td><strong>{LIN-RF-PHS-01:SS:.3f}</strong></td><td><strong>{LIN-RF-PHS-02:SS:.3f}</strong></td></tr>
        <tr><td>Loop Phase</td><td><strong>{INJ-RF-PLS-01:SS:.3f}</strong></td><td><strong>{INJ-RF-PLS-02:SS:.3f}</strong></td><td><strong>{INJ-RF-PLS-03:SS:.3f}</strong></td>
            <td><strong>{LIN-RF-PLS-01:SS:.3f}</strong></td><td><strong>{LIN-RF-PLS-02:SS:.3f}</strong></td></tr>
        <tr><td>Tuner Position</td><td></td><td><strong>{LIN-RF-MOVS-03:SS:.2f}</strong></td><td><strong>{LIN-RF-MOVS-04:SS:.2f}</strong></td>
            <td><strong>{LIN-RF-MOVS-01:SS:.2f}</strong></td><td><strong>{LIN-RF-MOVS-02:SS:.2f}</strong></td></tr>
        <tr><td>Gradient (MV)</td><td></td><td><strong>{ERLP-RFPSU:0396CAG:.2f}</strong></td><td><strong>{ERLP-RFPSU:0408CAG:.2f}</strong></td>
            <td><strong>{ERLP-RFPSU:0420CAG:.2f}</strong></td><td><strong>{ERLP-RFPSU:0432CAG:.2f}</strong></td></tr></table>'''),

    ('FEL', '''<table class="machine-status fel">
        <tr><th class="msTitle" colspan="4">FEL Status</th><th class="msDateTime" colspan="3">{timestamp}</th></tr>
        <tr><td>Gap<br><strong>{FEL-WIG-TRANS-01:MSABS:.3f}mm</strong></td><td>Wavelength<br><strong>{FEL-DIAG-SPEC-01:L0:.2f}&mu;m</strong></td><td>Bandwidth<br><strong>{FEL-DIAG-SPEC-01:W:.2f}&mu;m</strong></td>
        <td>Intensity<br><strong>{FEL-DIAG-SPEC-01:INT:.0f}</strong></td><td>Power<br><strong>X mW</strong></td><td colspan=2>Stability<br><strong>Y%</strong> rms, <strong>Z%</strong> p2p</td></tr>
        <tr><td>LA<br><strong>{INJ-LSR-ATT-01:S2TI:.2f}</strong></td><td colspan=2>FEL temperatures [&deg;C]<br>
        <strong>{ALICE-FEL-CAV-01:RT:.2f} {ALICE-FEL-CAV-02:RT:.2f} {ALICE-FEL-CAV-03:RT:.2f} {ALICE-FEL-CAV-04:RT:.2f}</strong></td>
        <td>MO PID setpoint<br><strong>{INJ-MO-LSR-EPID-01.VAL:.1f}</strong></td>
        <td>AR1-DIP-03<br><strong>{AR1-MAG-DIP-03:SI:.3f}A</strong></td><td>ST2-DIP-04<br><strong>{ST2-MAG-DIP-04:SI:.3f}A</strong></td>
        <td>Cavity mirror pos<br><strong>{FEL-DWN-TRANS-01:RCAL:.1f}&mu;m</strong></tr></table>''')])

    # Define HTML headers and footers
    # Note the {} here - this will be replaced by the machine region
    # We also add a menu of all the regions, hence the final <p>
    header = '''<!DOCTYPE html><html><head>
                    <title>{}ALICE Machine Status Server</title>
                    <link rel="stylesheet" href="https://elog.astec.ac.uk/alice/alicelog/default.css">
                    </head><body>
                    <h1>ALICE Machine Status Server</h1>
                    <p>Click on each machine area to see a list of current parameters.</p>
                    <p>'''
    footer = '''<p><a href=/restartServer>Restart server</a> - started on {}</p>
                <p><i>Machine Status Server v3.0 - Ben Shepherd, April 2015</i></p>
                </body></html>'''.format(datetime.now().strftime('%d/%m/%y %H:%M:%S'))

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
                if not pv.connected:
                    pvVal = float('nan')
                else:
                    pvVal = pv.get()
                # handle special cases
                # report a nicely formatted value for the train length
                # in micro- or nanoseconds
                if param == 'INJ-LSR-DLY-01`BCAL':
                    if pvVal < 1:
                        pvVal = '{:.0f} ns'.format(pvVal * 1000)
                    elif pvVal >= 1:
                        pvVal = '{:.0f} &mu;s'.format(pvVal)
                    else:
                        pvVal = 'N/A'

                # status of burst generator
                elif param == 'INJ-LSR-POC-01`RRUN':
                    if pvVal == -1:
                        pvVal = 'On'
                    elif pvVal == 0:
                        pvVal = 'Off'
                    else:
                        pvVal = 'N/A'

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
                              "area": "{}",
                              "params": '{}'}})'''.format(path, output.replace('\n', ''))

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
                      "folder": "{}",
                      "files": [  '''.format(folder.replace('\\', '/'))
            for file in files:
                if file[-4:].lower() == '.png':
                    output += '\t\t"{}", \n'.format(file)
            output = output[0:-3] + ']})'

        elif path == 'restartServer':
            # restart the server
            # serve a redirect page first
            contentType = "text/html"
            output = '''<html><head><meta http-equiv="refresh" content="3;url=/">
                        <title>Restarting - Machine Status Server</title></head>
                        <body><h1>ALICE Machine Status Server</h1>
                        <p>Restarting - please wait a few seconds or <a href=/>click here</a>.</p>
                        <p><img src="http://rubbercat.net/misc/tears/alice.gif"></p></body></html>'''
            self.server.running = False

#        elif path == 'favicon.ico':
#            # Serve a favicon (this doesn't work)
#            contentType = "image/ico"
#            output = open('Alice_Logo.ico', 'rb').read()

        else:
            # Default response
            contentType = "text/html"
            output = (self.header.format('') +
                      '<p>Invalid URL: /{}</p>'.format(path) + self.footer)

        self.send_response(200)
        self.send_header("Content-type", contentType)
        self.end_headers()
        self.wfile.write(output.encode('utf-8'))

try:

#    menu_options = (('Say Hello', None, hello),
#                    ('Switch Icon', None, switch_icon),
#                    ('A sub-menu', next(icons), (('Say Hello to Simon', next(icons), simon),
#                                                  ('Switch Icon', next(icons), switch_icon),
#                                                 ))
#                   )
#    def bye(sysTrayIcon): print('Exiting Machine Status Server.')
#
#    SysTrayIcon('Alice_Logo.ico', 'Machine Status Server', (), on_quit=bye, default_menu_index=1)
    port = 27643
    server = StoppableServer(('', port), MyHandler)
    certfile = r'C:\SSL\erlpcon2_dl_ac_uk_concat.crt'
    keyfile = r'C:\SSL\erlpcon2.private.key'
    server.socket = ssl.wrap_socket(server.socket, keyfile=keyfile, certfile=certfile, server_side=True)
    print('Started https server on port', port)
    print('Try https://localhost:{}/'.format(port))
    server.serve_forever() #until /restartServer requested
    sleep(2)

    # Restart the script
    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]

#    os.chdir(_startup_cwd)
    os.execv(sys.executable, args)

except KeyboardInterrupt:
    print('^C received, shutting down server')
    server.socket.close()

