# Pre-acquisition extension: parity control

The first controlled-residual pilot showed that its rigorous moment bound was
much smaller than cap squared, but exercise-state bounds were still loose.
Before acquiring any parity-control results, add the following development
experiment (not held-out confirmation).

Use the SAME uncapped financial target. The preceding experiment used an
analytic cap bridge; put-call parity lets this follow-up work directly with
the uncapped contract and a bounded residual. Let A,G be future arithmetic and
geometric averages, q=exp(-r(T-tau))/2, k=2(K-accrued), and

    F = q(E[A|X]-k), Pg = q E[(k-G)+|X],
    R = q[(k-G)+-(k-A)+] >= 0,
    C = F + Pg - E[R|X].

Arithmetic/geometric ordering and accrued>=0 imply R<=exp(-r(T-tau))*K.
Clip the continuation policy V into a proved interval [L,U] with
max(F,0)<=L<=C<=U<=F+Pg. Then a=F+Pg-V is between zero and Pg, and

    Y = 1(V>Kc)*(a-R),
    P = exp(-r*tau) E[(V-Kc)+ + Y + regret].

Y is bounded, and its conditional second moment is bounded analytically using
the lesser of the arithmetic/geometric spread moment and geometric-put second
moment. This avoids using a sampled maximum as a support bound. A small
sampled moment still cannot be inserted into the quantum schedule as a proof.

Repeat the fixed sixteen-replicate, 1024 outer by 2048 inner pilot for ALL
twelve contracts, with independent root 2026092503. Fixed 32-replicate classical
comparisons use root 2026092504, outer8192, inner16/256. Preserve all earlier
results. If tighter population moments matter for costing, predeclare a
separate fixed-N iid upper-confidence calculation, including its tail/range
term and failure probability. Do not stop on its observed confidence interval.

This is standard put-call parity and control-variate reasoning. No novelty or
quantum superiority follows from the decomposition alone. Prices, policy
regret, classical preprocessing, quantum loading and uncomputation still count.
