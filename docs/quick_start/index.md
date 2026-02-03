## Quick Start

### 1D Model

```python
import puffin_disk

# Example input values
m_star    = 1.0       # M_sun
r_d       = 100       # AU
sigma_1au = 1000      # g cm^-2
F_FUV     = 1e5       # G_0

# Run PUFFIN
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV)                                        
```

The model returns 1D arrays for radius and density. These can then be plotted:

```python
import matplotlib.pyplot as plt

r_array   = model[0]
rho_array = model[1]

plt.loglog(r_array, rho_array)
plt.show()                                       
```


### 2D Model

```python
import puffin_disk

# Example input values
m_star    = 1.0       # M_sun
r_d       = 100       # AU
sigma_1au = 1000      # g cm^-2
F_FUV     = 1e5       # G_0

# Run PUFFIN
model = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, FFUV_G0)                                        
```

The model returns 1D arrays for radius and height, and a 2D density array. These can then be plotted:

```python
import matplotlib.pyplot as plt

r_array   = model[0]
z_array   = model[1]
rho_array = model[2]

plt.contourf(r_array, z_array, np.log10(rho_array), cmap='Spectral_r', levels=np.arange(-20, -11, 0.2), extend='both')
plt.show()                                       
```
