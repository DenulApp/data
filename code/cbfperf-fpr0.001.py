from scipy.special import binom
from multiprocessing import Pool
from vicbf.vicbf import VICBF
from progressbar import ProgressBar
import zlib


def calculate_fpr(n, m, l, k):
    """Calculate the FPR for given parameters."""
    return pow(1.0 - pow(1.0 - 1.0 / m, n * k) - ((l - 1.0) / l) *
               n * k * (1.0 / m) * pow(1.0 - (1.0 / m), n * k - 1.0) -
               (((l - 1.0) * (l + 1)) / (6.0 * pow(l, 2.0))) *
               binom(n * k, 2.0) * pow(1.0 / m, 2.0) *
               pow(1.0 - (1.0 / m), n * k - 2.0),
               k)


def find_params(entries, target=0.001, deviation=0.0001):
    """Determine the more-or-less optimal parameters for the given values."""
    entries = float(entries)
    dlbase = 4.0
    hash_functions = 1
    slots = entries
    last = 0.0
    change_k = False
    while True:
        prob = calculate_fpr(entries, slots, dlbase, hash_functions)
        # print entries, dlbase, hash_functions, slots, prob
        if prob - target > deviation:
            # FPR is still too high, increase parameters
            if last > prob:
                # FPR has decreased since last step
                hash_functions += 1.0
                change_k = True
            else:
                # FPR has increased since last step
                if change_k:
                    hash_functions -= 1.0
                    change_k = False
                    slots += 1
                else:
                    hash_functions += 1.0
                    change_k = True
        elif prob - target < -deviation:
            # FPR is too low, decrease parameters
            slots -= 1
            change_k = False
        else:
            break
        last = prob
    return hash_functions, slots, prob


def to_vicbf(params):
    """Create a VICBF with given parameters and return the serialized sizes."""
    entries = int(float(params[0]))
    hash_functions = int(float(params[1]))
    slots = int(float(params[2]))

    v = VICBF(int(slots), int(hash_functions))
    for k in range(int(entries)):
        v.insert(k)
    serialized = v.serialize().tobytes()
    compressed = zlib.compress(serialized, 6)
    return len(serialized), len(compressed)


data = {}
results = {}
with open("rounds_agg.csv", "r") as rounds:
    print "Reading rounds..."
    for line in rounds:
        if line[0] == 'r' or line[0] == '#':
            continue
        tmp = line.strip().split(" ")
        rnd = int(tmp[0])
        if rnd == 0:
            continue
        noretrmedian = int(tmp[26])
        noretrmin = int(tmp[29])
        noretrmax = int(tmp[30])
        neverretrmedian = int(tmp[31])
        neverretrmin = int(tmp[34])
        neverretrmax = int(tmp[35])
        data[rnd] = {
            "noretrmedian": noretrmedian,
            "noretrmin": noretrmin,
            "noretrmax": noretrmax,
            "neverretrmedian": neverretrmedian,
            "neverretrmin": neverretrmin,
            "neverretrmax": neverretrmax,
        }
        for val in [noretrmedian, noretrmin, noretrmax, neverretrmedian, neverretrmin, neverretrmax]:
            results[val] = {}

print "Calculating VICBF parameters..."
pool = Pool(maxtasksperchild=1)
resiter = pool.imap(find_params, results.keys())
pbar = ProgressBar(maxval=len(results.keys()))
pbar.start()
c = 0
for i in results.keys():
    n = resiter.next()
    c += 1
    pbar.update(c)
    results[i] = {
        "hash_functions": str(n[0]),
        "slots": str(n[1]),
        "probability": str(n[2]),
        "len_uncompressed": str(n[1] + 10),
        "len_compressed": str(int(round((n[1] + 10)* 0.52)))
    }

pool.close()
pool.join()

print ""
#print "Calculating serialized VICBF size..."
#pbar = ProgressBar()
#for i in pbar(results.keys()):
#    n = to_vicbf([i, results[i]["hash_functions"], results[i]["slots"]])
#    results[i]["len_uncompressed"] = str(n[0])
#    results[i]["len_compressed"] = str(n[1])

with open("vicbf-scaling-fpr0.001-proto1.csv", "w") as fo:
    fo.write("round " +
             "nor_med_hf nor_med_slots nor_med_prob nor_med_lu nor_med_lc " +
             "nor_min_hf nor_min_slots nor_min_prob nor_min_lu nor_min_lc " +
             "nor_max_hf nor_max_slots nor_max_prob nor_max_lu nor_max_lc " +
             "nvr_med_hf nvr_med_slots nvr_med_prob nvr_med_lu nvr_med_lc " +
             "nvr_min_hf nvr_min_slots nvr_min_prob nvr_min_lu nvr_min_lc " +
             "nvr_min_hf nvr_min_slots nvr_min_prob nvr_min_lu nvr_min_lc\n")
    for rnd in sorted(data.keys()):
        nor_med = data[rnd]["noretrmedian"]
        nor_min = data[rnd]["noretrmin"]
        nor_max = data[rnd]["noretrmax"]
        nvr_med = data[rnd]["neverretrmedian"]
        nvr_min = data[rnd]["neverretrmin"]
        nvr_max = data[rnd]["neverretrmax"]
        fo.write(str(rnd) + " " +
                 results[nor_med]["hash_functions"] + " " + results[nor_med]["slots"] + " " + results[nor_med]["probability"] + " " + results[nor_med]["len_uncompressed"] + " " + results[nor_med]["len_compressed"] + " " +
                 results[nor_min]["hash_functions"] + " " + results[nor_min]["slots"] + " " + results[nor_min]["probability"] + " " + results[nor_min]["len_uncompressed"] + " " + results[nor_min]["len_compressed"] + " " +
                 results[nor_max]["hash_functions"] + " " + results[nor_max]["slots"] + " " + results[nor_max]["probability"] + " " + results[nor_max]["len_uncompressed"] + " " + results[nor_max]["len_compressed"] + " " +
                 results[nvr_med]["hash_functions"] + " " + results[nvr_med]["slots"] + " " + results[nvr_med]["probability"] + " " + results[nvr_med]["len_uncompressed"] + " " + results[nvr_med]["len_compressed"] + " " +
                 results[nvr_min]["hash_functions"] + " " + results[nvr_min]["slots"] + " " + results[nvr_min]["probability"] + " " + results[nvr_min]["len_uncompressed"] + " " + results[nvr_min]["len_compressed"] + " " +
                 results[nvr_max]["hash_functions"] + " " + results[nvr_max]["slots"] + " " + results[nvr_max]["probability"] + " " + results[nvr_max]["len_uncompressed"] + " " + results[nvr_max]["len_compressed"] + "\n")
