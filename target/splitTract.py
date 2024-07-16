import astropy.io.fits as pf
import numpy as np
import glob, os, sys

fileRoot = "wide/"
filenamePrefix = "target_wide_s23b_"
fitslist = np.sort(glob.glob("%s/%s*-*.fits"%(fileRoot, filenamePrefix)))
overwrite = False


def createFits(data, header, mask, fitsname, overwrite=True):
    cols = []
    for tt, tf in zip(header["TTYPE*"].values(), header["TFORM*"].values()):
        cols.append(pf.Column(name=tt, format=tf, array=data[tt][mask]))
    hdu = pf.BinTableHDU.from_columns(cols)
    hdu.writeto(fitsname, overwrite=overwrite)


def main():

    for ff in fitslist:
        print(ff)

        d = pf.open(ff)[1]
        header = d.header
        data = d.data
        tracts = data["tract"]
        trs = np.unique(tracts)
        for tr in trs:
            fout = "%s/%s%05i.fits"%(fileRoot, filenamePrefix, tr)
            if (os.path.exists(fout)) & (not overwrite):
                print ("     %s : file exists -> skipped"%fout)
            else:
                print ("     ", fout, os.path.exists(fout))
        
                mask = tracts == tr
        
                createFits(data, header, mask, fout, overwrite=overwrite)


if __name__ == "__main__":
    main()
