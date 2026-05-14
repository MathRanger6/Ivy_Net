#!/bin/bash

# Target the MAU executable
MSUPDATE_PATH="/Library/Application Support/Microsoft/MAU2.0/Microsoft AutoUpdate.app/Contents/MacOS/msupdate"

echo "========================================="
echo " Checking for available Microsoft Updates"
echo "========================================="
echo ""

# Run the list command
"$MSUPDATE_PATH" --list

echo ""
echo "========================================="
echo "Enter the App Codes you want to update (separated by spaces)."
read -p "Or press [ENTER] to update all available apps: " user_input
echo "========================================="
echo ""

# Check if the user just pressed Enter
if [ -z "$user_input" ]; then
    echo "No apps specified. Updating all available applications..."
    "$MSUPDATE_PATH" --install
else
    echo "Updating specified apps: $user_input"
    # Loop through each space-separated app code provided
    for app in $user_input; do
        echo ""
        echo "Processing $app..."
        "$MSUPDATE_PATH" --install --apps "$app"
    done
fi

echo ""
echo "Update process complete."
