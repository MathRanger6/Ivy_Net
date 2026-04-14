# Empirical Design: College Basketball → Professional Entry

## Outcome

\[
Y_i =
\begin{cases}
1 & \text{if player enters professional basketball} \\
0 & \text{otherwise}
\end{cases}
\]

## Pool Quality

\[
\text{PoolQ}_{jt}^{(-i)} =
\frac{1}{N_{jt}-1}
\sum_{k \neq i} \text{Perf}_{kt}
\]

## Model

\[
Y_i =
\beta_1 \text{Perf}_i +
\beta_2 \text{PoolQ}_{jt}^{(-i)} +
\beta_3 \left(\text{PoolQ}_{jt}^{(-i)}\right)^2 +
X_i'\gamma + \varepsilon_i
\]

\[
\beta_3 < 0
\]
