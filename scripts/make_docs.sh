rm -rf docs/_autosummary
mkdir docs/_static
make -C docs clean
make -C docs html
