import os
import re
import random
import string

log = []


def relayConfig():
    for param in os.environ.keys():
        if param.startswith("RELAY"):
            macaddress = param.split('_')[1]
            if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macaddress.lower()):
                log.append('location = /device/{0} {{\n\t if ($request_method = PUT) {{\n\t proxy_pass http://{1};\n\t}}\n\t uwsgi_pass   unix://code/switchmate.sock; \n}} \n'.format(macaddress.upper(), os.environ[param]))

def updateconfig(filepath, config):

    with open(filepath, "a") as f:
         f.write(config)
         f.close

relayConfig()
config = ''.join(log)

if not log:
   updateconfig('/etc/nginx/conf.d/default.conf', '}')
else:
   updateconfig('/etc/nginx/conf.d/default.conf', config + '\n }')

