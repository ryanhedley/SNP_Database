# SNP_Database

This is currently just a 'proof of concept'. It uploads genotyping data from Illumina GTC files into a SQLite database. The data can then be access via a Flask frontend.

### Requirements:

- GTC files (Illumina)
- BPM file (Illumina) corresponding to GTC files

### Dependencies:

- The "module" folder from Illumina's [BeadArrayFiles](https://github.com/Illumina/BeadArrayFiles) repository
- sqlite3
- flask
- easygui
- logging
