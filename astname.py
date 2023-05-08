#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A small script to get the name/provisional designation or asteroid number of
a small solar system body. Identification is based on NASA JPL/Horizons
index file, DASTCOM.IDX.
If it is not present, it will be downloaded from
ftp://ssd.jpl.nasa.gov/pub/xfr/DASTCOM.IDX, also, if it is older than 30 days,
the index file will be re-downloded.

The script accepts integer asteroid number(s) as argument, or asteroid
name(s), e.g.:
python3 astname.py 64 79
or:
python3 astname.py Angelina
Use double quotes if special characters are present in the astreoid name, e.g.:
python3 astname.py "Prokof'ev"
Use double quotes also, when searching for provisional designation e.g.:
python3 astname.py "1976 YG"
In extreme cases use backslash to make the input processable by the script,
e.g.:
python3.8 astname.py "G\!kun\|\|\'homdima"

The search is not case sensitive.
Use python3 astname.py --help to print this information.

@author: R. Szakáts, Konkoly Observatory, ELKH, 2021
Created on Wed Nov 10 09:23:47 2021
"""

import getpass
import os
import platform
import re
import shutil
import sys
import time
import urllib.request


def get_indexfile(url, path):
    """
    Downloads the NASA JPL/Horizons index file, DASTCOM.IDX and saves it to
    the path.

    Parameters
    ----------
    url : str
        Url of the index file.
    path : str
        Full path with filename for the output file.

    Returns
    -------
    None.

    """
    if os.path.exists(path):
        shutil.move(path, path+".old")
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response, \
             open(path, 'wb') as outfile:
            data = response.read()
            outfile.write(data)
    except urllib.error.URLError as e:
        print(e)
        print("Download failed!")
        if os.path.exists(path+".old"):
            shutil.move(path+".old", path)
            print("Using old index file...")
        else:
            sys.exit()


def print_help():
    """
    Returns the helpt text.
    """
    print("Usage:\nThe script accepts integer asteroid number(s) as argument,"
          " or asteroid "
          "name(s), e.g.:\n"
          "python3 astname.py 64\n"
          "or:\n"
          "python3 astname.py 64 79\n"
          "or:\n"
          "python3 astname.py Angelina\n"
          "Use double quotes, if special characters are present in the"
          "astreroid name, e.g.:\n"
          "python3 astname.py ""\"Prokof\'ev\"\n"
          "Use double quotes also, when searching for provisional"
          "designation e.g.:\n"
          "python3 astname.py \"1976 YG\"\n"
          "In extreme cases use backslash to make the input processable by \n"
          "the script, e.g.:\n"
          "python3 astname.py \"G\!kun\|\|\'homdima\"\n"
          "The search is not case sensitive.\n")


def nomatch(t):
    """
    Prints a message when there is no match for the input.

    Parameters
    ----------
    t : str
        The search string.

    Returns a no match string.
    """
    print(f"---------------------------\n"
          f"No match for {t}!\n"
          f"---------------------------\n")


def format_output(t, line):
    """
    If there is a match returns a formatted info block containing the Number,
    Name or Designation, NAIFID and other designations of the object.

    Parameters
    ----------
    t : string
        The search string.
    line : string
        The input line from DASTCOM.IDX.

    Returns
    -------
    str
        A formatted output.

    """
    for lin in line:
        des = str(lin.split(',')[0]).split()
        if len(des) > 2:
            des = des[1] + " " + des[2]
        else:
            des = des[1]
        alt = ""
        for i in range(2, 8):
            try:
                alt += str(lin.split(',')[i])+", "
            except IndexError:
                alt = alt
        alt = alt.replace(", ,", "")
        alt = alt.rstrip(" ,\n")
        print(  f"Object found for {t}!\n"
                f"---------------------------\n"
                f"Number: {str(lin.split(',')[0]).split()[0]}\n"
                f"Name/Designation: {des}\n"
                f"NAIFID: {str(lin).split(',')[1]}\n"
                f"Alternative designations: {alt}\n"
                f"---------------------------\n")
    if len(line) > 0:
        return True


def process_number(t, infile):
    """
    If input is an integer it will search for an asteroid number.

    Parameters
    ----------
    t : str
        Input string.
    infile : str
        Full path and name of the input index file.

    Returns
    -------
    str
        A fromatted output.

    """
    with open(infile, "r") as file:
        for line in file:
            if int(t) >= 50000000:
                if re.search(str(str(t)+" "), line):
                    return (format_output(t, [str(line)]))

            else:
                if re.search(str(" "+str(t)+" "+"[0-9A-Za-z]"), line):
                    return (format_output(t, [str(line)]))


def process_name(t, infile):
    """
    If input is a string it will search for an asteroid name or designation.

    Parameters
    ----------
    t : str
        Input string.
    infile : str
        Full path and name of the input index file.

    Returns
    -------
    str
        A fromatted output.

    """
    with open(infile, "r") as file:
        lines = []
        for line in file:
            if str(t).lower() in line.lower():
                lines.append(str(line))
        if len(lines) > 0:
            return (format_output(t, lines))


def process_naifid(t, infile):
    """
    If input is a NAIFID it will search for a NAIFID.

    Parameters
    ----------
    t : str
        Input string.
    infile : str
        Full path and name of the input index file.

    Returns
    -------
    str
        A fromatted output.

    """
    with open(infile, "r") as file:
        for line in file:
            if re.search(","+str(t)+",", line):
                return (format_output(t, [str(line)]))


def main():
    # Where to store the index file.
    if platform.system() == 'Linux':
        cachedir = '/home/'+str(getpass.getuser())+'/.cache/'
    elif platform.system() == 'Windows':
        cachedir = "c:\\Users\\"+str(getpass.getuser())+"\\.cache\\"
    if os.path.exists(cachedir) is False:
        os.mkdir(cachedir)
    datafile = 'DASTCOM.IDX'
    url = 'ftp://ssd.jpl.nasa.gov/pub/xfr/DASTCOM.IDX'
    infile = cachedir+datafile
    # If the index file is missing, the script will try to download it.
    if os.path.exists(cachedir+datafile) is False:
        print("No index file was found! Downloading...")
        get_indexfile(url, cachedir+datafile)
    else:
        # If the file is older than 30 days, it will be re-downloaded.
        ctime = os.path.getmtime(cachedir+datafile)
        if ((time.time()-ctime)/60./60./24.) > 30.:
            print(f"Index file {datafile} is older than 30 days! "
                  f"Downloading...")
            get_indexfile(url, cachedir+datafile)
    if len(sys.argv) == 1:
        print_help()
    # Printing help message.
    elif str(sys.argv[1]) == '--help':
        print_help()
    else:
        for i, targ in enumerate(sys.argv[1:]):
            # Check if the input is integer or string without a dot (float)
            if "." in targ:
                print(f"The {i+1}. argument ({targ}) is wrong! Plese see the "
                      f"usage below!")
                print_help()
                sys.exit()
            else:
                try:
                    targ = int(targ)
                    if isinstance(targ, int):
                        if int(targ) > 2000000 and int(targ) < 50000000:
                            result = process_naifid(targ, infile)
                            if result != True:
                                nomatch(targ)
                        else:
                            result = process_number(targ, infile)
                            if result != True:
                                nomatch(targ)
                except ValueError:
                    if isinstance(targ, str):
                        result = process_name(targ, infile)
                        if result != True:
                            nomatch(targ)


if __name__ == "__main__":
    main()
