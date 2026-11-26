# Fair best-response dynamics for Leontief donations

[![Repository verification](https://github.com/DannyExperiments/fair-leontief-donation-dynamics/actions/workflows/verify.yml/badge.svg?branch=main)](https://github.com/DannyExperiments/fair-leontief-donation-dynamics/actions/workflows/verify.yml) [![Verifier replay](https://github.com/DannyExperiments/fair-leontief-donation-dynamics/actions/workflows/replay.yml/badge.svg?branch=main)](https://github.com/DannyExperiments/fair-leontief-donation-dynamics/actions/workflows/replay.yml) [![PDF build](https://github.com/DannyExperiments/fair-leontief-donation-dynamics/actions/workflows/pdf.yml/badge.svg?branch=main)](https://github.com/DannyExperiments/fair-leontief-donation-dynamics/actions/workflows/pdf.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24564949.svg)](https://doi.org/10.5281/zenodo.24564949)

Must the aggregate allocation converge when every donor moves infinitely often, even if the waiting times have no uniform bound? The original question appears in [Greger, dissertation, Open Problem 5, p. 99](https://mediatum.ub.tum.de/doc/1759811/onlts4hzyc7oqggwzeixzb01l.Matthias%20S.%20Greger.pdf#page=115).

**Result.** For finite Leontief donor coordination with positive budgets, nonempty supports and arbitrary nonnegative weights, the aggregate under best responses from zero converges to the unique Nash-welfare allocation for every fair schedule.

[Read the paper (PDF)](paper/manuscript.pdf) · [LaTeX source](paper/manuscript.tex) · [Proof guide](proof/PROBLEM_AND_PROOF.md) · [Reproduce the checks](REPRODUCIBILITY.md)

Equal potential on a slice fixes the aggregate. Holding the outside donor’s block fixed as well then determines the exact gain at the first outside update.

Internally reviewed, not peer reviewed. [Mathematical audit](audits/public_safe_reports/MATHEMATICAL_AUDIT.md) · [Literature and priority](audits/public_safe_reports/LITERATURE_AUDIT.md) · [Citation](CITATION.cff)
