"""Python script to create GnuPlot plots."""

from subprocess import Popen, PIPE

# A few constants shared across all plots
FONTSIZE = "15"
TERMINAL = "postscript eps color solid"
LINEWIDTH = "3"
OUTPUT_PREFIX = "output/"
# The following is the template all GnuPlot script files share. It contains
# placeholders for a number of values:
# 0. Terminal type (filled from variable TERMINAL)
# 1. Output file
# 2. Title
# 3. Font size for all fonts (filled from FONTSIZE)
# 4. Label for X-Axis
# 5. Label for Y-Axis
# The template will be dynamically extended with the plot commands and other
# options (like logscale etc) required to create the desired plots.
TEMPLATE = """#!/usr/bin/gnuplot
set terminal {0}
set output '{1}'
set title "{2}" font ",{3}"
set xlabel "{4}" font ",{3}"
set ylabel "{5}" font ",{3}"
set xtics font ",{3}"
set ytics font ",{3}"
set key font ",{3}" spacing 1.5
"""

TARGET = [
    {  # Graph to display the distribution of share steps
        "output": "impl-simu-share-time.eps",
        "xlabel": "Step",
        "ylabel": "Fraction of Users",
        "title": "Share Distribution over Time",
        "options":
            [
                "set xrange[0:10]"
            ],
        "plot":
            [
                {
                    "input": "share-step-distribution.csv",
                    "x": "1",
                    "y": "2",
                    "title": "p(n)",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                }
            ]
    },  # End Share Step Distribution Graph
    {  # Graph to display degree distribution of a scale-free network
        "output": "impl-simu-scale-free.eps",
        "xlabel": "Degree",
        "ylabel": "Number of Users",
        "title": "Degree Distribution of a Scale-Free Network",
        "options":
            [
                "set logscale xy",
                "set xrange[1:1000]"
            ],
        "plot":
            [
                {
                    "input": "u100000/user-distribution.csv",
                    "x": "2",
                    "y": "3",
                    "title": "u = 100 000 Users",
                    "type": "lines",
                    "filter":
                        {
                            "column": "1",
                            "value": "0"
                        },
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                }
            ]
    },  # End of degree distribution of a scale-free network plot
    {  # Graph to display how the degree distribution evolves over rounds
        "output": "impl-simu-user-development.eps",
        "xlabel": "Degree",
        "ylabel": "Number of Users",
        "title": "Median Degree Distribution over Time (100k initial Users)",
        "options":
            [
                "set logscale xy",
                "set xrange[1:1000]"
            ],
        "plot":
            [
                {
                    "input": "u100000/user-distribution.csv",
                    "x": "2",
                    "y": "3",
                    "title": "Step 0",
                    "type": "lines",
                    "filter":
                        {
                            "column": "1",
                            "value": "0"
                        },
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                },
                {
                    "input": "u100000/user-distribution.csv",
                    "x": "2",
                    "y": "3",
                    "title": "Step 50",
                    "type": "lines",
                    "filter":
                        {
                            "column": "1",
                            "value": "50"
                        },
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                },
                {
                    "input": "u100000/user-distribution.csv",
                    "x": "2",
                    "y": "3",
                    "title": "Step 100",
                    "type": "lines",
                    "filter":
                        {
                            "column": "1",
                            "value": "100"
                        },
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                },
                {
                    "input": "u100000/user-distribution.csv",
                    "x": "2",
                    "y": "3",
                    "title": "Step 150",
                    "type": "lines",
                    "filter":
                        {
                            "column": "1",
                            "value": "150"
                        },
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                },
                {
                    "input": "u100000/user-distribution.csv",
                    "x": "2",
                    "y": "3",
                    "title": "Step 200",
                    "type": "lines",
                    "filter":
                        {
                            "column": "1",
                            "value": "200"
                        },
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                }
            ]
    },  # End of degree distribution over time plot
    {  # Graph to display the VICBF scaling
        "output": "eval-simu-vicbf-scaling.eps",
        "xlabel": "Step",
        "ylabel": "Size (MB)",
        "title": "Median Size of Serialized VI-CBF over Time (100k initial Users, Orphans only)",
        "options":
            [
                "set encoding iso_8859_1",
                "set termoption dash",
                "set key top left",
                "set for [i=1:5] linetype i lt i",
                'set style line 1 lt 6 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 2 lt 1 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 3 lt 6 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 4 lt 1 lc rgb "blue" lw ' + LINEWIDTH,
            ],
        "plot":
            [
                {
                    "input": "u100000/vicbf-scaling-fpr0.01-proto1.csv",
                    "x": "1",
                    "y": "($20 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.01 \261 0.0001, Protocol 1)",
                    "type": "lines",
                    "options":
                        [
                            "ls 1",
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.01-proto2.csv",
                    "x": "1",
                    "y": "($20 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.01 \261 0.0001, Protocol 2)",
                    "type": "lines",
                    "options":
                        [
                            "ls 3"
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.01-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001, Protocol 1)",
                    "type": "lines",
                    "options":
                        [
                            "ls 2",
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.01-proto2.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001, Protocol 2)",
                    "type": "lines",
                    "options":
                        [
                            "ls 4"
                        ]
                }
            ]
    },  # End of VICBF scaling graph
    {  # Graph to display the VICBF scaling for 1000 users
        "output": "eval-simu-vicbf-scaling-u1000.eps",
        "xlabel": "Step",
        "ylabel": "Size (MB)",
        "title": "Median Size of Serialized VI-CBF over Time (1k initial Users, Orphans only)",
        "options":
            [
                "set encoding iso_8859_1",
                "set termoption dash",
                "set key top left",
                "set for [i=1:5] linetype i lt i",
                'set style line 1 lt 6 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 2 lt 1 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 3 lt 6 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 4 lt 1 lc rgb "blue" lw ' + LINEWIDTH,
            ],
        "plot":
            [
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-proto1.csv",
                    "x": "1",
                    "y": "($20 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.01 \261 0.0001, Protocol 1)",
                    "type": "lines",
                    "options":
                        [
                            "ls 1",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-proto2.csv",
                    "x": "1",
                    "y": "($20 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.01 \261 0.0001, Protocol 2)",
                    "type": "lines",
                    "options":
                        [
                            "ls 3"
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001, Protocol 1)",
                    "type": "lines",
                    "options":
                        [
                            "ls 2",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-proto2.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001, Protocol 2)",
                    "type": "lines",
                    "options":
                        [
                            "ls 4"
                        ]
                }
            ]
    },  # End of VICBF scaling graph for 1000 users
    {  # Graph to display the VICBF scaling depending on FPR, u=100000
        "output": "eval-simu-vicbf-scaling-u100000-fpr.eps",
        "xlabel": "Step",
        "ylabel": "Size (MB)",
        "title": "Median Size of Serialized VI-CBF for different FPRs over Time (100k initial Users, Orphans only)",
        "options":
            [
                "set encoding iso_8859_1",
                "set termoption dash",
                "set key top left",
                "set for [i=1:5] linetype i lt i",
                'set style line 1 lt 6 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 2 lt 1 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 3 lt 6 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 4 lt 1 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 5 lt 6 lc rgb "green" lw ' + LINEWIDTH,
                'set style line 6 lt 1 lc rgb "green" lw ' + LINEWIDTH,
            ],
        "plot":
            [
                {
                    "input": "u100000/vicbf-scaling-fpr0.1-proto1.csv",
                    "x": "1",
                    "y": "($20 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 5",
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.01-proto1.csv",
                    "x": "1",
                    "y": "($20 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 1",
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.001-proto1.csv",
                    "x": "1",
                    "y": "($20 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 3"
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.1-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 6"
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.01-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 2",
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.001-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 4"
                        ]
                },
            ]
    },  # End of VICBF FPR scaling graph for u=100000
    {  # Graph to display the VICBF scaling depending on FPR, u=100000, compressed only
        "output": "eval-simu-vicbf-scaling-u100000-fpr-compressed.eps",
        "xlabel": "Step",
        "ylabel": "Size (MB)",
        "title": "Median Compressed VI-CBF Size for different FPRs over Time (u=100k, Orphans only)",
        "options":
            [
                "set encoding iso_8859_1",
                "set termoption dash",
                "set key top left",
                "set for [i=1:5] linetype i lt i",
                'set style line 1 lt 6 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 2 lt 1 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 3 lt 6 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 4 lt 1 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 5 lt 6 lc rgb "green" lw ' + LINEWIDTH,
                'set style line 6 lt 1 lc rgb "green" lw ' + LINEWIDTH,
            ],
        "plot":
            [
                {
                    "input": "u100000/vicbf-scaling-fpr0.1-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 6"
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.01-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 2",
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.001-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 4"
                        ]
                },
            ]
    },  # End of VICBF FPR scaling graph for u=100000
    {  # Graph to display the VICBF scaling depending on FPR for u=1000
        "output": "eval-simu-vicbf-scaling-u1000-fpr.eps",
        "xlabel": "Step",
        "ylabel": "Size (MB)",
        "title": "Median Size of Serialized VI-CBF for different FPRs over Time (1k initial Users, Orphans only)",
        "options":
            [
                "set encoding iso_8859_1",
                "set termoption dash",
                "set key top left",
                "set for [i=1:5] linetype i lt i",
                'set style line 1 lt 6 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 2 lt 1 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 3 lt 6 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 4 lt 1 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 5 lt 6 lc rgb "green" lw ' + LINEWIDTH,
                'set style line 6 lt 1 lc rgb "green" lw ' + LINEWIDTH,
            ],
        "plot":
            [
                {
                    "input": "u1000/vicbf-scaling-fpr0.1-proto1.csv",
                    "x": "1",
                    "y": "($20 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 5",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-proto1.csv",
                    "x": "1",
                    "y": "($20 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 1",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.001-proto1.csv",
                    "x": "1",
                    "y": "($20 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 3"
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.1-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 6"
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 2",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.001-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 4"
                        ]
                },
            ]
    },  # End of VICBF FPR scaling graph for u=1000
    {  # Graph to display the VICBF scaling depending on FPR for u=1000
        "output": "eval-simu-vicbf-scaling-u1000-fpr-compressed.eps",
        "xlabel": "Step",
        "ylabel": "Size (MB)",
        "title": "Median Compressed VI-CBF Size for different FPRs over Time (u=1k, Orphans only)",
        "options":
            [
                "set encoding iso_8859_1",
                "set termoption dash",
                "set key top left",
                "set for [i=1:5] linetype i lt i",
                'set style line 1 lt 6 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 2 lt 1 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 3 lt 6 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 4 lt 1 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 5 lt 6 lc rgb "green" lw ' + LINEWIDTH,
                'set style line 6 lt 1 lc rgb "green" lw ' + LINEWIDTH,
            ],
        "plot":
            [
                {
                    "input": "u1000/vicbf-scaling-fpr0.1-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 6"
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 2",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.001-proto1.csv",
                    "x": "1",
                    "y": "($21 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 4"
                        ]
                },
            ]
    },  # End of VICBF FPR scaling graph for u=1000, compressed only
    {  # Graph to display the VICBF scaling depending on FPR, productive KVs only, u=100000
        "output": "eval-simu-vicbf-scaling-u100000-productive.eps",
        "xlabel": "Step",
        "ylabel": "Size (MB)",
        "title": "Median Size of Serialized VI-CBF for different FPRs over Time (100k initial Users, Non-Orphans only)",
        "options":
            [
                "set encoding iso_8859_1",
                "set termoption dash",
                "set key top left",
                "set for [i=1:5] linetype i lt i",
                'set style line 1 lt 6 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 2 lt 1 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 3 lt 6 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 4 lt 1 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 5 lt 6 lc rgb "green" lw ' + LINEWIDTH,
                'set style line 6 lt 1 lc rgb "green" lw ' + LINEWIDTH,
            ],
        "plot":
            [
                {
                    "input": "u100000/vicbf-scaling-fpr0.1-retronly.csv",
                    "x": "1",
                    "y": "($5 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 5",
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.01-retronly.csv",
                    "x": "1",
                    "y": "($5 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 1",
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.001-retronly.csv",
                    "x": "1",
                    "y": "($5 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 3"
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.1-retronly.csv",
                    "x": "1",
                    "y": "($6 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 6"
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.01-retronly.csv",
                    "x": "1",
                    "y": "($6 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 2",
                        ]
                },
                {
                    "input": "u100000/vicbf-scaling-fpr0.001-retronly.csv",
                    "x": "1",
                    "y": "($6 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 4"
                        ]
                },
            ]
    },  # End of VICBF FPR scaling graph for u=100000 for productive KVs only
    {  # Graph to display the VICBF scaling depending on FPR, productive KVs only, u=1000
        "output": "eval-simu-vicbf-scaling-u1000-productive.eps",
        "xlabel": "Step",
        "ylabel": "Size (MB)",
        "title": "Median Size of Serialized VI-CBF for different FPRs over Time (1k initial Users, Non-Orphans only)",
        "options":
            [
                "set encoding iso_8859_1",
                "set termoption dash",
                "set key top left",
                "set for [i=1:5] linetype i lt i",
                'set style line 1 lt 6 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 2 lt 1 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 3 lt 6 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 4 lt 1 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 5 lt 6 lc rgb "green" lw ' + LINEWIDTH,
                'set style line 6 lt 1 lc rgb "green" lw ' + LINEWIDTH,
            ],
        "plot":
            [
                {
                    "input": "u1000/vicbf-scaling-fpr0.1-retronly.csv",
                    "x": "1",
                    "y": "($5 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 5",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-retronly.csv",
                    "x": "1",
                    "y": "($5 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 1",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.001-retronly.csv",
                    "x": "1",
                    "y": "($5 / 1024 / 1024)",
                    "title": "Uncompressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 3"
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.1-retronly.csv",
                    "x": "1",
                    "y": "($6 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 6"
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-retronly.csv",
                    "x": "1",
                    "y": "($6 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 2",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.001-retronly.csv",
                    "x": "1",
                    "y": "($6 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 4"
                        ]
                },
            ]
    },  # End of VICBF FPR scaling graph for u=100000 for productive KVs only
    {  # Graph to display the VICBF scaling depending on FPR, productive KVs only, u=1000, only compressed
        "output": "eval-simu-vicbf-scaling-u1000-productive-compressed.eps",
        "xlabel": "Step",
        "ylabel": "Size (MB)",
        "title": "Median Compressed VI-CBF Size for different FPRs over Time (u=1k, Non-Orphans only)",
        "options":
            [
                "set encoding iso_8859_1",
                "set termoption dash",
                "set key top left",
                "set for [i=1:5] linetype i lt i",
                'set style line 1 lt 6 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 2 lt 1 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 3 lt 6 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 4 lt 1 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 5 lt 6 lc rgb "green" lw ' + LINEWIDTH,
                'set style line 6 lt 1 lc rgb "green" lw ' + LINEWIDTH,
            ],
        "plot":
            [
                {
                    "input": "u1000/vicbf-scaling-fpr0.1-retronly.csv",
                    "x": "1",
                    "y": "($6 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 6"
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-retronly.csv",
                    "x": "1",
                    "y": "($6 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 2",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.001-retronly.csv",
                    "x": "1",
                    "y": "($6 / 1024 / 1024)",
                    "title": "Compressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 4"
                        ]
                },
            ]
    },  # End of VICBF FPR scaling graph for u=100000 for productive KVs only
    {  # Graph to display the VICBF scaling depending on FPR, productive KVs only, u=1000, static network
        "output": "eval-simu-vicbf-scaling-u1000-productive-static.eps",
        "xlabel": "Step",
        "ylabel": "Size (KB)",
        "title": "Median Size of Serialized VI-CBF for different FPRs over Time (1k initial Users, static network)",
        "options":
            [
                "set encoding iso_8859_1",
                "set termoption dash",
                "set key top left",
                "set for [i=1:5] linetype i lt i",
                'set style line 1 lt 6 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 2 lt 1 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 3 lt 6 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 4 lt 1 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 5 lt 6 lc rgb "green" lw ' + LINEWIDTH,
                'set style line 6 lt 1 lc rgb "green" lw ' + LINEWIDTH,
            ],
        "plot":
            [
                {
                    "input": "u1000/vicbf-scaling-fpr0.1-retronly-static.csv",
                    "x": "1",
                    "y": "($5 / 1024)",
                    "title": "Uncompressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 5",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-retronly-static.csv",
                    "x": "1",
                    "y": "($5 / 1024)",
                    "title": "Uncompressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 1",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.001-retronly-static.csv",
                    "x": "1",
                    "y": "($5 / 1024)",
                    "title": "Uncompressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 3"
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.1-retronly-static.csv",
                    "x": "1",
                    "y": "($6 / 1024)",
                    "title": "Compressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 6"
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-retronly-static.csv",
                    "x": "1",
                    "y": "($6 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 2",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.001-retronly-static.csv",
                    "x": "1",
                    "y": "($6 / 1024)",
                    "title": "Compressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 4"
                        ]
                },
            ]
    },  # End of VICBF FPR scaling graph for u=100000 for productive KVs only, static network
    {  # Graph to display the VICBF scaling depending on FPR, productive KVs only, u=1000, static network, compressed only
        "output": "eval-simu-vicbf-scaling-u1000-productive-static-compressed.eps",
        "xlabel": "Step",
        "ylabel": "Size (KB)",
        "title": "Median Compressed VI-CBF Size for different FPRs over Time (u=1k, static network)",
        "options":
            [
                "set encoding iso_8859_1",
                "set termoption dash",
                "set key top left",
                "set for [i=1:5] linetype i lt i",
                'set style line 1 lt 6 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 2 lt 1 lc rgb "red" lw ' + LINEWIDTH,
                'set style line 3 lt 6 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 4 lt 1 lc rgb "blue" lw ' + LINEWIDTH,
                'set style line 5 lt 6 lc rgb "green" lw ' + LINEWIDTH,
                'set style line 6 lt 1 lc rgb "green" lw ' + LINEWIDTH,
            ],
        "plot":
            [
                {
                    "input": "u1000/vicbf-scaling-fpr0.1-retronly-static.csv",
                    "x": "1",
                    "y": "($6 / 1024)",
                    "title": "Compressed (FPR=0.1 \261 0.001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 6"
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.01-retronly-static.csv",
                    "x": "1",
                    "y": "($6 / 1024)",
                    "title": "Compressed (FPR=0.01 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 2",
                        ]
                },
                {
                    "input": "u1000/vicbf-scaling-fpr0.001-retronly-static.csv",
                    "x": "1",
                    "y": "($6 / 1024)",
                    "title": "Compressed (FPR=0.001 \261 0.0001)",
                    "type": "lines",
                    "options":
                        [
                            "ls 4"
                        ]
                },
            ]
    },  # End of VICBF FPR scaling graph for u=100000 for productive KVs only, static network
    {  # Graph to display the median number of Type I and II orphaned records over time
        "output": "eval-simu-orphaned-records.eps",
        "xlabel": "Step",
        "ylabel": "Number of Pairs",
        "title": "Median Number of Orphaned Key-Value-Pairs over Time (100k initial Users)",
        "options":
            [
                "set encoding iso_8859_1",
                "set key top left",
                "set format y '%.0s %c'"
            ],
        "plot":
            [
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "22",
                    "title": "Type I",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "($32 - $22)",
                    "title": "Type II",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "32",
                    "title": "Type I + II",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
            ]
    },  # End of orphaned records over time graph
    {  # Type I + II Orphan boxplot
        "output": "eval-simu-orphaned-records-1+2-boxplot.eps",
        "xlabel": "Step",
        "ylabel": "Number of Pairs",
        "title": "Number of Orphaned Key-Value-Pairs over Time (100k initial Users)",
        "options":
            [
                "set encoding iso_8859_1",
                "set xrange[0:205]",
                "set key top left",
                "set format y '%.0s %c'"
            ],
        "plot":
            [
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "33:35:36:34:52",
                    "title": "Type I + II",
                    "type": "candlesticks",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ],
                    "options_post":
                        [
                            "whiskerbars"
                        ]
                },
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "32:32:32:32:52",
                    "title": None,
                    "type": "candlesticks",
                    "options":
                        [
                            "lc rgb '#000000'",
                            "lt -1",
                            "notitle"
                        ]
                },
            ]
    },  # End of boxplot of Type I + II records
    {  # Type I + II Orphan boxplot
        "output": "eval-simu-productive-records-boxplot.eps",
        "xlabel": "Step",
        "ylabel": "Number of Pairs",
        "title": "Number of Non-Orphaned Key-Value-Pairs over Time (100k initial Users)",
        "options":
            [
                "set encoding iso_8859_1",
                "set xrange[0:205]",
                "set format y '%.0s %c'"
            ],
        "plot":
            [
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "38:40:41:39:52",
                    "title": "Quartiles / Min / Max",
                    "type": "candlesticks",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ],
                    "options_post":
                        [
                            "whiskerbars"
                        ]
                },
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "37:37:37:37:52",
                    "title": None,
                    "type": "candlesticks",
                    "options":
                        [
                            "lc rgb '#000000'",
                            "lt -1",
                            "notitle"
                        ]
                },
            ]
    },  # End of boxplot of Type I + II records
    {  # Type I + II Orphan boxplot
        "output": "eval-simu-productive-records-static-boxplot.eps",
        "xlabel": "Step",
        "ylabel": "Number of Pairs",
        "title": "Number of Non-Orphaned Key-Value-Pairs over Time (1k Users, Static Network)",
        "options":
            [
                "set encoding iso_8859_1",
                "set xrange[0:205]",
                "set format y '%.0s %c'"
            ],
        "plot":
            [
                {
                    "input": "u1000/simulation-rounds-static.csv",
                    "x": "1",
                    "y": "38:40:41:39:52",
                    "title": "Quartiles / Min / Max",
                    "type": "candlesticks",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ],
                    "options_post":
                        [
                            "whiskerbars"
                        ]
                },
                {
                    "input": "u1000/simulation-rounds-static.csv",
                    "x": "1",
                    "y": "37:37:37:37:52",
                    "title": None,
                    "type": "candlesticks",
                    "options":
                        [
                            "lc rgb '#000000'",
                            "lt -1",
                            "notitle"
                        ]
                },
            ]
    },  # End of boxplot of Type I + II records
    {  # Graph to display the number of Type II orphans
        "output": "eval-simu-orphans-type2.eps",
        "xlabel": "Step",
        "ylabel": "Number of Pairs",
        "title": "Number of Type II Orphans over Time (100k initial Users)",
        "options":
            [
                "set encoding iso_8859_1",
                "set xrange[0:205]",
                "set format y '%.0s %c'"
            ],
        "plot":
            [
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "($33 - $23):($35 - $25):($36 - $26):($34 - $24):52",
                    "title": "Quartiles / Min / Max",
                    "type": "candlesticks",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ],
                    "options_post":
                        [
                            "whiskerbars"
                        ]
                },
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "($32 - $22):($32 - $22):($32 - $22):($32 - $22):52",
                    "title": None,
                    "type": "candlesticks",
                    "options":
                        [
                            "lc rgb '#000000'",
                            "lt -1",
                            "notitle"
                        ]
                }
            ]
    },  # End of Type II Orphans
    {  # Graph to display the number of Type I orphans
        "output": "eval-simu-orphans-type1.eps",
        "xlabel": "Step",
        "ylabel": "Number of Pairs",
        "title": "Number of Type I Orphans over Time (100k initial Users)",
        "options":
            [
                "set encoding iso_8859_1",
                "set xrange[0:205]",
                "set format y '%.0s %c'"
            ],
        "plot":
            [
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "23:25:26:24:52",
                    "title": "Quartiles / Min / Max",
                    "type": "candlesticks",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ],
                    "options_post":
                        [
                            "whiskerbars"
                        ]
                },
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "22:22:22:22:52",
                    "title": None,
                    "type": "candlesticks",
                    "options":
                        [
                            "lc rgb '#000000'",
                            "lt -1",
                            "notitle"
                        ]
                }
            ]
    },
    {  # Graph to display difference between median orphaned records
        "output": "eval-simu-orphaned-records-compare.eps",
        "xlabel": "Step",
        "ylabel": "Number of Pairs",
        "title": "Median Number of Orphaned Key-Value-Pairs over Time (Comparison, 100k initial Users)",
        "options":
            [
                "set encoding iso_8859_1",
                "set xrange[0:205]",
                "set key top left",
                "set format y '%.0s %c'"
            ],
        "plot":
            [
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "32",
                    "title": "Median (Protocol 1)",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                },
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "($32 - $22)",
                    "title": "Median (Protocol 2)",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                }
            ]
    },  # End of graph to display difference between median orphaned records
    {  # Graph to display the development of the user count over time for 100k initial
        "output": "impl-simu-user-count-development.eps",
        "xlabel": "Step",
        "ylabel": "Number of Users",
        "title": "Median Number of Active Users over Time (100k initial Users)",
        "options":
            [
                "set encoding iso_8859_1",
                "set key top left",
                "set format y '%.0s %c'"
            ],
        "plot":
            [
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "2",
                    "title": "Active and Inactive Users",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                },
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "7",
                    "title": "Active Users",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                },
                {
                    "input": "u100000/simulation-rounds.csv",
                    "x": "1",
                    "y": "12",
                    "title": "Inactive Users",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                }
            ]
    },  # End of graph to display development of user count over time for 100k initial
    {  # Graph to display the development of the user count over time for 1k initial
        "output": "impl-simu-user-count-development-u1000.eps",
        "xlabel": "Step",
        "ylabel": "Number of Users",
        "title": "Median Number of Active Users over Time (1k initial Users)",
        "options":
            [
                "set encoding iso_8859_1",
                "set key top left",
                "set format y '%.0s %c'"
            ],
        "plot":
            [
                {
                    "input": "u1000/simulation-rounds.csv",
                    "x": "1",
                    "y": "2",
                    "title": "Active and Inactive Users",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                },
                {
                    "input": "u1000/simulation-rounds.csv",
                    "x": "1",
                    "y": "7",
                    "title": "Active Users",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                },
                {
                    "input": "u1000/simulation-rounds.csv",
                    "x": "1",
                    "y": "12",
                    "title": "Inactive Users",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH,
                        ]
                }
            ]
    },  # End of graph to display development of user count over time
    {  # Graph to display the median number of Type I and II orphaned records over time (u1000)
        "output": "eval-simu-orphaned-records-u1000.eps",
        "xlabel": "Step",
        "ylabel": "Number of Pairs",
        "title": "Median Number of Orphaned Key-Value-Pairs over Time (1k initial Users)",
        "options":
            [
                "set encoding iso_8859_1",
                "set key top left",
                "set format y '%.0s %c'"
            ],
        "plot":
            [
                {
                    "input": "u1000/simulation-rounds.csv",
                    "x": "1",
                    "y": "22",
                    "title": "Type I",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "u1000/simulation-rounds.csv",
                    "x": "1",
                    "y": "($32 - $22)",
                    "title": "Type II",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "u1000/simulation-rounds.csv",
                    "x": "1",
                    "y": "32",
                    "title": "Type I + II",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
            ]
    },  # End of orphaned records over time graph (u1000)
    {  # Graph to display the median performance of VICBF inserts
        "output": "eval-comp-vicbf-inserts.eps",
        "xlabel": "Slots",
        "ylabel": "ms",
        "title": "Median Performance of VI-CBF Inserts",
        "options":
            [
                "set encoding iso_8859_1",
                "set format x '%.0s %c'",
                "set key bottom left"
            ],
        "plot":
            [
                {
                    "input": "< awk '$1 ~ /^insert$/ && $2 ~ /^2$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4 / 1000000)",
                    "title": "k=2",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^insert$/ && $2 ~ /^3$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4 / 1000000)",
                    "title": "k=3",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^insert$/ && $2 ~ /^4$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4 / 1000000)",
                    "title": "k=4",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^insert$/ && $2 ~ /^5$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4 / 1000000)",
                    "title": "k=5",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
            ]
    },  # End of median VICBF insert performance
    {  # Graph to display the median performance of true positive VICBF queries
        "output": "eval-comp-vicbf-queryp.eps",
        "xlabel": "Slots",
        "ylabel": "ms",
        "title": "Median Performance of VI-CBF Queries (TP)",
        "options":
            [
                "set encoding iso_8859_1",
                "set format x '%.0s %c'",
                "set key bottom left"
            ],
        "plot":
            [
                {
                    "input": "< awk '$1 ~ /^queryp$/ && $2 ~ /^2$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4 / 1000000)",
                    "title": "k=2",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^queryp$/ && $2 ~ /^3$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4 / 1000000)",
                    "title": "k=3",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^queryp$/ && $2 ~ /^4$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4 / 1000000)",
                    "title": "k=4",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^queryp$/ && $2 ~ /^5$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4 / 1000000)",
                    "title": "k=5",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
            ]
    },  # End of true positive VICBF query performance
    {  # Graph to display the median performance of true negative / false positive VICBF queries
        "output": "eval-comp-vicbf-queryn.eps",
        "xlabel": "Slots",
        "ylabel": "ms",
        "title": "Median Performance of VI-CBF Queries (TN / FP)",
        "options":
            [
                "set encoding iso_8859_1",
                "set format x '%.0s %c'"
            ],
        "plot":
            [
                {
                    "input": "< awk '$1 ~ /^queryn$/ && $2 ~ /^2$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4 / 1000000)",
                    "title": "k=2",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^queryn$/ && $2 ~ /^3$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4 / 1000000)",
                    "title": "k=3",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^queryn$/ && $2 ~ /^4$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4 / 1000000)",
                    "title": "k=4",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^queryn$/ && $2 ~ /^5$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4 / 1000000)",
                    "title": "k=5",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
            ]
    },  # End of TN / FP VICBF Query performance
    {  # Graph to display the median performance of the VICBF serialization
        "output": "eval-comp-vicbf-serial.eps",
        "xlabel": "Slots",
        "ylabel": "ms",
        "title": "Median Performance of VI-CBF Serialization (10k entries)",
        "options":
            [
                "set encoding iso_8859_1",
                "set format x '%.0s %c'",
                "set key top left"
            ],
        "plot":
            [
                {
                    "input": "< awk '$1 ~ /^serialize$/ && $2 ~ /^2$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4)",
                    "title": "k=2",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^serialize$/ && $2 ~ /^3$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4)",
                    "title": "k=3",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^serialize$/ && $2 ~ /^4$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4)",
                    "title": "k=4",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^serialize$/ && $2 ~ /^5$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($4)",
                    "title": "k=5",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
            ]
    },  # End of TN / FP VICBF serialization performance
    {  # Graph to display the median processing time increase when adding compression to serialization
        "output": "eval-comp-vicbf-serial-comp-increase.eps",
        "xlabel": "Slots",
        "ylabel": "ms",
        "title": "Median Compression Time for Serialized Data (10k entries)",
        "options":
            [
                "set encoding iso_8859_1",
                "set format x '%.0s %c'",
                "set key top left"
            ],
        "plot":
            [
                {
                    "input": "< awk '$1 ~ /^serialize$/ && $2 ~ /^2$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($9 - $4)",
                    "title": "k=2",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^serialize$/ && $2 ~ /^3$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($9 - $4)",
                    "title": "k=3",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^serialize$/ && $2 ~ /^4$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($9 - $4)",
                    "title": "k=4",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "< awk '$1 ~ /^serialize$/ && $2 ~ /^5$/' benchmark/vicbf-benchmark.txt",
                    "x": "3",
                    "y": "($9 - $4)",
                    "title": "k=5",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
            ]
    },  # End of TN / FP VICBF serialization performance
    {  # Graph to display the VICBF serialization size with different strategies
        "output": "app-vicbfser-smart.eps",
        "xlabel": "Number of entries",
        "ylabel": "Size (bytes)",
        "title": "Size of Serialized VI-CBF with Smart Serialization Strategy",
        "options":
            [
                "set encoding iso_8859_1",
                "set key bottom right"
            ],
        "plot":
            [
                {
                    "input": "serialization/vicbf-serialization-size-smart.txt",
                    "x": "1",
                    "y": "2",
                    "title": "Uncompressed",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "serialization/vicbf-serialization-size-smart.txt",
                    "x": "1",
                    "y": "3",
                    "title": "Compressed",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },

            ]
    },  # End of VICBF serialization size with smart strategy
    {  # Graph to display the VICBF serialization size with full strategy
        "output": "app-vicbfser-full.eps",
        "xlabel": "Number of entries",
        "ylabel": "Size (bytes)",
        "title": "Size of Serialized VI-CBF with Full Serialization Strategy",
        "options":
            [
                "set encoding iso_8859_1",
                "set key bottom right"
            ],
        "plot":
            [
                {
                    "input": "serialization/vicbf-serialization-size-full.txt",
                    "x": "1",
                    "y": "2",
                    "title": "Uncompressed",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },
                {
                    "input": "serialization/vicbf-serialization-size-full.txt",
                    "x": "1",
                    "y": "3",
                    "title": "Compressed",
                    "type": "lines",
                    "options":
                        [
                            "lw " + LINEWIDTH
                        ]
                },

            ]
    },  # End of VICBF serialization size with full strategy
]

