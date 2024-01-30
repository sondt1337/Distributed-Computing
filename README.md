# Distributed Computing
Please check our paper research for more information: [A_Secure_PolyDot_Matrix_Multiplication_Approach_For_Distributed_Computing.pdf](/Paper-Research/A_Secure_PolyDot_Matrix_Multiplication_Approach_For_Distributed_Computing.pdf)
## Input 

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

## Process
### 1. Encode 
The Master node encodes the submatrices of X & Y using the functions F & G below:

$$
F(z) = \sum_{i=1}^{m} \sum_{j=1}^{n} X_{i,j} z^{n \cdot (i-1) + j-1}
$$

$$
G(z) = \sum_{k=1}^{n} \sum_{l=1}^{p} Y_{k,l} z^{n-k + mn(i-1)}
$$

where F and G are encode function satisfied F: $\mathbb{F}^{\frac{M}{m} \times \frac{N}{n}} \rightarrow \mathbb{F}^{\frac{M}{m} \times \frac{N}{n}}$ and G: $\mathbb{G}^{\frac{M}{m} \times \frac{N}{n}} \to \mathbb{G}^{\frac{M}{m} \times \frac{N}{n}}$

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

### 3. Decoding (Result recovering)


## POLYDOT WITH SECURITY

## Structure
![](/Distributed-Computing/image.png)

## Author 
If you have any question about this research, please contact us:

Thai Son Dinh: sondinh99999@gmail.com
Dang Anh Duc Pham: anhduc03nb@gmail.com
