# PUFFIN: Python Utility For FUV Irradiated disk deNsities

`PUFFIN` is a parametric framework for efficiently generating density structures of externally irradiated protoplanetary disks with photoevaporative winds. It provides a computationally efficient alternative to full radiation-hydrodynamic simulations, which can be used as inputs to chemical models, enabling systematic exploration of disk-wind chemistry across wide parameter ranges.

## Features

- **Fast generation**: Create full 1D or 2D density structures in seconds to minutes (vs. weeks/months for hydrodynamical simulations)
- **Validated framework**: Extensively tested against the FRIED grid of hydrodynamical simulations
- **Comprehensive parameter coverage**:
  - Stellar masses: 0.3 to 3.0 M☉
  - Disk radii: 20 to 150 au
  - Surface densities: 10¹ to 10⁴ g cm⁻²
  - External FUV fields: 10² to 10⁵ G₀
- **Flexible mass-loss rates**: User-specified values or automatic interpolation from FRIED grid
- **Physically motivated structure**: 
  - Disk interior with hydrostatic equilibrium
  - Smooth disk-wind transition region
  - Spherically diverging photoevaporative wind
- **Easy integration**: Output compatible with radiative transfer and chemical modeling codes

## Installation

Install PUFFIN directly from PyPI:

```bash
pip install puffin_disk
```

Or install from source:

```bash
git clone https://github.com/lukekeyte/PUFFIN.git
cd PUFFIN
pip install -e .
```

## Dependencies

- numpy
- scipy
- matplotlib

## Quick Start

```python
from puffin import DiskModel

# Create a disk model with specified parameters
model = DiskModel(
    stellar_mass=1.0,      # Solar masses
    disk_radius=100,       # au
    surface_density=1000,  # g cm^-2 at 1 au
    fuv_field=1000        # G0
)

# Generate 2D density structure
model.run_2d()

# Access density grid
density = model.density_2d
r_grid = model.r_grid
z_grid = model.z_grid

# Visualize the structure
model.plot_density()
```

## Key Applications

PUFFIN is designed for:

1. **Chemical modeling**: Generate realistic disk-wind density structures as inputs for thermochemical codes
2. **Parameter surveys**: Systematically explore how stellar mass, disk properties, and external FUV affect disk structure
3. **Observational predictions**: Model molecular line emission and develop diagnostics for spatially unresolved observations
4. **Planet formation studies**: Investigate volatile budgets and snowline locations in irradiated environments

## Model Components

### 1D Model
- Power-law disk interior with exponential taper
- Smooth transition region ("plateau")
- Spherically diverging wind from disk outer edge
- Calibrated taper steepness scaling with stellar mass, disk radius, and FUV field

### 2D Model
- Hydrostatic equilibrium with external FUV heating
- Extended "halo" transition region from disk surface
- Spherically diverging wind from focal point (~0.5 r_d)
- Realistic vertical temperature structure
- Wind suppression in gravitationally bound inner regions

## Validated Parameter Range

The model has been tested across:
- 320 unique parameter combinations
- 600+ 1D FRIED models
- Representative 2D hydrodynamical simulations
- Typical accuracy: factor of ~2 agreement with full simulations

## Important Notes

- The model focuses on FUV-driven external photoevaporation
- Temperature and radiation fields from model construction should **not** be used directly for chemistry
- Always use dedicated radiative transfer codes (e.g., DALI, RADMC-3D) with PUFFIN density structures
- Best suited for FUV fields 10² - 10⁵ G₀; extrapolation beyond validated ranges should be done cautiously
- Model does not include:
  - External EUV radiation
  - Internal photoevaporation from the central star
  - Magnetic fields or non-thermal processes

## Model Limitations

PUFFIN may produce unphysical structures under these conditions:

1. **Optically thin disks**: Surface densities below ~10 g cm⁻² at 1 au may cause issues with defining the disk surface
2. **Excessive halo mass**: In ~2% of cases, the transition region may become too massive (automatically flagged)
3. **Mass-loss rate inconsistencies**: Wind densities exceeding disk surface densities (automatically corrected)

The package includes validation utilities that check for these edge cases and warn when parameters fall outside validated ranges.

## Documentation

Comprehensive documentation, tutorials, and example notebooks are available at:
**[puffin-disk.readthedocs.io](https://puffin-disk.readthedocs.io)**

## Example Use Cases

### Generate a simple 1D model
```python
from puffin import DiskModel1D

model = DiskModel1D(
    stellar_mass=0.6,
    disk_radius=40,
    surface_density=1000,
    fuv_field=1000
)

model.run()
r, density = model.get_profile()
```

### Use with FRIED mass-loss rate interpolation
```python
from puffin import DiskModel

model = DiskModel(
    stellar_mass=1.0,
    disk_radius=100,
    surface_density=1000,
    fuv_field=5000,
    use_fried_mdot=True  # Automatically interpolate mass-loss rate
)

model.run_2d()
```

### Export for use with DALI
```python
import numpy as np
from puffin import DiskModel

model = DiskModel(stellar_mass=1.0, disk_radius=100, 
                  surface_density=1000, fuv_field=1000)
model.run_2d()

# Export density structure
np.save('density_grid.npy', model.density_2d)
np.save('r_grid.npy', model.r_grid)
np.save('z_grid.npy', model.z_grid)

# Use these grids as input to DALI or other radiative transfer codes
```

## Citation

If you use PUFFIN in your research, please cite:

Keyte, L. & Haworth, T. J. (2025), "A parametric model for externally irradiated protoplanetary disks with photoevaporative winds", MNRAS, 000, 1-21

```bibtex
@article{keyte2025puffin,
    author = {Keyte, Luke and Haworth, Thomas J.},
    title = {A parametric model for externally irradiated protoplanetary disks with photoevaporative winds},
    journal = {MNRAS},
    year = {2025},
    volume = {000},
    pages = {1-21}
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Luke Keyte (l.keyte@qmul.ac.uk)  
Astronomy Unit, Queen Mary University of London

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests on GitHub. For major changes, please open an issue first to discuss proposed modifications.

## Support

For questions, bug reports, or feature requests:
- Open an issue on [GitHub](https://github.com/lukekeyte/PUFFIN)
- Email: l.keyte@qmul.ac.uk
- Check the [documentation](https://puffin-disk.readthedocs.io) for detailed guides

## Acknowledgments

PUFFIN builds upon the FRIED grid of hydrodynamical simulations (Haworth et al. 2018, 2023). Development was supported by UKRI guaranteed funding for a Horizon Europe ERC consolidator grant (EP/Y024710/1).

## Related Projects

- **SIMBA**: Astrophysical chemical network solver for modeling chemistry in the density structures generated by PUFFIN
- **FRIED**: Grid of radiation-hydrodynamic simulations of externally irradiated disks (Haworth et al. 2018, 2023)
- **DALI**: 1+1D thermochemical code for protoplanetary disks (Bruderer et al. 2012)

## Version History

### v1.0.0 (2025)
- Initial release
- 1D and 2D parametric models
- FRIED grid interpolation
- Comprehensive validation against hydrodynamical simulations
```