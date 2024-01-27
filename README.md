# Haplotype-Inference-using-Quantum-Annealers

Haplotype Inference with Pure Parsimony: A Quantum Computing Approach

## Setup

```bat
pip install dwave-system
pip install dwave-neal
pip install ortools==9.5.2237
```

## Run  QUBO formulation 

Each formulation has a main function that allow you to run simulated annealing on problems in `files`.

```bat
python formulationDI.py
python formulationSCP.py
python formulationQHI.py
```

## Create and evaluate dataset

1. Generate haplotype set

```bat
ms.exe 10 20 -s 8 -r 100.0 2501 > HapSet.inp
```

2. Copy `HapSet.inp` to folder `Data`

3. Generate dataset

```bat
python generate-dataset.py
```

4. Run preprocess

```bat
python preprocess-input.py
```

5. Run ILP solver to obtain optimal solutions
```bat
python HI_ILP.py
```
