#!/usr/bin/python3

import os
import argparse
import csv
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('files', type=str, nargs='+')
parser.add_argument('output', type=str)
parser.add_argument('-b', '--before', type=str, default=datetime.datetime.max.strftime('%4Y-%m-%d %H:%M'))
parser.add_argument('-a', '--after', type=str, default=datetime.datetime.min.strftime('%4Y-%m-%d %H:%M'))
parser.add_argument('-d', '--delimiter', type=str, default='\t')
args = parser.parse_args()
before = datetime.datetime.strptime(args.before, '%Y-%m-%d %H:%M')
after = datetime.datetime.strptime(args.after, '%Y-%m-%d %H:%M')


fo = open(args.output, 'w')
w = csv.writer(fo, delimiter=args.delimiter)
w.writerow(['time', 'batch', 'cycle', 'phase', 'en', 'rp', 'ec', 'cur', 'prs_md', 'prs_pf', 'vol_di', 'vol_rg', 'vol_fw'])

for n, name in enumerate(args.files):
    c, h = list(), dict()
    fi = open(name, 'r')
    t0s = os.path.split(name)[-1].split('.')[0]
    t0 = datetime.datetime.strptime(t0s, '%Y%m%d%H%M%S')

    while True:
        l = fi.readline()
        if len(l) == 0:
            break
        if l[0] == '\0':
            continue
        c.append(l)

    r = csv.reader(c, delimiter=args.delimiter)
    for i, v in enumerate(next(r)):
        h[v] = i

    for l in r:
        if len(l) != len(h):
            continue

        try:
            time = t0 + datetime.timedelta(0, round(float(l[h['time']])))
        except ValueError:
            continue

        batch = n + int(l[h['count']])
        cycle = int(l[h['cyc']])
        phase = l[h['proc']].lower() + '-' + l[h['ph']]
        en = int(l[h['mod-en']])
        rp = int(l[h['mod-pl']])
        ec = round(float(l[h['ec']]) * 10000)  # conductivity (uS/cm)
        cur = float(l[h['cur']])  # current (A)
        prs_md = round(float(l[h['mod-ps']]) / 100000, 3)  # module pressure (bar)
        prs_pf = round(float(l[h['pf-ps']]) / 100000, 3)  # prefilter pressure (bar)
        vol_di = float(l[h['di-vol']])  # deionization tank volume (l)
        vol_rg = float(l[h['rg-vol']])  # regeneration tank volume (l)
        vol_fw = float(l[h['fw1-vol']])  # freshwater tank volume (l)

        if time > before:
            break
        if time < after:
            continue

        w.writerow(
            [time, batch, cycle, phase, en, rp, ec, cur, prs_md, prs_pf, vol_di, vol_rg, vol_fw]
        )
