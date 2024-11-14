#!/bin/bash

# Proveri da li je unet argument
if [ -z "$1" ]; then
  echo "Koriscenje: $0 NOVI_NAZIV"
  exit 1
fi

# Novi naziv koji će zameniti '__SERVICE_NAME__'
NOVI_NAZIV=$1

# Prolazak kroz sve fajlove rekurzivno u trenutnom direktorijumu, isključujući .sh fajlove
find "$(pwd)" -type f ! -name "*.sh" | while IFS= read -r file; do
  # Postavljanje odgovarajuće kodne stranice
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS varijanta, koristi LC_CTYPE i zahteva .bak ekstenziju
    LC_CTYPE=C sed -i .bak "s/__SERVICE_NAME__/$NOVI_NAZIV/g" "$file" && rm "${file}.bak"
  else
    # Linux varijanta, koristi LC_ALL bez dodatne ekstenzije
    LC_ALL=C sed -i "s/__SERVICE_NAME__/$NOVI_NAZIV/g" "$file"
  fi
done

echo "Zamenjen __SERVICE_NAME__ sa $NOVI_NAZIV u svim fajlovima, osim u .sh fajlovima."
