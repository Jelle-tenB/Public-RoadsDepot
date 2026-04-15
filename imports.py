from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional
from sqlcipher3 import connect, DatabaseError # It says these modules don't exist, but they do.

DB_PATH = r"RoadsDepot2026.db"
LOGDB_PATH = rf"RoadsDepotLog{datetime.now().strftime('%Y')}.db"

MOBIELS_DICT = {"string": ["merk:", "model:", "opslag:"],
                "int": ["totaal:"],
                "bool": [],
                "kwaliteit": True,
                "displayport": False}
DESKTOPS_DICT = {"string": ["merk:", "model:", "ram:", "CPU:", "opslag:", "locatie:"],
                 "int": ["totaal:"],
                 "bool": ["dvd"],
                 "kwaliteit": True,
                 "displayport": False}
LAPTOPS_DICT = {"string": ["merk:", "model:", "ram:", "CPU:", "opslag:", "locatie:"],
                "int": ["totaal:"],
                "bool": ["dvd"],
                "kwaliteit": True,
                "displayport": False}
VOEDINGEN_DICT = {"string": ["merk:", "soort:"],
                  "int": ["totaal:", "wattage:"],
                  "bool": ["nieuw"],
                  "kwaliteit": False,
                  "displayport": False}
TOETSENBORDEN_DICT = {"string": ["merk:", "model:"],
                      "int": ["totaal:"],
                      "bool": ["nieuw", "draadloos"],
                      "kwaliteit": False,
                      "displayport": False}
MUIZEN_DICT = {"string": ["merk:", "model:"],
               "int": ["totaal:"],
               "bool": ["nieuw", "draadloos"],
               "kwaliteit": False,
               "displayport": False}
KABELS_DICT = {"string": ["model:", "lengte:"],
               "int": ["totaal:"],
               "bool": [],
               "kwaliteit": False,
               "displayport": False}
BEELDSCHERMEN_DICT = {"string": ["merk:", "model:", "locatie:"],
                      "int": ["totaal:", "inch:", "VGA:", "DVI:", "HDMI:", "USB_A:", "USB_B:", "USB_C:", "ethernet:"],
                      "bool": ["docking", "webcam", "speaker"],
                      "kwaliteit": False,
                      "displayport": True}

CATEGORIE_DICT = {"mobiels": MOBIELS_DICT,
                  "desktops": DESKTOPS_DICT,
                  "laptops": LAPTOPS_DICT,
                  "voedingen": VOEDINGEN_DICT,
                  "toetsenborden": TOETSENBORDEN_DICT,
                  "muizen": MUIZEN_DICT,
                  "kabels": KABELS_DICT,
                  "beeldschermen": BEELDSCHERMEN_DICT}

CATEGORIE_COLUMNS = {"mobiels": ["merk", "model", "totaal", "A_kwaliteit", "B_kwaliteit", "C_kwaliteit", "opslag", "opmerking"],
                   "desktops": ["merk", "model", "totaal", "A_kwaliteit", "B_kwaliteit", "C_kwaliteit", "CPU", "ram", "opslag", "dvd", "locatie", "opmerking"],
                   "laptops": ["merk", "model", "totaal", "A_kwaliteit", "B_kwaliteit", "C_kwaliteit", "CPU", "ram", "opslag", "dvd", "locatie", "opmerking"],
                   "voedingen": ["merk", "totaal", "wattage", "soort", "nieuw", "opmerking"],
                   "toetsenborden": ["merk", "model", "totaal", "nieuw", "draadloos", "opmerking"],
                   "muizen": ["merk", "model", "totaal", "nieuw", "draadloos", "opmerking"],
                   "kabels": ["model", "totaal", "lengte", "opmerking"],
                   "beeldschermen": ["merk", "model", "totaal", "inch", "VGA", "DVI", "displayport_in", "displayport_out", "HDMI", "USB_A", "USB_B", "USB_C", "ethernet", "docking", "webcam", "speaker", "locatie", "opmerking"]}

class Shared:
    """This class is used to share data between different modules."""
    def __init__(self) -> None:
        self.categorie: Optional[str] = None
        self.key: Optional[str] = None
        self.gebruiker: Optional[str] = None
        self.path: Optional[str] = None
        self.is_log_active: Optional[bool] = False
        self.sorted: Optional[bool] = False
        self.sort_column: Optional[str] = None
        self.bool_list = []
        self.kwaliteit_list = []
        self.kwaliteit_label_list = []
        self.int_list = []
        self.string_list = []
        self.bool_placement = []
        self.kwaliteit_placement = []
        self.kwaliteit_label_placement = []
        self.int_placement = []
        self.string_placement = []
        self.int_label_list = []
        self.string_label_list = []
        self.int_label_placement = []
        self.string_label_placement = []
        self.displayport_placement = []
        self.displayport_label_placement = []
        self.opmerking: Optional[str] = None
        self.db_id: Optional[int] = None

