# Conda Recipe for basespace-commons

## Pre-requisites

This requires `conda-build` to be installed:

```
conda install -y -q conda-build
```

## Installation

To install locally and use your local channel:

```
conda-build .
conda install -y basespace-commons --use-local
conda config --add channels local
```
