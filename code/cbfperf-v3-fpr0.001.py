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
        retrmedian = int(tmp[26]) - int(tmp[31])
        retrmin = int(tmp[29]) - int(tmp[34])
        retrmax = int(tmp[30]) - int(tmp[35])
        data[rnd] = {
            "retrmedian": retrmedian,
            "retrmin": retrmin,
            "retrmax": retrmax,
        }
        for val in [retrmedian, retrmin, retrmax]:
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
        "len_compressed": str(int(round((n[1] + 10) * 0.52)))
    }

pool.close()
pool.join()

print ""
# print "Calculating serialized VICBF size..."
# pbar = ProgressBar()
# for i in pbar([val for val in sorted(results.keys()) if val <= 11000000]):
#     n = to_vicbf([i, results[i]["hash_functions"], results[i]["slots"]])
#     results[i]["len_uncompressed"] = str(n[0])
#     results[i]["len_compressed"] = str(n[1])

with open("vicbf-scaling-fpr0.001-retronly.csv", "w") as fo:
    fo.write("round " +
             "r_med_hf r_med_slots r_med_prob r_med_lu r_med_lc " +
             "r_min_hf r_min_slots r_min_prob r_min_lu r_min_lc " +
             "r_max_hf r_max_slots r_max_prob r_max_lu r_max_lc\n")
    for rnd in sorted(data.keys()):
        r_med = data[rnd]["retrmedian"]
        r_min = data[rnd]["retrmin"]
        r_max = data[rnd]["retrmax"]
        fo.write(str(rnd) + " " +
                 results[r_med]["hash_functions"] + " " + results[r_med]["slots"] + " " + results[r_med]["probability"] + " " + results[r_med]["len_uncompressed"] + " " + results[r_med]["len_compressed"] + " " +
                 results[r_min]["hash_functions"] + " " + results[r_min]["slots"] + " " + results[r_min]["probability"] + " " + results[r_min]["len_uncompressed"] + " " + results[r_min]["len_compressed"] + " " +
                 results[r_max]["hash_functions"] + " " + results[r_max]["slots"] + " " + results[r_max]["probability"] + " " + results[r_max]["len_uncompressed"] + " " + results[r_max]["len_compressed"] + "\n")
