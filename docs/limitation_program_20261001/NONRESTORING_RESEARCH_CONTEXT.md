# Non-restoring root research context and matched oracle

Non-restoring quantum square-root circuits have an established primary literature, including [Muñoz-Coreas and Thapliyal's original design](https://arxiv.org/abs/1712.08254) and [Kupryianau and Niemiec's Qrisp implementation](https://arxiv.org/html/2507.12603v1). The latter explicitly describes a computation whose radicand register becomes the remainder, alongside the root output. Its reported adder and circuit resources cannot be transferred directly to this project's input-preserving, root-only clean-XOR oracle.

This local experiment implements one signed-remainder recurrence family using the existing exact X/CX/CCX backend. It retains every remainder snapshot, derives each new root bit from the new remainder's sign, copies only the root into the arbitrary native output word, and reverses the entire computation. No Qrisp package, external hardware job, published headline savings or uncharged remainder output is part of the measured result.

Our independent invariant is stated in terms of each processed base-four radicand prefix `N`, current floor root `Q`, and signed remainder `R`:

- For `R >= 0`, `R = N - Q²`.
- For `R < 0`, `R = N - (Q+1)²`.
- In either case, `Q = isqrt(N)` and `-(2Q+1) <= R <= 2Q`.

Appending digit `d` changes `N` to `4N+d`. The next trial remainder is `4R+d-(4Q+1)` when the old remainder is nonnegative, or `4R+d+(4Q+3)` otherwise. The next root is `2Q + [new R >= 0]`. This is our mathematical derivation and is checked independently against integer square roots, rather than assumed from a library implementation.

With `k=43` root bits, a signed `k+2=45`-bit word holds every final remainder whose sign is inspected. The temporary value `4R+d` can lie outside that signed range. The circuit computes the complete update modulo `2^45`; this remains exact for the final signed result because the invariant proves the final integer lies inside the signed range. No intermediate truncated sign is used to select a branch.

The local protocol, emitted arrays, exhaustive tests and full-source accounting determine whether this implementation helps the pricing target. This is a narrower conclusion than resolving square-root arithmetic in every quantum algorithm or establishing quantum pricing advantage.
