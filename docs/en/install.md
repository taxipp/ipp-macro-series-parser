# Installation and configuration

> Note: this documentation is being written. French transalation needed

## Installation

Clone the ipp-macro-series-parser Git repository on your machine and install the Python package.
Assuming you are in your working directory:

```
git clone https://github.com/taxipp/ipp-macro-series-parser
cd ipp-macro-series-parser
pip install -e .
```

## Configuration

Rename config.ini as config_local.ini, replacing each None by the path of the folder in which you wish to store the data which will be downloaded or created.
For example, the data downloaded with comptes_nationaux will be stored in a folder of your choice, which you should have indicated in cn_directory.
