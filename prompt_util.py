from langchain.prompts import PromptTemplate



def get_prompt(example: str | None):
    """
    自訂產生 SQL 的 Prompt
    """

    prompt_template = f"""
        你是一個 SQL 生成器，請基於以下資訊生成一個 SQL 查詢：
        
        - 資料表格式: {{table_info}}
        - 使用者的問題: {{input}}
        - 每次獲取資料數量: {{top_k}}

        請輸出完整的 SQL 查詢，不要包含任何解釋文字，並符合下面規則。

        ### 1. SQL 語法規則  

        - **表格名稱必須加上雙引號**  
        - ✅ 正確：`SELECT 名稱 FROM "table_name"`  
        - ❌ 錯誤：`SELECT 名稱 FROM table_name`（**表格名稱沒有雙引號，錯誤！**）  
        - ❌ 錯誤：`SELECT 名稱 FROM 'table_name'`（**單引號錯誤！**）  

        - **欄位名稱不可使用雙引號**  
        - ✅ 正確：`SELECT 名稱 FROM "table_name"`  
        - ❌ 錯誤：`SELECT "名稱" FROM "table_name"`（**欄位名稱不應加雙引號！**）  

        - **聚合函數必須加括號**  
        - ✅ 正確：`SELECT MIN(日期) FROM "table_name"`  
        - ❌ 錯誤：`SELECT MIN 日期 FROM "table_name"`  

        ### 2. `GROUP BY` 使用規則  

        - **當問題涉及「最高」「最低」「平均」「總和」時，一定要 `GROUP BY`**  
        - **當問題要求「每個對象」、「每個類別」、「每個項目」時，一定要 `GROUP BY`**  
        - ❌ 錯誤：`SELECT AVG(數值) FROM "table_name"`  
        - ✅ 正確：`SELECT 類別, AVG(數值) FROM "table_name" GROUP BY 類別`  
        - **選擇正確的 `GROUP BY` 屬性**  
        - 若問題涉及某項目（如：「哪個項目的值最高？」）➡ `GROUP BY 項目名稱`  
        - 若問題涉及某類別（如：「哪個類別的平均值最高？」）➡ `GROUP BY 類別名稱`  
        - 若問題未明確說明，預設使用 `GROUP BY 項目名稱`  
        - **`SELECT` 中必須包含 `GROUP BY` 的欄位**  
        - ❌ 錯誤：`SELECT MAX(數值) FROM "table_name" GROUP BY 類別`  
        - ✅ 正確：`SELECT 類別, MAX(數值) FROM "table_name" GROUP BY 類別`  

        """

    if example is not None and example != "":
        prompt_template += f"""

        以下是檢索出最相關的範例問答：
            {example}
        """

    return PromptTemplate.from_template(prompt_template)