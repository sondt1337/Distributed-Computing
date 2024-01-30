# Distributed Computing with Matrix Multiplication
## Structure
![](/Distributed-Computing/image.png)

## PolyDot Code without security

Master node partition the matrix 

$$
\mathbf{X} = \begin{pmatrix}
X_{1,1} & \cdots & X_{1,n} \\
\vdots  & \ddots & \vdots \\
X_{m,1} & \cdots & X_{m,n}
\end{pmatrix}
\quad ,
\mathbf{Y} = \begin{pmatrix}
Y_{1,1} & \cdots & Y_{1,p} \\
\vdots  & \ddots & \vdots \\
Y_{n,1} & \cdots & Y_{n,p}
\end{pmatrix}
$$

where $m | M, n | N, p | P, X_{i,j} \in \mathbb{F}^{\frac{M}{m} \times \frac{N}{n}}, Y_{k, l} \in \mathbb{F}^{\frac{N}{n} \times \frac{P}{p}}$.

The resulting matrix $Z=XY$ is represented as follows:

$$
\mathbf{Z} = \begin{pmatrix}
Z_{1,1} & \cdots & Z_{1,p} \\
\vdots  & \ddots & \vdots \\
Z_{m,1} & \cdots & Z_{m,p}
\end{pmatrix}
\quad
$$

with
$$
Z_{u, v} = \sum_{k=1}^{n} X_{u,k} Y_{v, k}, u \in {1, 2, ..., m},  v \in {1, 2, 3, ..., p}
$$ 


### 1. Encode 
The Master node encodes the submatrices of X & Y using the functions F & G below:

$$
F(z) = \sum_{i=1}^{m} \sum_{j=1}^{n} X_{i,j} z^{n \cdot (i-1) + j-1}
$$

$$
G(z) = \sum_{k=1}^{n} \sum_{l=1}^{p} Y_{k,l} z^{n-k + mn(i-1)}
$$

where F and G are encode function satisfied F: $\mathbb{F}^{\frac{M}{m} \times \frac{N}{n}} \rightarrow \mathbb{F}^{\frac{M}{m} \times \frac{N}{n}}$ and G: $\mathbb{F}^{\frac{N}{n} \times \frac{P}{p}} \to \mathbb{F}^{\frac{N}{n} \times \frac{P}{p}}$

### 2. Task computing
$i$-th worker calculate $F(z_{i})G(z_{i})$. As soon as worker $i$ completes  the computation, it will send
the result back to themaster node, noting that the returned
results from the workers may vary in speed depending on each worker’s computational capabilities, and the returned results may not be accurate.

$$
\begin{align*}
F(z)G(z) &= (\sum_{i=1}^{m} \sum_{j=1}^{n} X_{i, j} z^{n(i-1)+j-1}) \times \\
&\quad(\sum_{k=1}^{n} \sum_{l=1}^{p} Y_{k, l} z^{n-k + mn(l-1)}) \\
&= \sum_{i, j, k, l}^{}X_{i, j} Y_{k, l} Z ^{n(i-1)+j-1+n-k + mn(l-1)}
\end{align*}
$$

The coefficient of $Z_{u, v}$ in the  polynomial corresponding to the exponent z is $n(u-1) + n-1 +mn(v-1)$ in the case where the index $j = k$ in $X_{i,j}$ and $Y_{k,l}$
### 3. Decoding (Result recovering)
The master node will collect the fastest R results returned by the workers. Afterward, the master node will recover the result $Z_{i, j}$ with $i \in {1,2,...,m}, j \in {1,2,...,p}$ based on polynomial interpolation.

Since the degree of the polynomial is $mnp + n - 2$, when applying the polynomial interpolation method, a minimum of $mnp + n - 1$ values is required to achieve the fastest results from the workers for the recovery of the matrix $Z$. Therefore, the recovery threshold is:

$$
\begin{align*} 
P_R = mnp + n - 1
\end{align*}
$$

and communication load is:
$$
\begin{align*} 
C_L = P_D \frac{MP}{mp}
\end{align*}
$$
## PolyDot Code with security

### 1. Encode
To accomplish this objective,we add rows or columns containing random elements to matrices A and B, respectively.From there, we consider two distinct cases:

#### a. Case 1: $n < m$

$$
\begin{align*} 
\Delta_{P_C} = \lceil \frac{P_C} {n}\rceil
\end{align*}
$$

#### b. Case 2: $n \geq m$

$$
\begin{align*}
\Delta_{P_C} = \left\lceil \frac{P_C}{\min\{ m, p \}} \right\rceil
\end{align*}
$$

###  2. Verification key
Let $n_0=\frac{N}{n},m_0=\frac{M}{m},p_0=\frac{P}{p}$.

In case: $m_0 < p_0$ The master node will generate the key $k_i$ corresponding to $F^{* }(z_i)$, where the vectors $k^{T}_{i} \in \mathbb{F}^{m^{* }}$, as follows:

$$
\begin{align*}
R_i = k_i F^{* }(z_i)
\end{align*}
$$

In case: $m_0 \geq p_0$, master node will generate vector $k_i \in \mathbb{F}^{p^{* }}$ corresponding to G∗(zi)as follow:

$$
\begin{align*}
R_i= G^{* }(z_i)k_i
\end{align*}
$$

#### 3. Task computing 
After generating thekey, themaster code will send $F^{* }(z_i)$ and $G^{* }(z_i)$ to each i-thworker.The workers perform computations:

$$
\begin{align*}
F_z(z_i) = F^{* }(z_i)G^{* }(z_i)
\end{align*}
$$

## Contact
### Paper
If you have any question about this research, please check our research paper for more information: [A_Secure_PolyDot_Matrix_Multiplication_Approach_For_Distributed_Computing.pdf](/Paper-Research/A_Secure_PolyDot_Matrix_Multiplication_Approach_For_Distributed_Computing.pdf)
### Authors
Thai Son Dinh: sondinh99999@gmail.com

Dang Anh Duc Pham: anhduc03nb@gmail.com
