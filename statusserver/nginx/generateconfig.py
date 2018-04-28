import os
import re
import random
import string

log = []


def defaultConfig():
    log.append('location / { \n\t include uwsgi_params; \n\t uwsgi_pass   unix://code/switchmate.sock; \n\t }\t\n')

def relayConfig():
    for param in os.environ.keys():
        if param.startswith("RELAY"):
            macaddress = param.split('_')[1]
            if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macaddress.lower()):
                log.append('location = /device/{0} {{\n\t if ($request_method = PUT) {{\n\t proxy_pass http://{1};\n\t}}\n\t uwsgi_pass   unix://code/switchmate.sock; \n}} \n'.format(macaddress.upper(), os.environ[param]))

def updateconfig(filepath, replacements):

    with open(filepath) as infile, open(filepath, 'w') as outfile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            outfile.write(line)

defaultConfig()
relayConfig()
config = ''.join(log)
#updateconfig('/etc/nginx/conf.d/default.conf', {'$REPLACE':config})
