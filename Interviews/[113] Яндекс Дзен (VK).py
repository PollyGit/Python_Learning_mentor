# Задача 1 (Pandas):
# Есть файл со строчками вида url \t title
# Напишите функцию, которая берет имя файла и на выходе возвращает json
# Пример файла: example.tsv
# Пример того, что должно быть на выходе




# ----------------
# из чат гпт

import pandas as pd

def tsv_urls_to_json(path: str, has_header: bool = False) -> str:
    """
    path — путь к файлу .tsv
    has_header — True, если в файле есть заголовки столбцов; иначе ожидаем 2 колонки: url, title
    Возвращает JSON-строку вида:
    [{"url": "...", "title": "..."}, ...]
    """
    df = pd.read_csv(
        path,
        sep="\t",
        header=0 if has_header else None,
        names=None if has_header else ["url", "title"],
        dtype={"url": "string", "title": "string"},
        encoding="utf-8"
    )

    # лёгкая очистка
    df["url"] = df["url"].str.strip()
    df["title"] = df["title"].str.strip()

    # в JSON (читаемо и с кириллицей)
    return df.to_json(orient="records", force_ascii=False, indent=2)



#
# Пример использования

# ВАЖНО: в Windows-пути используйте raw-строку или двойные слэши
json_str = tsv_urls_to_json(r"D:\Desktop\datasets\example.tsv", has_header=False)
print(json_str)


#