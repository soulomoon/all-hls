## Script to install hls from github release
### Idea
Install prebuild all versions of [haskell-language-server](https://github.com/haskell/haskell-language-server) with ease
### Description
Simple script to download hls binaries from github releases
It first download all the files into execute path's cache folder unzip it
then install them to binary folder specified
### Cache
the cache is in execute path `cache` folder
every run would check if the same binary file already
exist in the cache folder. It would only download them from
github not the cache.  
### Run
`python3 some_bin_path`
some_bin_path is where you want to put binary files to.