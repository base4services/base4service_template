#!/bin/bash

# Proveri da li su zadati argumenti
if [ -z "$1" ]; then
  echo "Usage: $0 NEW_NAME [DIRECTORY]"
  exit 1
fi

# Nova vrednost za zamenu '__SERVICE_NAME__'
NEW_NAME=$1

# Direktorijum za pretragu; podrazumevani je trenutni direktorijum
TARGET_DIR=${2:-$(pwd)}

# Proveri da li direktorijum postoji
if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: Directory $TARGET_DIR does not exist."
  exit 1
fi

# Iteriraj kroz sve fajlove rekurzivno u zadatom direktorijumu, izuzimajući .sh fajlove
find "$TARGET_DIR" -type f ! -name "*.sh" | while IFS= read -r file; do
  # Postavi odgovarajući lokal za rukovanje kodiranjem
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS varijanta: koristi LC_CTYPE i zahteva .bak ekstenziju za zamenu u mestu
    LC_CTYPE=C sed -i .bak "s/__SERVICE_NAME__/$NEW_NAME/g" "$file" && rm "${file}.bak"
  else
    # Linux varijanta: koristi LC_ALL bez potrebe za rezervnim ekstenzijama
    LC_ALL=C sed -i "s/__SERVICE_NAME__/$NEW_NAME/g" "$file"
  fi
done