shared = Shared()

@contextmanager
def open_db_readonly(key: str, timeout: int = 30):
    """
    Open a read-only SQLite connection.
    Connection is closed automatically after use.
    """

    db = connect(
        f"file:{DB_PATH}?mode=ro",
        uri=True,
        timeout=timeout,
    )

    try:
        db.execute(f"PRAGMA key = '{key}';")
        # Safety: enforce read-only at SQLite level
        db.execute("PRAGMA query_only = ON;")
        yield db
    finally:
        db.close()


@contextmanager
def open_db_write(key: str, timeout: int = 30):
    """
    Open a write SQLite connection.
    Connection is closed automatically after use.
    """
    db = connect(
        DB_PATH,
        timeout=timeout,
        isolation_level="IMMEDIATE"
    )

    try:
        db.execute(f"PRAGMA key = '{key}';")
        db.execute("PRAGMA query_only = OFF;")
        yield db
    finally:
        pass

def test_connection(key: str):
    """Checks if the database can be opened with the given key."""
    try:
        conn = connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(f"PRAGMA key = '{key}';")
        cur.execute("SELECT * FROM desktops LIMIT 1;")
        cur.fetchone()
        conn.close()
        return True
    except DatabaseError:
        return False

@contextmanager
def open_logdb(logkey, timeout: int = 30):
    # Currently unused!
    """
    Open a write SQLite connection to the log database.
    Connection is closed automatically after use.
    """
    db = connect(
        LOGDB_PATH,
        timeout=timeout,
        isolation_level="IMMEDIATE"
    )

    try:
        db.execute(f"PRAGMA key = '{logkey}';")
        db.execute("PRAGMA query_only = OFF;")
        yield db
    finally:
        pass

@contextmanager
def open_old_logdb(logkey, path, timeout: int = 30):
    # Currently unused!
    """
    Open a write SQLite connection to the log database.
    Connection is closed automatically after use.
    """
    db = connect(
        path,
        timeout=timeout,
        isolation_level="IMMEDIATE"
    )

    try:
        db.execute(f"PRAGMA key = '{logkey}';")
        db.execute("PRAGMA query_only = OFF;")
        yield db
    finally:
        db.close()

def check_log_exists():
    # Currently unused!
    """Check if the log database exists."""
    if Path(LOGDB_PATH).is_file():
        return True
    else:
        # Make new Log
        # Because of unuse this will always return True
        return True

def create_new_log(ww):
    # Currently unused!
    """Makes a new log database"""
    try:
        db = connect(LOGDB_PATH)
        db.execute("PRAGMA foreign_keys = ON;")
        db.execute(f"PRAGMA key = '{ww}';")
        db.execute(MAKE_NEW_LOG)
        db.commit()
        return True
    except Exception as e:
        return e

def make_backup(key: str):
    """
    Makes a backup of the current database and log database.
    With a maximum of 7 backups.
    """

    today = datetime.now().strftime("%Y-%m-%d")
    backup_folder = Path(r".\dbBackups")
    backup_path = Path(backup_folder)/f"backup{today}.db"

    # No log backup for now, as the log database is currently unused and would just take up space.
    # logbackup_folder = Path(r"I:\RoadsDepotDB\logBackups")
    # logbackup_path = Path(logbackup_folder)/f"logbackup{today}.db"

    if backup_path.exists(): # and logbackup_path.exists():
        return

    backup_list = sorted(
        backup_folder.glob("backup*.db"),
        key=lambda p: datetime.strptime(
            p.stem.replace("backup", ""),
            "%Y-%m-%d"
        ),
        reverse=True)

    # logbackup_list = sorted(
    #     logbackup_folder.glob("logbackup*.db"),
    #     key=lambda p: datetime.strptime(
    #         p.stem.replace("logbackup", ""),
    #         "%Y-%m-%d"
    #     ),
    #     reverse=True)

    if len(backup_list) >= 7:
        Path(backup_list[-1]).unlink()

    # if len(logbackup_list) >= 7:
    #     Path(logbackup_list[-1]).unlink()

    with open_db_readonly(key) as old_db:
        old_db.execute("PRAGMA wal_checkpoint(PASSIVE);")
        with connect(backup_path) as new_db:
            new_db.execute(f"PRAGMA key = '{key}';")
            old_db.backup(new_db)

    # with open_logdb(key) as old_log_db:
    #     old_log_db.execute("PRAGMA wal_checkpoint(PASSIVE);")
    #     with connect(logbackup_path) as new_log_db:
    #         new_log_db.execute(f"PRAGMA key = '{key}';")
    #         old_log_db.backup(new_log_db)