for target in TARGET:
    print "Generate:", target["title"], "=>", target["output"]
    # Fill in the template
    output = TEMPLATE.format(TERMINAL,
                             OUTPUT_PREFIX + target["output"],
                             target["title"],
                             FONTSIZE,
                             target["xlabel"],
                             target["ylabel"])

    # Add additional options like logscale
    if target["options"] is not None:
        for option in target["options"]:
            output += option + "\n"

    # Add plot commands
    plotcmd = "plot "
    for plot in target["plot"]:
        target = ""
        if "filter" in plot.keys():
            target = "< awk '${0} ~ /^{1}$/' {2}".format(plot["filter"]["column"],
                                                         plot["filter"]["value"],
                                                         plot["input"])
        else:
            target = plot["input"]

        plotcmd += '"' + target + '" u ' + plot["x"] + ":" + plot["y"] + ' '
        plotcmd += "w " + plot["type"] + " "
        if plot["options"] is not None:
            for option in plot["options"]:
                plotcmd += option + " "

        if plot["title"] is not None:
            plotcmd += "t '" + plot["title"] + "' "

        if "options_post" in plot.keys():
            for option in plot["options_post"]:
                plotcmd += option + " "

        plotcmd += ", "
    # Merge plot commands into output
    output += plotcmd[:-2] + "\n"

    # Execute command to generate Gnuplot
    pobj = Popen(['/usr/bin/gnuplot'], stdin=PIPE)
    pobj.communicate(input=output)
    pobj.wait()
