#!/usr/bin/env python

import sys
import json
import base64

records = []
for line in sys.stdin:
    records.append({'value': base64.b64encode(line)})

print(json.dumps({'records': records}))
