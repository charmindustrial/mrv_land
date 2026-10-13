#!/bin/bash
# prints the dialog title, value, each input row (name, value, ±), and the Close button ref
python3 read_modal.py "$1" /dev/null | grep -E 'dialog "|tCO₂e$|^- button ".* [0-9].* source|±|Close|^- row "' | sed 's/\[cursor=pointer\]//'
