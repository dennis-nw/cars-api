#!/usr/bin/env bash
touch ./data/test.db
sqlite3 ./data/test.db < ./data/cars.sql
pytest tests/
rm ./data/test.db
