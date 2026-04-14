
# Empirical Design (LaTeX)

## Outcome
\[
Y_i=
\begin{cases}
1 & \text{if pro entry}\\
0 & \text{otherwise}
\end{cases}
\]

## Pool Quality
\[
\text{PoolQ}_{jt}^{(-i)}=\frac{1}{N_{jt}-1}\sum_{k\neq i}\text{Perf}_{kt}
\]

## Model
\[
\Pr(Y_i=1)=f(\text{Perf}_i+\text{PoolQ}_{jt}^{(-i)}+\left(\text{PoolQ}_{jt}^{(-i)}\right)^2)
\]
