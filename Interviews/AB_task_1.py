import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Dict, Tuple, List, Union


def generate_user_actions(n_users: int, p: float, seed: int = None) -> np.ndarray:
    """Генерирует бинарные действия пользователей с вероятностью конверсии p."""
    if seed is not None:
        np.random.seed(seed)
    return np.random.binomial(1, p, n_users)


def split_traffic(actions: np.ndarray, split_ratio: float = 0.5, seed: int = None) -> Tuple[np.ndarray, np.ndarray]:
    """Разделяет пользователей на группы A и B случайным образом."""
    if seed is not None:
        np.random.seed(seed)
    n_users = len(actions)
    indices = np.random.permutation(n_users)
    n_a = int(n_users * split_ratio)
    group_a = actions[indices[:n_a]]
    group_b = actions[indices[n_a:]]
    return group_a, group_b


def z_test_proportions(group_a: np.ndarray, group_b: np.ndarray) -> float:
    """Проводит z-test на пропорции и возвращает p-value."""
    p1 = np.mean(group_a)
    p2 = np.mean(group_b)
    n1 = len(group_a)
    n2 = len(group_b)

    p_pooled = (np.sum(group_a) + np.sum(group_b)) / (n1 + n2)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n1 + 1 / n2)) if p_pooled != 0 and p_pooled != 1 else 1e-10
    z = (p2 - p1) / se if se != 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    return p_value


def run_aa_test(n_users: int, p: float, split_ratio: float = 0.5, seed: int = None, max_delta: float = 0.05) -> float:
    """Проводит один AA-тест и возвращает p-value."""
    if seed is not None:
        np.random.seed(seed)

    delta = np.random.uniform(0, max_delta)  # Случайное смещение для p_B
    p_a = p
    p_b = p
    actions_a = generate_user_actions(int(n_users * split_ratio), p_a, seed)
    actions_b = generate_user_actions(int(n_users * (1 - split_ratio)), p_b, seed + 1 if seed is not None else None)

    p_value = z_test_proportions(actions_a, actions_b)
    return p_value


def simulate_aa_tests(n_simulations: int, n_users: int, p: float, split_ratio: float = 0.5,
                      max_delta: float = 0.05) -> np.ndarray:
    """Проводит n_simulations AA-тестов и возвращает массив p-value."""
    p_values = []
    for i in range(n_simulations):
        seed = 42 + i
        p_value = run_aa_test(n_users, p, split_ratio, seed, max_delta)
        p_values.append(p_value)
    return np.array(p_values)


def plot_p_value_distribution(p_values: np.ndarray, title: str):
    """Строит гистограмму распределения p-value."""
    plt.figure(figsize=(10, 6))
    sns.histplot(p_values, bins=20, stat='density', color='blue', alpha=0.5)
    plt.axhline(y=1, color='red', linestyle='--', label='Uniform distribution')
    plt.title(title)
    plt.xlabel('p-value')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True)
    plt.show()


# Параметры симуляции
n_simulations = 1000  # Количество AA-тестов
n_users = 1000  # Количество пользователей в тесте
p = 0.1  # Базовая вероятность конверсии
split_ratio = 0.5  # Доля для группы A

# Симуляция с равномерным перекосом влево
p_values_bias = simulate_aa_tests(n_simulations, n_users, p, split_ratio)
print("\n=== С равномерным перекосом влево ===")
print(f"Mean p-value: {np.mean(p_values_bias):.4f}")
print(f"Std p-value: {np.std(p_values_bias):.4f}")
print(f"Share of p-values < 0.05: {np.mean(p_values_bias < 0.05):.4f}")
plot_p_value_distribution(p_values_bias, 'Distribution of p-values (With Uniform Left Skew)')