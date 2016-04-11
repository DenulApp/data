This folder contains the scripts used to derive the expected size of the VI-CBF from the raw data. As you can probably tell, they were hacked together quickly and were not written for readability. I'm sorry for what reading them will probably do to your eyes. Also, this description is going to assume that you have read the evaluation section of my thesis.

Anyway. As you can see, there are nine scripts in this folder, named after the following scheme:

    cbfperf{,-v2,-v3}-fpr0.{1,01,001}.py

The scripts all work generally the same way and only differ in a few lines. 

* The `fpr0.{1,01,001}` indicates which target FPR they are trying to achieve. 
* The scripts simply named `cbfperf-fpr...` calculate the size of the bloom filter using protocol 1
* The `cbfperf-v2-fpr...` scripts calculate protocol 2
* The `cbfperf-v3-fpr...` scripts calculate a hypothetical case without any orphans

That's about all there is to it.

Used libraries:

* [Scipy](https://github.com/scipy/scipy) (licensed BSD)
* [Progressbar](https://github.com/niltonvolpato/python-progressbar) (licensed LGPL / BSD)
* [pyVICBF](https://github.com/malexmave/pyVICBF) (licensed Apache v2)
