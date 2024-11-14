#!/bin/bash

# Proveri da li je unet argument
if [ -z "$1" ]; then
  echo "Koriscenje: $0 NOVI_NAZIV"
  exit 1
fi

# Novi naziv koji će zameniti 'nemanja'
NOVI_NAZIV=$1

# Prolazak kroz sve fajlove rekurzivno u trenutnom direktorijumu, relativno
find "$(pwd)" -type f | while IFS= read -r file; do
  # Postavljanje odgovarajuće kodne stranice
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS varijanta, koristi LC_CTYPE i zahteva .bak ekstenziju
    LC_CTYPE=C sed -i .bak "s/nemanja/$NOVI_NAZIV/g" "$file" && rm "${file}.bak"
  else
    # Linux varijanta, koristi LC_ALL bez dodatne ekstenzije
    LC_ALL=C sed -i "s/nemanja/$NOVI_NAZIV/g" "$file"
  fi
done
