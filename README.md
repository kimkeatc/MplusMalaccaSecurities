# MplusMalaccaSecurities
https://www.mplusonline.com.my/macsecos/index.asp related function.

# Build *.whl file
```
C:\Users\MplusMalaccaSecurities> RMDIR /s /q build dist mplus.egg-info
C:\Users\MplusMalaccaSecurities> python setup.py sdist bdist_wheel
```

# Install package *.whl files under sub-directory, dist
```
C:\Users\MplusMalaccaSecurities> python -m pip install --find-links=.\dist mplus
```

# Uninstall package
```
C:\Users\kimke\Desktop\workspace\MplusMalaccaSecurities>python -m pip uninstall -y mplus
```

# Applications

## Development
```
C:\Users\MplusMalaccaSecurities> python

```

