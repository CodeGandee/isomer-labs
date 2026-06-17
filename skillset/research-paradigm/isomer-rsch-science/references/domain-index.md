# Domain Index

Use this local index for domain routing. It intentionally summarizes the large source package-card catalog instead of importing every generated card.

## Domain Families

| Domain | Common Package Examples | Typical Checks |
| --- | --- | --- |
| Astronomy and astrophysics | Astropy, Astroquery, Lightkurve, Photutils, yt | Python import, data access, FITS or table schema, unit consistency |
| Bioinformatics and single-cell | Biopython, Scanpy, AnnData, scvi-tools, Snakemake, Nextflow | import or CLI, input format, reference data, count matrices, workflow dry run |
| Computational chemistry and molecular dynamics | PySCF, Psi4, OpenMM, GROMACS, CP2K, NWChem, xTB | executable or import, version, force field or basis availability, small molecule smoke test |
| Materials science and electronic structure | ABINIT, Quantum ESPRESSO, LAMMPS, phonopy, spglib, JDFTx | executable, MPI or module state, input parser, small cell or phonon smoke test |
| Computational fluid dynamics and finite elements | OpenFOAM, SU2, MFEM, deal.II, FEniCS or DOLFINx, MOOSE | executable or build, mesh/input availability, small case run, residual checks |
| Electromagnetics and plasma | Meep, openEMS, WarpX, Smilei, gprMax | executable or import, GPU/MPI backend, small domain smoke test, field output schema |
| High-energy physics | Geant4, ROOT, Uproot, pyhf, Awkward, coffea | executable or import, data format, detector or histogram schema, event-count checks |
| Quantum information | Qiskit, Cirq, PennyLane, QuTiP, Quimb, NetKet | import, backend availability, simulator smoke test, seed and circuit reproducibility |
| Robotics and physics simulation | MuJoCo, Drake, Bullet, Gazebo, DART | executable/import, renderer or headless mode, model file availability, deterministic toy simulation |
| Workflow and provenance | AiiDA, Snakemake, Nextflow, jobflow, atomate2 | CLI or import, profile/config availability, dry run, provenance database state |

## Routing Rules

- Use domain examples only to choose what to inspect next.
- Verify the actual package, executable, module, license, data, and backend before computed work.
- If a package is outside this index, classify by required evidence: environment check, computation, analysis, sweep, validation, and claim discipline still apply.
- If package-specific knowledge is essential, record the need as a deferred package-card lookup or ask for an approved resource import.
