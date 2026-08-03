"""Deze modules verzorg de database services voor de foto modules."""

import sqlite3
import logging
from contextlib import contextmanager

# eigen uncties
from progs.context.context import Context

logger = logging.getLogger(__name__)


@contextmanager
def db_sessie(pad):
    db = sqlite3.connect(pad)
    db.execute("PRAGMA journal_mode=WAL;")
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db.close()


def get_db(ctx):
    if ctx.db is None:
        ctx.db = sqlite3.connect(ctx.db.pad)
        ctx.db.row_factory = sqlite3.Row
    return ctx.db


def open(cntxt: Context, sql_stmt):
    """Voer CREATE TABLE uit."""
    with db_sessie(cntxt.db.pad) as db:
        db.execute(sql_stmt)
        logger.info("Tabel aangemaakt of bestaat al.")


def haalop_rijen(cntxt, sql_stmt):
    """Voer SELECT uit en retourneer alle rijen."""
    try:
        with db_sessie(cntxt.db.pad) as db:
            cursor = db.cursor()
            cursor.execute(sql_stmt)
            return cursor.fetchall()
    except Exception:
        return []


def haalop_rij(cntxt: Context, sql_stmt):
    """Voer SELECT uit en retourneer één rij."""
    try:
        with db_sessie(cntxt.db.pad) as db:
            cursor = db.cursor()
            cursor.execute(sql_stmt)
            return cursor.fetchone()
    except Exception:
        return []


def voegtoe_rij(cntxt: Context, sql_stmt, rij):
    """Voer INSERT uit voor één rij."""
    with db_sessie(cntxt.db.pad) as db:
        db.execute(sql_stmt, rij)


def voegtoe_rijen(cntxt: Context, sql_stmt, rijen):
    """Voer bulk INSERT uit."""
    with db_sessie(cntxt.db.pad) as db:
        cursor = db.cursor()
        cursor.executemany(sql_stmt, rijen)
        logger.info(f"{len(rijen)} rijen toegevoegd.")
