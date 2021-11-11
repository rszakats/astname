# astname
A small script to get the name/provisional designation or asteroid number of a small Solar System body.

## Motivation
Identifying small Solar System Bodies can be confusing at first because of the numerous IDs that can be used.
This script can help you to get all the available IDs for a known Solar System Body.

## Source of the IDs

Identification is based on NASA JPL/Horizons index file, DASTCOM.IDX.
If it is not present, it will be downloaded from
ftp://ssd.jpl.nasa.gov/pub/xfr/DASTCOM.IDX, also, if it is older than 30 days,
the index file will be re-downloded.

## Scripts

The script is available both in python and in bash.
The python version needs only basic python3 packages, and python3:

* os
* sys
* getpass
* re
* time
* platform
* urllib.request
* shutil

The bash version needs:
* bash
* wget
* GNU Awk
* grep

## Usage

The script accepts integer asteroid number(s) as argument, asteroid name(s) or
NAIFID(s), e.g.:

`python3 astname.py 64 79`

`astname 64 79`

or:

`python3 astname.py Angelina`

`astname Angelina`

or:

`python3 astname.py 2000016`

`astname 2000016`

Use double quotes if special characters are present in the astreoid name, e.g.:

`python3 astname.py "Prokof'ev"`
`astname "Prokof'ev"`

Use double quotes also, when searching for provisional designation e.g.:

`python3 astname.py "1976 YG"`

`astname "1976 YG"`

In extreme cases use backslash to make the input processable by the script,
e.g.:

`python3.8 astname.py "G\!kun\|\|\'homdima"`

Warning: the bash version cannot handle this kind of input right now!

The search is not case sensitive.
Use 

`python3 astname.py --help`

or:

`astname --help`

to print this information.

## How to install

Bash version:

Download the script and make it executable:

`chmod +x astname`

Then move it to your $PATH.

Python version:
If you want to run it directly with your preferred python version, download the script and run it from the directory where you downloaded it:

`python3.9 astname.py`

Or you can use it like the bash version, and make it executable:

`chmod +x astname.py`

And move the file to your $PATH. Then you can run it like this:

`astname.py --help`

## Supported operating systems

Bash version:

Only Linux is supported at the moment.

Python version:

Linux and Windows are supported at the moment.

## Example

Input:

`astname 11 4 "2007 Or10" Psyche`

Output:

```
==========================================================================
IAU Number: 11
Name or Designation:  Parthenope 
NAIFID: 2000011
Alternative designations:  A850 JA, I50J00A
==========================================================================
IAU Number: 4
Name or Designation:  Vesta 
NAIFID: 2000004
Alternative designations:  A807 FA, I07F00A
==========================================================================
IAU Number: 225088
Name or Designation:  Gonggong 
NAIFID: 2225088
Alternative designations:  2007 OR10, 3443951, K07O10R
==========================================================================
IAU Number: 16
Name or Designation:  Psyche 
NAIFID: 2000016
Alternative designations:  A852 FA, I52F00A
==========================================================================
```
## Credits
@author: R. Szakáts, [Konkoly Observatory](https://konkoly.hu/index_en.shtml), ELKH, 2021
