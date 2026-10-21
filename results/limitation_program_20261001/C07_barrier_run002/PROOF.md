# Continuous one-date barrier-band proof

At date t>0, S_i(t)=S0*exp((r-sigma^2/2)t+sigma*sqrt(rho*t)Z+sigma*sqrt((1-rho)*t)Z_i). Conditioning on all idiosyncratic Brownian shocks gives B(t)=exp(s_c Z)W, s_c=sigma*sqrt(rho*t)>0, W>0 finite almost surely. The original independent continuous common Brownian driver makes Z standard Gaussian and independent of W.

For 0<=eta<H, the event H-eta<=B<=H+eta restricts Z to an interval of length L/s_c, L=log((H+eta)/(H-eta)). Its probability is at most min(1,L/(s_c*sqrt(2*pi))) for every W, hence also unconditionally.

Writing d=L/(2*s_c), a shifted interval has probability g(c)=Phi(c+d)-Phi(c-d). Its derivative is phi(c+d)-phi(c-d), nonpositive for c>=0 and nonnegative for c<=0. Thus its exact shift-independent supremum is g(0)=2*Phi(d)-1. No observed W or financial sample enters this bound.

Conditional on any finite positive W, B has a continuous lognormal law. Every deterministic endpoint, including B=H, has probability zero after averaging over W. The original alive test B<H and knockout convention B>=H are preserved; digital equality is not claimed to have probability zero.

If |B_digital-B_continuous|<=eta outside a separately bounded bad event E, then differing one-date barrier decisions imply E or |B_continuous-H|<=eta. Apply the unconditional Gaussian band bound plus P(E). Conditioning on E's complement can destroy Gaussian independence and is never used.

If a proved per-stock multiplicative/log discrepancy, including native exp and clipping, bounds each stock ratio between exp(-delta) and exp(delta), the positive equal-weight basket obeys the same ratio bounds. Different barrier decisions require H*exp(-delta)<=B_continuous<=H*exp(delta), whose log length is exactly 2*delta. The symmetric dollar radius H*(exp(delta)-1) also covers this band because 2-exp(delta)<=exp(-delta).

Given separately proved already-discounted smooth-payoff error zeta on the good domain, a discounted cap on the barrier-switch payoff difference, an any-contractual-date band probability and discounted bad-domain tail dollars, triangle inequality gives dollar_bias<=zeta+cap*P(any band)+tail_dollars. A one-date band alone supplies none of the remaining terms or full-path coverage. The original native output is already discounted: no second discount is applied.

Exact rational Machin pi intervals, integer-square-root enclosures and dyadic outward arithmetic are used. log((1+x)/(1-x)) is enclosed by its positive atanh series and geometric remainder. The centered Gaussian integral uses the integrated Taylor series for exp(-z^2/2); Taylor's derivative bound gives remainder <=8^(2m+3)/(2^(m+1)*(m+1)!*(2m+3)) for 0<=z<=8. Larger arguments use monotonicity and the rigorous probability cap one.
