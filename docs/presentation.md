## Presentation

> Note: this documentation is being written. French transalation needed

TAXIPP is the new version of Institut des Politiques Publique's microsimulation software, coded in Python.
IPP-Macro-Series-Parser is a collection of scripts to parse raw data (demographics, national accounts, ...) to build data files needed to calibrate the survey data.

## Installation

Clone the ipp-macro-series-parser Git repository on your machine and install the Python package.
Assuming you are in your working directory:

```
git clone https://github.com/taxipp/ipp-macro-series-parser
cd ipp-macro-series-parser
pip install -e .
```

Rename config.ini as config_local.ini, replacing None by the path to the folder in which you wish to store the data which will be downloaded.
For example, the data downloaded with comptes_nationaux will be stored in a folder of your choice, which you should have indicated in cn_directory.

##  Data
