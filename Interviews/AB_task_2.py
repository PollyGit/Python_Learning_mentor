import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Dict, Tuple, List, Union


class DistributionGenerator:
    def __init__(self, config: Dict):
        self.config = config
        self.sample_a = None
        self.sample_b = None
        self.params_a = {}
        self.params_b = {}
        self.metric_type = config['metric_type']
        self.n = config['n']
        self.seed = config.get('seed')
        self.quantile_q = config.get('quantile_q', 0.5)
        self.true_effect = None
        self.estimated_effect = None
        if self.seed is not None:
            np.random.seed(self.seed)

    def _generate_params(self) -> Tuple[Dict, Dict]:
        params_a, params_b = {}, {}

        if self.metric_type == 'ratio_metric':
            num_mu = np.random.uniform(self.config['num_mu_range'][0], self.config['num_mu_range'][1])
            num_sigma = np.random.uniform(self.config['num_sigma_range'][0], self.config['num_sigma_range'][1])
            denom_mu = np.random.uniform(self.config['denom_mu_range'][0], self.config['denom_mu_range'][1])
            denom_sigma = np.random.uniform(self.config['denom_sigma_range'][0], self.config['denom_sigma_range'][1])

            effect = np.random.uniform(-0.2 * (self.config['num_mu_range'][1] - self.config['num_mu_range'][0]),
                                       0.2 * (self.config['num_mu_range'][1] - self.config['num_mu_range'][0]))
            num_mu_b = num_mu + effect

            params_a = {'num_mean': num_mu, 'num_std': num_sigma, 'denom_mean': denom_mu, 'denom_std': denom_sigma}
            params_b = {'num_mean': num_mu_b, 'num_std': num_sigma, 'denom_mean': denom_mu, 'denom_std': denom_sigma}
            self.true_effect = effect / denom_mu if denom_mu != 0 else 0

        elif self.metric_type == 'conversion':
            p_a = np.random.uniform(self.config['value_range'][0], self.config['value_range'][1])
            effect = np.random.uniform(-0.2 * (self.config['value_range'][1] - self.config['value_range'][0]),
                                       0.2 * (self.config['value_range'][1] - self.config['value_range'][0]))
            p_b = np.clip(p_a + effect, 0, 1)

            params_a = {'p': p_a}
            params_b = {'p': p_b}
            self.true_effect = effect

        elif self.metric_type == 'quantile':
            mu = np.random.uniform(self.config['mu_range'][0], self.config['mu_range'][1])
            sigma_a = np.random.uniform(self.config['sigma_range'][0], self.config['sigma_range'][1])
            sigma_b = np.random.uniform(self.config['sigma_range'][0], self.config['sigma_range'][1])
            effect = np.random.uniform(-0.2 * (self.config['mu_range'][1] - self.config['mu_range'][0]),
                                       0.2 * (self.config['mu_range'][1] - self.config['mu_range'][0]))
            mu_b = mu + effect

            params_a = {'mean': mu, 'std': sigma_a}
            params_b = {'mean': mu_b, 'std': sigma_b}
            self.true_effect = effect

        elif self.metric_type == 'mean_metric':
            mu = np.random.uniform(self.config['mu_range'][0], self.config['mu_range'][1])
            sigma_a = np.random.uniform(self.config['sigma_range'][0], self.config['sigma_range'][1])
            sigma_b = np.random.uniform(self.config['sigma_range'][0], self.config['sigma_range'][1])
            effect = np.random.uniform(-0.2 * (self.config['mu_range'][1] - self.config['mu_range'][0]),
                                       0.2 * (self.config['mu_range'][1] - self.config['mu_range'][0]))
            mu_b = mu + effect

            params_a = {'mean': mu, 'std': sigma_a}
            params_b = {'mean': mu_b, 'std': sigma_b}
            self.true_effect = effect

        return params_a, params_b

    def generate_samples(self) -> Tuple[Union[np.ndarray, Tuple], Union[np.ndarray, Tuple]]:
        self.params_a, self.params_b = self._generate_params()

        if self.metric_type == 'ratio_metric':
            num_a = np.random.normal(self.params_a['num_mean'], self.params_a['num_std'], self.n)
            denom_a = np.random.normal(self.params_a['denom_mean'], self.params_a['denom_std'], self.n)
            num_b = np.random.normal(self.params_b['num_mean'], self.params_b['num_std'], self.n)
            denom_b = np.random.normal(self.params_b['denom_mean'], self.params_b['denom_std'], self.n)
            self.sample_a = (num_a, denom_a)
            self.sample_b = (num_b, denom_b)
            self.estimated_effect = (np.mean(num_b) / np.mean(denom_b)) - (np.mean(num_a) / np.mean(denom_a))

        elif self.metric_type == 'conversion':
            self.sample_a = np.random.binomial(1, self.params_a['p'], self.n)
            self.sample_b = np.random.binomial(1, self.params_b['p'], self.n)
            self.estimated_effect = np.mean(self.sample_b) - np.mean(self.sample_a)

        elif self.metric_type == 'quantile':
            self.sample_a = np.random.normal(self.params_a['mean'], self.params_a['std'], self.n)
            self.sample_b = np.random.normal(self.params_b['mean'], self.params_b['std'], self.n)
            self.estimated_effect = np.quantile(self.sample_b, self.quantile_q) - np.quantile(self.sample_a,
                                                                                              self.quantile_q)

        elif self.metric_type == 'mean_metric':
            self.sample_a = np.random.normal(self.params_a['mean'], self.params_a['std'], self.n)
            self.sample_b = np.random.normal(self.params_b['mean'], self.params_b['std'], self.n)
            self.estimated_effect = np.mean(self.sample_b) - np.mean(self.sample_a)

        return self.sample_a, self.sample_b

    def statistical_test(self) -> float:
        if self.metric_type == 'ratio_metric':
            num_a, denom_a = self.sample_a
            num_b, denom_b = self.sample_b
            return self._linearization(num_a, denom_a, num_b, denom_b)

        elif self.metric_type == 'conversion':
            contingency_table = pd.crosstab(
                np.array([0] * len(self.sample_a) + [1] * len(self.sample_b)),
                np.concatenate([self.sample_a, self.sample_b])
            )
            return stats.chi2_contingency(contingency_table)[1]

        elif self.metric_type == 'quantile':
            return self._bootstrap_quantile_test()

        elif self.metric_type == 'mean_metric':
            return stats.ttest_ind(self.sample_a, self.sample_b).pvalue

    def _linearization(self, num_t: np.ndarray, denom_t: np.ndarray,
                       num_c: np.ndarray, denom_c: np.ndarray) -> float:
        def to_np_array(*arrays):
            res = [np.array(arr, dtype='float') for arr in arrays]
            return res if len(res) > 1 else res[0]

        def lin(num, denom, cntrl_ratio):
            return num - cntrl_ratio * denom

        num_t, denom_t, num_c, denom_c = to_np_array(num_t, denom_t, num_c, denom_c)
        cntrl_ratio = num_c.sum() / denom_c.sum()

        lin_signals_t = lin(num_t, denom_t, cntrl_ratio)
        lin_signals_c = lin(num_c, denom_c, cntrl_ratio)

        return stats.ttest_ind(lin_signals_t, lin_signals_c).pvalue

    def _bootstrap_quantile_test(self, n_bootstraps: int = 1000) -> float:
        def get_quantile(data):
            return np.quantile(data, self.quantile_q)

        deltas = []
        for _ in range(n_bootstraps):
            boot_a = np.random.choice(self.sample_a, size=self.n, replace=True)
            boot_b = np.random.choice(self.sample_b, size=self.n, replace=True)
            deltas.append(get_quantile(boot_b) - get_quantile(boot_a))

        return 2 * min(np.mean(np.array(deltas) > 0), np.mean(np.array(deltas) < 0))

    def _z_test_proportions(self) -> float:
        """Проводит z-test на пропорции и возвращает p-value."""
        p1 = np.mean(sample_a)
        p2 = np.mean(sample_b)
        n1 = len(sample_a)
        n2 = len(sample_b)

        p_pooled = (np.sum(sample_a) + np.sum(sample_b)) / (n1 + n2)
        se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n1 + 1 / n2)) if p_pooled != 0 and p_pooled != 1 else 1e-10
        z = (p2 - p1) / se if se != 0 else 0
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))

        return p_value

    def visualize(self):
        if self.metric_type == 'conversion':
            fig, ax = plt.subplots(figsize=(6, 5))
            conv_a = np.mean(self.sample_a)
            conv_b = np.mean(self.sample_b)
            sns.barplot(x=['A', 'B'], y=[conv_a, conv_b], ax=ax)
            ax.set_title('Conversion Rates')
            ax.set_ylabel('Conversion Rate')
            plt.tight_layout()
            plt.show()

        elif self.metric_type == 'ratio_metric':
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            num_a, denom_a = self.sample_a
            num_b, denom_b = self.sample_b
            ratios_a = num_a / denom_a
            ratios_b = num_b / denom_b
            sns.histplot(ratios_a, ax=ax1, label='Sample A', alpha=0.5)
            sns.histplot(ratios_b, ax=ax1, label='Sample B', alpha=0.5)
            ax1.set_title('Ratio Distributions (num/denom)')
            ax1.legend()

            x = np.linspace(min(ratios_a.min(), ratios_b.min()),
                            max(ratios_a.max(), ratios_b.max()), 100)
            ax2.plot(x, stats.norm.pdf(x, np.mean(ratios_a), np.std(ratios_a)),
                     label='A Theoretical')
            ax2.plot(x, stats.norm.pdf(x, np.mean(ratios_b), np.std(ratios_b)),
                     label='B Theoretical')
            ax2.set_title('Theoretical Ratio Distributions')
            ax2.legend()
            plt.tight_layout()
            plt.show()

        else:  # mean_metric и quantile
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            sns.histplot(self.sample_a, ax=ax1, label='Sample A', alpha=0.5)
            sns.histplot(self.sample_b, ax=ax1, label='Sample B', alpha=0.5)
            ax1.set_title('Sample Distributions')
            ax1.legend()

            x = np.linspace(min(self.sample_a.min(), self.sample_b.min()),
                            max(self.sample_a.max(), self.sample_b.max()), 100)
            ax2.plot(x, stats.norm.pdf(x, self.params_a['mean'], self.params_a['std']),
                     label='A Theoretical')
            ax2.plot(x, stats.norm.pdf(x, self.params_b['mean'], self.params_b['std']),
                     label='B Theoretical')
            ax2.set_title('Theoretical Distributions')
            ax2.legend()
            plt.tight_layout()
            plt.show()

    def print_results(self):
        print(f"Metric Type: {self.metric_type}")
        print("\nGenerated Parameters:")
        print(f"Group A: {self.params_a}")
        print(f"Group B: {self.params_b}")
        print(f"\nTrue Effect: {self.true_effect:.4f}")
        print(f"Estimated Effect: {self.estimated_effect:.4f}")
        if self.metric_type == 'conversion':
            base_value = self.params_a['p']
        elif self.metric_type == 'quantile':
            base_value = self.params_a['mean']
        elif self.metric_type == 'mean_metric':
            base_value = self.params_a['mean']
        else:  # ratio_metric
            base_value = self.params_a['num_mean'] / self.params_a['denom_mean'] if self.params_a[
                                                                                        'denom_mean'] != 0 else 0
        relative_effect = (self.estimated_effect / base_value * 100) if base_value != 0 else 0
        print(f"Relative Effect: {relative_effect:.2f}%")
        if self.metric_type == 'conversion':
            p_chi2 = self.statistical_test()
            p_z_test = self._z_test_proportions()
            print(f'P-value chi2: {p_chi2:.4f}')
            print(f'P-value z-test: {p_z_test:.4f}')
        else:
            print(f"P-value: {self.statistical_test():.4f}")
        print(f"True effect exists: {self.true_effect is not None and abs(self.true_effect) > 0}")


# Конфигурация для A/B теста
simulation_config = {
    "ratio_metric": {
        "metric_type": "ratio_metric",
        "n": 1000,
        "num_mu_range": (50, 300),
        "num_sigma_range": (10, 50),
        "denom_mu_range": (1, 10),
        "denom_sigma_range": (0.5, 2),
        "seed": 11
    },
    "conversion": {
        "metric_type": "conversion",
        "n": 1000,
        "value_range": (0.05, 0.25),
        "seed": 11
    },
    "quantile": {
        "metric_type": "quantile",
        "n": 1000,
        "mu_range": (10, 200),
        "sigma_range": (5, 30),
        "quantile_q": 0.5,
        "seed": 11
    },
    "mean_metric": {
        "metric_type": "mean_metric",
        "n": 1000,
        "mu_range": (50, 51),
        "sigma_range": (10, 50),
        "seed": 11
    }
}

# Пример использования
if __name__ == "__main__":
    for metric, config in simulation_config.items():
        print(f"\n=== Testing {metric.upper()} ===")
        generator = DistributionGenerator(config)
        sample_a, sample_b = generator.generate_samples()
        generator.visualize()
        generator.print_results()