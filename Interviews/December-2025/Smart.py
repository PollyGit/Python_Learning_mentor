# 2

import pandas as pd
import numpy as np

# df1 = clients: phone, templateNum, email, fio, closed
# df2 = parsed_emails: phone, email, parsedDt

clients = df1.copy()
parsed = df2.copy()

clients["closed"] = pd.to_datetime(clients["closed"], errors="coerce")
parsed["parsedDt"] = pd.to_datetime(parsed["parsedDt"], errors="coerce")

# если email в clients может быть пустой строкой
clients["email"] = clients["email"].replace("", pd.NA)

# 1) Соединяем, чтобы у каждой parsed-записи была дата closed клиента (по phone)
# Важно: если в clients phone уникален — отлично. Если нет, уточняй ключ.
m = clients[["phone", "closed"]].merge(parsed, on="phone", how="left")

# 2) Разделяем на "после закрытия" и "до закрытия"
after = m.query("parsedDt.notna() and parsedDt > closed").copy()
before = m.query("parsedDt.notna() and parsedDt <= closed").copy()


# 3) Для каждого phone выбираем:
#    - after: минимальный parsedDt (первый после)
#    - before: максимальный parsedDt (последний до)
idx_after = after.groupby("phone")["parsedDt"].idxmin()
best_after = after.loc[idx_after, ["phone", "email", "parsedDt"]].rename(
    columns={"email": "email_after", "parsedDt": "parsed_after"}
)

idx_before = before.groupby("phone")["parsedDt"].idxmax()
best_before = before.loc[idx_before, ["phone", "email", "parsedDt"]].rename(
    columns={"email": "email_before", "parsedDt": "parsed_before"}
)

# 4) Склеиваем эти "лучшие" email обратно к clients
out = (clients
       .merge(best_after, on="phone", how="left")
       .merge(best_before, on="phone", how="left")
)


# 5) Применяем правило выбора parsed email:
#    если есть after → берём after, иначе before
out["email_from_parsed"] = out["email_after"].combine_first(out["email_before"])

# 6) Финальный email для рассылки:
#    если у клиента email уже есть — берём его, иначе parsed
out["final_email"] = out["email"].combine_first(out["email_from_parsed"])

# Результат
out_to_send = out[["phone", "fio", "templateNum", "closed", "final_email"]]
print(out_to_send)

































#