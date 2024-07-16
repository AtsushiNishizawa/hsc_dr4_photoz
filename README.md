## get target catalog

To obtain the target catalog, first set the user environment as 
```shell
$ HSC_SSP_CAS_USER=username 
$ HSC_SSP_CAS_PASSWORD=password 
$ export HSC_SSP_CAS_USER 
$ export HSC_SSP_CAS_PASSWORD 
```
and then make directory
```shell
$ cd target/
$ mkdir wide 
$ mkdir dud 
```
Finally, it takes ~3 days for query and download the entire data. 
```shell
$ python3 query_wide.py 
$ python3 query_deep.py 
``` 

If you want to split the data tract by tract, run the code
```shell
$ python3 splitTract.py 
```
