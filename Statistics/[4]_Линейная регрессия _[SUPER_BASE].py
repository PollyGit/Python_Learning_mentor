# Пример из интернета на вопрос, как зависят коэф регресии и корреляции

# Демонстрация: корреляции vs коэффициенты регрессии (множественная коллинеарность)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.linalg import lstsq

rng = np.random.default_rng(42)
n = 300

# Два сильно связанные признака (почти дубликаты)
X1 = rng.normal(0, 1, n)
X2 = 0.9 * X1 + rng.normal(0, 0.3, n)  # высокая корреляция X1~X2

# Истинная генерация таргета (вклад X1 значительно больше)
eps = rng.normal(0, 1, n)
y = 3.0 * X1 + 0.2 * X2 + eps

df = pd.DataFrame({"X1": X1, "X2": X2, "y": y})

# 1) Парные корреляции
corr = df[["X1", "X2", "y"]].corr()

# 2) Простые регрессии (y~X1) и (y~X2)
def simple_ols(x, y):
    X = np.column_stack([np.ones(len(x)), x])
    beta, *_ = lstsq(X, y, rcond=None)
    yhat = X @ beta
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    return {"intercept": beta[0], "beta": beta[1], "R2": r2}

s1 = simple_ols(df["X1"].values, df["y"].values)
s2 = simple_ols(df["X2"].values, df["y"].values)
simple_tbl = pd.DataFrame([s1, s2], index=["y ~ X1", "y ~ X2"])

# 3) Множественная регрессия (y~X1+X2)
X = np.column_stack([np.ones(n), df["X1"].values, df["X2"].values])
beta_full, *_ = lstsq(X, df["y"].values, rcond=None)
yhat_full = X @ beta_full
ss_res = np.sum((df["y"].values - yhat_full) ** 2)
ss_tot = np.sum((df["y"].values - df["y"].values.mean()) ** 2)
r2_full = 1 - ss_res / ss_tot
multi_tbl = pd.DataFrame(
    {"coef": beta_full, "": ["intercept", "X1", "X2"]}
).set_index("")

# 4) Стандартизованные коэффициенты (z-оценки, без интерсепта)
Z = df[["X1", "X2", "y"]].apply(lambda c: (c - c.mean()) / c.std(ddof=0))
Xz = Z[["X1", "X2"]].values  # уже центрованные и со скейлом=1
yz = Z["y"].values
beta_std, *_ = lstsq(Xz, yz, rcond=None)  # без интерсепта (среднее=0)
std_tbl = pd.DataFrame({"std_beta": beta_std}, index=["X1", "X2"])

# 5) VIF (наглядность коллинеарности): 1/(1 - R^2_j), где R^2_j из регрессии Xj ~ остальные
def r2_of_regress(y, X):
    beta, *_ = lstsq(X, y, rcond=None)
    yhat = X @ beta
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return 1 - ss_res / ss_tot

r2_x1_on_x2 = r2_of_regress(df["X1"].values, np.column_stack([np.ones(n), df["X2"].values]))
r2_x2_on_x1 = r2_of_regress(df["X2"].values, np.column_stack([np.ones(n), df["X1"].values]))
vif_tbl = pd.DataFrame({"VIF": [1/(1 - r2_x1_on_x2), 1/(1 - r2_x2_on_x1)]}, index=["X1", "X2"])

# Показ таблиц

# нет в доступе этого файла юпитер ноутбука
import caas_jupyter_tools
caas_jupyter_tools.display_dataframe_to_user("1) Парные корреляции", corr.round(3))
caas_jupyter_tools.display_dataframe_to_user("2) Простые регрессии (y~X1 и y~X2)", simple_tbl.round(3))
caas_jupyter_tools.display_dataframe_to_user("3) Множественная регрессия (y~X1+X2): коэффициенты и R^2",
                                             pd.concat([multi_tbl.round(3),
                                                        pd.DataFrame({"coef":[np.nan, np.nan, np.nan], "R2":[r2_full, np.nan, np.nan]},
                                                                     index=["intercept","X1","X2"]).round(3)], axis=1))
caas_jupyter_tools.display_dataframe_to_user("4) Стандартизованные коэффициенты (y,z ~ Xz1+Xz2)", std_tbl.round(3))
caas_jupyter_tools.display_dataframe_to_user("5) VIF (диагностика коллинеарности)", vif_tbl.round(3))

# Два простых графика для интуиции
# (а) y vs X1 с линией простой регрессии
plt.figure(figsize=(6,4))
plt.scatter(df["X1"].values, df["y"].values, alpha=0.6)
x_line = np.linspace(df["X1"].min(), df["X1"].max(), 100)
y_line = s1["intercept"] + s1["beta"] * x_line
plt.plot(x_line, y_line)
plt.xlabel("X1")
plt.ylabel("y")
plt.title("Простая регрессия: y ~ X1")
plt.show()

# (б) X1 vs X2 (показать сильную корреляцию предикторов)
plt.figure(figsize=(6,4))
plt.scatter(df["X1"].values, df["X2"].values, alpha=0.6)
plt.xlabel("X1")
plt.ylabel("X2")
plt.title("Высокая коллинеарность: X1 vs X2")
plt.show()
