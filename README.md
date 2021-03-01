Some info about the useful files in my branch: 

Background_chop:
- ignores data values at the ends of the real data files are these are effectively negligible and just noise
- Because no. of data points for MC and real data are not the same, reduced size of real data set by taking averages ( see code for details)
- Need to add functionality to allow making specific cuts
- Needs cross-verification 

chop_v1:
- Made a minor bug fix but other than that this is identical to the one in Dominic's branch 

chop_v2-0-1a:
- Fixed bug when plotting fitting function with Weronika's latest upload (chop_v2-0-1 in Weronika's branch)
- Save function still does not work 
- auto_cuts() not in use 

fit-vmass.cxx
- Uses Prof. Evans's fitting code primarily, with tweaks, to fit A Gaussian to the vmass with chosen cuts
