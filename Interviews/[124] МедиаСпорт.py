# Есть функция random2(), которая равновероятно возвращает 1 или 0.
# Используя неизменную функцию random2(), надо написать функцию random3(), которая равновероятно возвращает 0 / 1 /2

import plotly.express as px
import pandas as pd
import numpy as np
import random

def random2():
    return random.randint(0,1)


def random3():
    while True:
        a = random2()
        b = random2()
        val = a * 2 + b
        if val < 3:
            return val



#решение из чат гпт

import numpy as np
import pandas as pd
import re

# ---- 1) Синтетический датасет (20000 строк) --------------------------------
n = 20_000
rng = np.random.default_rng(42)

# user_id: 15 символов из набора "1234567890abcdefghijklmnopqrstuvwxyz"
alphabet = np.array(list("1234567890abcdefghijklmnopqrstuvwxyz"))
user_id = ["".join(rng.choice(alphabet, size=15)) for _ in range(n)]

# payment_provider_number: случайные 1..10
payment_provider_number = rng.integers(1, 11, size=n)

# click2deposit: N(1440, 200), можно обрезать снизу нулём (по желанию)
click2deposit = rng.normal(1440, 200, size=n)

# deposit_amount: N(2025, 1000), отрицательные → 0
deposit_amount = rng.normal(2025, 1000, size=n)
deposit_amount = np.clip(deposit_amount, 0, None)

# retention: {1:0.35, 2:0.25, 3:0.20, 4:0.15, 5:0.05}
ret_vals = np.array([1, 2, 3, 4, 5])
ret_p    = np.array([0.35, 0.25, 0.20, 0.15, 0.05])
retention = rng.choice(ret_vals, size=n, p=ret_p)

df = pd.DataFrame({
    "user_id": user_id,
    "payment_provider_number": payment_provider_number,
    "click2deposit": click2deposit,
    "deposit_amount": deposit_amount,
    "retention": retention,
})

# Если у user_id есть дубликаты — оставляем первое
df = df.drop_duplicates("user_id", keep="first").reset_index(drop=True)

# ---- Задача 1. Среднее время до депозита по платёжной системе ---------------
avg_c2d = (
    df.groupby("payment_provider_number", as_index=False)["click2deposit"]
      .mean()
      .rename(columns={"click2deposit": "avg_click2deposit_by_provider"})
)
df = df.merge(avg_c2d, on="payment_provider_number", how="left")

# ---- Задача 2. Функция по user_id -------------------------------------------
# «все буквы в исходном порядке» + «квадрат числа, полученного из всех цифр user_id»
def transform_user_id(uid: str) -> str:
    letters = re.sub(r"[^A-Za-z]", "", uid)
    digits  = re.sub(r"[^0-9]", "", uid)
    num_sq  = str(int(digits or "0") ** 2)  # big int — ок в Python
    return letters + num_sq

# ---- Задача 3. Применить функцию и сохранить в новый столбец ----------------
# циклов снаружи нет; map вызовет функцию для каждой строки
df["user_id_feature"] = df["user_id"].map(transform_user_id)

# ---- Задача 4. Мода/медиана/среднее/дисперсия/ст.откл. ----------------------
cols = ["click2deposit", "deposit_amount", "retention"]

# базовые агрегаты
basic_stats = df[cols].agg(["mean", "median", "var", "std"]).T

# мода (если несколько мод — берём первую)
modes = {c: (df[c].mode().iloc[0] if not df[c].mode().empty else np.nan) for c in cols}
basic_stats["mode"] = pd.Series(modes)

basic_stats = basic_stats[["mode", "median", "mean", "var", "std"]]
print(basic_stats)

















