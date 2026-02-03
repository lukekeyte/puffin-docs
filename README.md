# PUFFIN

**<u>P</u>ython <u>U</u>tility <u>F</u>or <u>F</u>UV <u>I</u>rradiated disk de<u>N</u>sity structures**

`PUFFIN` is a parametric framework for efficiently generating density structures of externally irradiated protoplanetary disks with photoevaporative winds. It provides a computationally efficient alternative to full radiation-hydrodynamic simulations, which can be used as inputs to chemical models, enabling systematic exploration of disk-wind chemistry across wide parameter ranges.

## Installation

Install `PUFFIN` directly from PyPI using pip:

```bash
pip install puffin_disk
```

**Requirements:**
- Python 3.8 or higher
- numpy >= 1.20.0
- scipy >= 1.7.0
- matplotlib >= 3.3.0

**Dependencies:**
- numpy
- scipy
- matplotlib


## Key Features

* **Fast generation**: Create 1D/2D density structures in seconds to minutes (vs. weeks/months for hydrodynamical simulations)
* **Validated framework**: Extensively tested against 600+ hydrodynamical simulations
* **Comprehensive parameter coverage**:
  - Stellar masses: 0.3 to 3.0 M☉
  - Disk radii: 20 to 150 au
  - Surface densities: 10¹ to 10⁴ g cm⁻²
  - External FUV fields: 10² to 10⁵ G₀
* **Flexible mass-loss rates**: User-specified values or automatic interpolation from FRIED grid
* **Easy integration**: Output compatible with chemical modelling and radiative transfer codes (eg. `DALI`, `RADMC-3D`)


## Citation

If you use `PUFFIN` as part of your research, please cite our overview article:

```text
@misc{keyte_haworth_2026,
      title={A parametric model for externally irradiated protoplanetary disks with photoevaporative winds}, 
      author={Luke Keyte and Thomas J. Haworth},
      year={2026},
      eprint={2602.02011},
      archivePrefix={arXiv},
      primaryClass={astro-ph.EP},
      url={https://arxiv.org/abs/2602.02011}, 
}
```


## Author

**Luke Keyte**  
Postdoctoral Researcher  
Queen Mary University of London  
l.keyte@qmul.ac.uk


## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests on GitHub. For major changes, please open an issue first to discuss proposed modifications.

## Support

For questions, bug reports, or feature requests:
- Open an issue on [GitHub](https://github.com/lukekeyte/PUFFIN)
- Email: l.keyte@qmul.ac.uk
- Check the [documentation](https://puffin.readthedocs.io) for detailed guides


## License

This project is licensed under the MIT License.