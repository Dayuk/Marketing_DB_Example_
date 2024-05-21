# sheets_connector.py
import gspread
from settings import MAX_ROWS, MAX_COLS

class GoogleSheetConnector:
    def __init__(self, credentials, spreadsheet_name):
        self.credentials = credentials
        self.spreadsheet_name = spreadsheet_name
        self.max_rows = MAX_ROWS
        self.max_cols = MAX_COLS
        self.headers = ["id", "name", "text", "link", "datetime"]

    def insert_data(self, data, table_name):
        gc = gspread.authorize(self.credentials)  # credentials 객체를 사용하여 인증
        spreadsheet = gc.open(self.spreadsheet_name)
        sheet_name = table_name
        try:
            self.sheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            # sheet가 존재하지 않을때 sheet 생성
            self.sheet = spreadsheet.add_worksheet(title=sheet_name, rows=self.max_rows, cols=self.max_cols)
            self.sheet.insert_row(self.headers, index=1)

            # 1행 고정
            self.sheet.freeze(rows=1)

        #데이터 입력
        self.sheet.append_row(data)
    