# PUFFIN: Python Utililty For Fuv Irradiated disk deNsity structures

Puffin is...

## Features

- Initialization of chemical species, reactions, and environmental parameters
- Efficient solving of stiff ODEs representing chemical reactions
- Support for various reaction types including:
  - Gas-phase reactions
  - Grain-surface chemistry
  - Photochemistry
- Integration of self-shielding factors for specific molecules (H2, CO, N2, C)
- Optimization using Numba JIT compilation for performance-critical functions
- Comprehensive logging and progress tracking

## Installation

You can install PUFFIN directly from the source:

```bash
pip install puffin_disk
```

## Dependencies

- numpy
- scipy
- matplotlib
- numba
- tqdm
- pandas

## Model Components

PUFFIN consists of several key components:
- Elements: Handling of chemical elements
- Species: Management of atomic and molecular species
- Gas: Gas phase parameters and properties
- Dust: Dust grain properties and interactions
- Environment: Environmental conditions (UV field, cosmic rays, etc.)
- Reactions: Chemical reaction network and rates
- Parameters: System parameters and constants

## Citation

If you use PUFFIN in your research, please cite:
[Citation information to be added]

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Luke Keyte (l.keyte@qmul.ac.uk)

## Contributing

Contributions are welcome! Please get in touch.
