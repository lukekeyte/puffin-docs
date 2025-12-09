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

Install `PUFFIN` directly from source:

```bash
git clone https://github.com/lukekeyte/PUFFIN.git
cd PUFFIN
pip install -e .
```

## Dependencies

- numpy
- scipy
- matplotlib

## Documentation

Comprehensive documentation, tutorials, and example notebooks are available at:
**[puffin-disk.readthedocs.io](https://puffin-disk.readthedocs.io)**


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

## Version History

### v1.0.0 (2025)
- Initial release
- 1D and 2D parametric models
- FRIED grid interpolation
- Comprehensive validation against hydrodynamical simulations