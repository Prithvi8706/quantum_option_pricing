# F23 omitted-mode dollar bound for the original B4/B8 contracts

The original parameters are S0=K=100, H=140, sigma=3/10, rho=2/5, r=3/100 and T=1, with 12 or 52 equal contractual dates. Write the continuous full log-price vector as m+LZ and its rank-r approximation as m+L_r Z_r, with the original deterministic drift m_ij=log(S0)+(r-sigma^2/2)t_j. Retained and omitted independent standard normals give X=X_r+R, with R independent of X_r and marginal variance v_omit. This is an explicit covariance approximation, including changed marginal stock expectations. It is not the original finite Box-Muller/native circuit.

The asset covariance eigenvalues are sigma^2(1+(a-1)rho) for the normalized common vector and sigma^2(1-rho) for the a-1 Helmert vectors. The contractual-time covariance Delta min(i,j) has eigenvalues Delta/[4 sin^2((2k-1)pi/(2(2n+1)))] and eigenvectors proportional to sin((2k-1)i pi/(2n+1)), k=1,...,n. Their squared norm is (2n+1)/4. These follow by applying the tridiagonal inverse (diagonal 2 except terminal 1, off-diagonal -1) to each sine vector; distinct eigenvectors are orthogonal. Tensor products diagonalize the separable original covariance. The canonical ordering is descending eigenvalue, then asset/time indices, with exact repeated Helmert/time eigenvalues recognized. No approximate tie decision is allowed. The shared `basis.py` supplies the same intended formulas; it is read-only and is not imported by this screen.

For one fixing S=S_r exp(R), R~N(0,v_omit), independence and the original full drift give

```text
E|S-S_r| = S0 exp(r t) [2 Phi(sqrt(v_omit))-1]
          <= S0 exp(r t) sqrt(2 v_omit/pi).
```

Indeed E|exp(R)-1|=exp(v_omit/2)[2Phi(sqrt(v_omit))-1], while E S_r=S0 exp(rt-v_omit/2). The final inequality integrates the standard normal density from 0 to sqrt(v_omit) and uses its maximum 1/sqrt(2pi). The identity has its continuous v_omit=0 limit. For date basket B_j and average A, triangle inequality gives Delta_j=(1/a)sum_i S0 exp(rt_j)sqrt(2 v_omit,ij/pi) as an upper bound on E|B_j-B_r,j|, and (1/n)sum_j Delta_j bounds E|A-A_r|. The positive part is 1-Lipschitz, so the discounted unbarriered call difference is at most d times this average, d=exp(-rT).

For the monitored knock-out, both full and approximate stock vectors stay positive and use every original date. On either law's strict survival all monitored baskets are below H, so its average is below H and its discounted payoff lies in [0,d(H-K)]. Let I and I_r be their survival indicators. Pathwise,

```text
|d(A-K)+ I - d(A_r-K)+ I_r|
 <= d|A-A_r| + d(H-K) 1{I != I_r}.
```

If all basket errors are at most eta and no original basket is within eta of H, survival agrees, including the strict barrier ties. Thus Markov and a union bound give

```text
P(I != I_r) <= min(1, sum_j Delta_j/eta
                       + sum_j P(|B_j-H| <= eta)).
```

The ORIGINAL full GBM basket at date t_j factors as B_j=exp(sigma sqrt(rho) W_common(t_j)) C_j, with C_j>0 independent of the common Brownian value. Conditional on C_j, log B_j has normal variance sigma^2 rho t_j. Its density is bounded by 1/[sigma sqrt(2pi rho t_j)]. For 0<eta<H this proves

```text
P(|B_j-H| <= eta)
 <= min(1, log((H+eta)/(H-eta)) / [sigma sqrt(2pi rho t_j)]).
```

This band bound uses the original common factor, not an assumed common factor in the truncated law. Combine these expressions for eta=1,5,10. The final valid dollar upper bound is the minimum of the three combined bounds and the law-independent d(H-K) support bound. At full rank, the two paths coincide exactly and the bound is zero directly, without taking a spurious positive band limit. An upper bound that misses the prospective allowance cannot prove actual price bias large.

All expressions are enclosed by outward dyadic120 rational arithmetic. Alternating Machin arctangents bound pi. Sine Taylor uses 32 terms and a Lagrange remainder bounded by 2^65/65! after periodic reduction into [0,pi/2]. Positive exponential and atanh series include analytic tails; square roots use integer-square-root brackets. Interval ordering and diagonal/trace identities are checked. Finite diagnostic checks support the arithmetic implementation; the inequalities above are population coupling proofs.

The [Sigman GBM notes, sections 1.2.3 and 1.3](https://www.columbia.edu/~ks20/4703-07/4703-07-Notes-BM-GBM-I.pdf) support the exponential GBM representation and independent increments, not the omission-error formula (derived here). The locally frozen F16 copy is read-only at SHA256 `c86059f6ac619b51a19f09450433d1a382db8ba54d155dbfe4abefafa68d849e`. No smoothness/integration theorem or finite-law/native bridge is inferred from this continuous model proof. Preparation, source/inverse, path arithmetic, finite-law and physical eligibility remain separate obligations. No timing or adoption is part of this screen.
