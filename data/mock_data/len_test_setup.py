# **********************************************************************************************************************
# Bloomberg Data Licence Cost Review
# **********************************************************************************************************************
# IMPORTS
import os
import numpy as np
import pandas as pd

# logging
from traceback import print_exc
from colorama import Fore
import timeit
from typing import List, Optional, Dict, Any, Union

# database connections
from db_connections.DB_CONN import DATABASE_CONNECTOR

# ORM
from models.process.invoices.invoices_dl import BBG_Invoice_DL
from models.process.invoices.invoices_refresh import BBG_Invoice_Refresh
from models.process.invoices.invoices_bval import BBG_Invoice_BVAL


# ----------------------------------------------------------------------------------------------------------------------
# import invoice packages for all accounts
# ----------------------------------------------------------------------------------------------------------------------
l_id_account_number = [30395902, 30412720, 30314240]
l_invoice_dt = ["202209"]

db = DATABASE_CONNECTOR(connection_list=["PG_GAM"])

for id_account_number in l_id_account_number:
    for invoice_dt in l_invoice_dt:
        s_time = timeit.default_timer()
        BBG_Invoice_DL.control_read_source_file(
            id_account_number=id_account_number,
            invoice_dt=invoice_dt,
            search_file_name="DL_Report",
            db=db,
        )

        BBG_Invoice_Refresh.control_read_source_file(
            id_account_number=id_account_number,
            invoice_dt=invoice_dt,
            search_file_name="DL_Surcharge",
            db=db,
        )

        BBG_Invoice_BVAL.control_read_source_file(
            id_account_number=id_account_number,
            invoice_dt=invoice_dt,
            search_file_name="BVAL_Report",
            db=db,
        )

        elapsed = timeit.default_timer() - s_time
        print(
            Fore.LIGHTGREEN_EX,
            f"Invoice package imported for account/ reporting month: {id_account_number}/{invoice_dt}",
            Fore.RESET,
        )
