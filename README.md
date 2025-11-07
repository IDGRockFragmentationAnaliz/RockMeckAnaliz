# RockMeckAnaliz

```
pip install numpy
pip install pandas
pip install matplotlib
pip install pyvista[all] # библиотека 3д геометрии и отображения
pip install pyproj # библиотека георграфических проэкций
pip install scikit-spatial
```

$\phi$ - strike

$\delta$ - dip

$\lambda$ - rake

$$
\mathbf{n} = (\sin(\text{dip}) \sin(\text{strike}), -\sin(\text{dip}) \cos(\text{strike}), \cos(\text{dip}))
$$

$$
n_{x_i} (x - x_i) + n_{y_i} (y- y_i) + n_{h_i} (h - h_i) = 0
$$

Уравнение прямой в сечении $H$

$$
n_{x_i} (x - x_i) + n_{y_i} (y- y_i) + n_{h_i} (H - h_i) = 0
$$

Уравнение сферы радиуса $r$

$$
(x - x_i)^2+(y-y_i)^2+(h-h_i)^2=r_i^2
$$

Уравнение окружности в сечении $H$

$$
(x - x_i)^2+(y-y_i)^2=r_i^2-(H-h_i)^2
$$


The local coordinate system has its origin at
latitude $35.867^\circ N$, longitude $120.447^\circ W$ and is oriented $N42^\circ W$