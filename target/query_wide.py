#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
# (c) Atsushi J. Nishizawa, 
# Last update : July. 10 2024
#
# This is a python script to download target photometric catalog
# from database for DR4 (S23B) internal release.
#
# you will be asked
# 1) tract list in a text format (e.g. tract_list_wide.txt)
# 2) hscSspQuery3.py
# 3) master query file (target_wide_s23b_master.sql)
#

import numpy as np
import argparse
import hscSspQuery3 as Q
import sys, os
from getpass import getpass


def getPassword(passenv=""):
    password_from_envvar = os.environ.get(passenv, '')
    if password_from_envvar != '':
        return password_from_envvar
    else:
        return getpass('Enter your DB password: ')
    
def getUser(unameenv=""):
    uname_from_envvar = os.environ.get(unameenv, '')
    if uname_from_envvar != '':
        return uname_from_envvar
    else:
        return raw_input('Enter your DB username: ')



if ( __name__ == "__main__" ):

    #
    # set os environment to avoid directly typing username
    #
    unameenv = "HSC_SSP_CAS_USER"
    user = getUser(unameenv=unameenv)

    #
    # set os environment to avoid directly typing password
    #
    passenv = "HSC_SSP_CAS_PASSWORD"
    pw = getPassword(passenv=passenv)

    
    #
    # specify the file including the list of tract (single tract in each row)
    #
    TractListFile = "tract_list_wide.txt"
    tract_list = np.loadtxt(TractListFile, dtype="unicode")
    Ntracts = len(tract_list)
    print ("number of tracts :", Ntracts)

    Nloop = int(Ntracts/10)
    tracts1, tracts2 = [], []
    for i in range(Nloop):
        ist = i*10
        ied = min((i+1)*10-1, Ntracts-1)
        tracts1.append(tract_list[ist])
        tracts2.append(tract_list[ied])
        #print (ist, ied, tract_list[ist], tract_list[ied])
    #sys.exit(-1)

    #
    # specify the sql master file
    # The string "TTRACTT" is replaced by the actual value of tract before the query.
    #
    MasterQueryFile = "target_wide_s23b_master.sql"
    MasterQuery = open(MasterQueryFile).read()

    #
    # specify the data release version
    # 
    DR   = 'dr4'


    #
    # The query will not overwrite the existing fits files.
    # If you want to update your query, first remove the fits file
    # which is obtained by the previous queries, or just turn on
    # the overwrite flag.
    #
    foverwrite = False
    tract_list = tract_list[::-1] # to be removed 
    for tract1, tract2 in zip(tracts1, tracts2):

        OutFileName = "wide/target_wide_s23b_%05i-%05i.fits"%(int(tract1), int(tract2))
        print (OutFileName)

        if ( (os.path.exists(OutFileName)) and (os.path.getsize(OutFileName)!=0) and (not foverwrite) ):
            print (OutFileName, "exists (skipped)")
            continue

        Query = MasterQuery.replace("TTRACTT1", str(tract1)).replace("TTRACTT2", str(tract2))
 
        #"""
        Q.query(
            user=user,
            release_version=DR,
            delete_job=True,
            form='fits',
            nomail=True,
            preview=False,
            skip_syncheck=False,
            api_url='https://hscdata.mtk.nao.ac.jp/datasearch/api/catalog_jobs/',
            outputfile=OutFileName,
            pw=pw,
            sql=Query
            )
        #"""
