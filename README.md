# aps-inventory-tools
Inventory scripts

## Run
Create a input DokuWiki table to read in:

```shell
touch server_inven.txt
```

Grab inventory from SISTA wiki from the title header to the </sortable> tag and paste into 'server_inven.txt' and run converter.

```shell
python inventory.py
```

This will create a csv output file inventory.csv