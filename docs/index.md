# PUFFIN

**<u>P</u>ython <u>U</u>tility <u>F</u>or <u>F</u>UV <u>I</u>rradiated disk de<u>N</u>sity structures**

`PUFFIN` is a parametric framework for efficiently generating density structures of externally irradiated protoplanetary disks with photoevaporative winds. It provides a computationally efficient alternative to full radiation-hydrodynamic simulations, which can be used as inputs to chemical models, enabling systematic exploration of disk-wind chemistry across wide parameter ranges.

## Installation

`PUFFIN` is a standalone Python script. Simply clone or download the repository:
```bash
git clone https://github.com/yourusername/puffin.git
cd puffin
```
**Repository structure:**
```
puffin/
├── FRIEDV2_ALL_fPAH1p0_growth.dat   # FRIED grid lookup table
├── helpers.py                       # Helper functions
└── puffin.py                        # Main code (1D and 2D models)
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
* **Easy integration**: Output compatible with chemicall modelling and radiative transfer codes (eg. DALI, RADMC-3D)

## Dependencies

- matplotlib
- numpy
- scipy  

## Author

**Luke Keyte**  
Postdoctoral Researcher  
Queen Mary University of London  
l.keyte@qmul.ac.uk

## License

This project is licensed under the MIT License.

```{toctree}
:maxdepth: 2
:caption: Contents

quick_start/index
physical_model/index
```