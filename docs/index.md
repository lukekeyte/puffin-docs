# PUFFIN Documentation

**PUFFIN** (Python Utility For FUV Irradiated disk deNsities) is a parametric framework for efficiently generating density structures of externally irradiated protoplanetary disks with photoevaporative winds.
```{toctree}
:maxdepth: 2
:caption: Contents

quick_start/index
physical_model/index
```

## Key Features

* **Fast generation**: Create 1D/2D density structures in seconds to minutes (vs. weeks/months for hydrodynamical simulations)
* **Validated framework**: Extensively tested against 600+ hydrodynamical simulations
* **Comprehensive parameter coverage**:
  - Stellar masses: 0.3 to 3.0 M☉
  - Disk radii: 20 to 150 au
  - Surface densities: 10¹ to 10⁴ g cm⁻²
  - External FUV fields: 10² to 10⁵ G₀
* **Flexible mass-loss rates**: User-specified values or automatic interpolation from FRIED grid
* **Easy integration**: Output compatible with radiative transfer codes (DALI, RADMC-3D)

## Installation

Install PUFFIN directly from source:
```bash
git clone https://github.com/lukekeyte/PUFFIN.git
cd PUFFIN
pip install -e .
```

## Dependencies

- numpy
- scipy  
- matplotlib

## Quick Links

* [GitHub Repository](https://github.com/lukekeyte/PUFFIN)
* [Paper (Keyte & Haworth 2025)](https://ui.adsabs.harvard.edu/)
* [FRIED Grid](https://ui.adsabs.harvard.edu/abs/2023MNRAS.526.4315H/abstract)

## Citation

If you use PUFFIN in your research, please cite:

Keyte, L. & Haworth, T. J. (2025), "A parametric model for externally irradiated protoplanetary disks with photoevaporative winds", MNRAS (in press)

## Author

Luke Keyte (l.keyte@qmul.ac.uk)  
Astronomy Unit, Queen Mary University of London

## License

This project is licensed under the MIT License.