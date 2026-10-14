

#!/bin/bash
set -e

cd /var/www/hospital_api

source venv/bin/activate

git pull origin main

pip install -r requirements.txt

alembic upgrade head

sudo systemctl restart hospital_api

sudo systemctl status hospital_api --no-pager
