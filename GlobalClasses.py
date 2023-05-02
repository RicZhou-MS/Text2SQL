'''
GlobalContext class is used to store global variables

Created by Ric Zhou on 2023-04-29
'''
import os
from dotenv import load_dotenv


class GlobalContext:
    DB_SERVER = ""
    DB_NAME = ""
    DB_USER = ""
    DB_USER_PASS = ""
    OPENAI_API_KEY = ""
    OPENAI_BASE = ""
    System_Prompt = """You are smart AI can do text to SQL, following is the Azure SQL database data model with table definitions, you will provide SQL statement that can answer user question based on the data model, you will think step by step throughout and return SQL statement directly without any additional explanation.

<Table definition> 
{tableDefinition}
"""

    FewShot_Prompt = ""
    few_shot_user_msg1 = '''"AWC Logo Cap"这个产品销售最好的三个城市是哪些？'''
    few_shot_ai_msg1 = """SELECT TOP 3 A.City, sum(SOD.LineTotal) AS TotalSales  
FROM [SalesLT].[SalesOrderDetail] SOD  
JOIN [SalesLT].[Product] P ON SOD.ProductID = P.ProductID  
JOIN [SalesLT].[SalesOrderHeader] SOH ON SOD.SalesOrderID = SOH.SalesOrderID  
JOIN [SalesLT].[Address] A ON SOH.ShipToAddressID = A.AddressID  
WHERE P.Name = 'AWC Logo Cap'  
GROUP BY A.City  
ORDER BY TotalSales DESC;  
"""
    few_shot_user_msg2 = ""
    few_shot_ai_msg2 = ""

    def __init__(self):
        load_dotenv()
        # get environment variables set by .env file
        GlobalContext.DB_SERVER = os.getenv("DB_SERVER")
        GlobalContext.DB_NAME = os.getenv("DB_NAME")
        GlobalContext.DB_USER = os.getenv("DB_USER")
        GlobalContext.DB_USER_PASS = os.getenv("DB_USER_PASS")
        GlobalContext.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        GlobalContext.OPENAI_BASE = os.getenv("OPENAI_BASE")
