import sqlcipher3
from imports_unsecure import DB_PATH

password = "Technology"

# Open encrypted database
enc = sqlcipher3.connect(r"I:\RoadsDepotDB\RoadsDepot2026_enc.db")
enc.execute(f"PRAGMA key = '{password}';")

# Attach plaintext database
enc.execute(r"ATTACH DATABASE 'testdb.db' AS plaintext KEY '';")

# Export
enc.execute("SELECT sqlcipher_export('main', 'plaintext');")
enc.execute("DETACH DATABASE plaintext;")

enc.commit()
enc.close()
