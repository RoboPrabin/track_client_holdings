import pandas as pd
from sqlalchemy import create_engine
from utils import helper
from config import config

class BroExtractor:

    def extract_bro(self):
        # Step 1: Read Excel
        # excel_path = r"D:\Trishakti\Projects\RPA\track_stock_price\data\output\holdings_FINAL.xlsx"
        excel_path = config.OUTPUT_CLIENT_DATA_FILEPATH_FINAL
        df_excel = pd.read_excel(excel_path)

        # Step 2: Connect to PostgreSQL
        engine = create_engine(helper.get_intranet_engine())
        df_client_rm = pd.read_sql("SELECT client_code, rm_id FROM client_rm", engine)
        df_rm = pd.read_sql("SELECT u_id, rm_name, rm_fname FROM rm_tbl", engine)

        # Step 3: Merge RM info into client_rm
        df_merged = df_client_rm.merge(df_rm, left_on='rm_id', right_on='u_id', how='left')

        # Step 4: Create 'Bro' column using RM name
        df_merged['bro'] = df_merged['rm_name'] + ' ' + df_merged['rm_fname']

        # Step 5: Ensure matching data types for merge
        df_excel['username'] = df_excel['username'].astype(str)
        df_merged['client_code'] = df_merged['client_code'].astype(str)

        # Step 6: Merge RM info into Excel data
        df_final = df_excel.merge(df_merged[['client_code', 'bro']], left_on='username', right_on='client_code', how='left')

        df_final.drop(columns=['client_code'], inplace=True)
        # Step 7: Fill missing Bro values with "N/A"
        df_final['bro'] = df_final['bro'].fillna("N/A")
        df_final['clientCode'] = df_final['clientCode'].fillna("N/A")
        helper.convert_columns_to_str(df=df_final)
        # Step 8: Save enriched Excel file
        # output_path = r"D:\Trishakti\Projects\RPA\track_stock_price\data\output\holdings_with_bro.xlsx"
        df_final.to_excel(excel_path, index=False)

        print("✅ Excel file enriched with Bro column and saved successfully!")
