#!/usr/bin/env python3
"""Reaggregate saved losses only. Python >=3.8 standard library; no forecasts."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import fmean
import sys

ROOT = Path(__file__).resolve().parent
MODELS = ('official-floor', 'semantics-only', 'semantic-gaussian', 'block-bootstrap')
FAMILY = {'factors_daily': 'factor_log_return', 'g10_fx_daily': 'fx_level',
          'em_transfer_early': 'fx_level', 'rates_daily': 'rate_level'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    manifest = read('manifest.json')
    for name, info in manifest['files'].items():
        path = ROOT / name
        require(path.is_file() and not path.is_symlink(), 'Missing or linked file: ' + name)
        require(path.stat().st_size == info['bytes'] and sha(path) == info['sha256'],
                'Integrity mismatch: ' + name)
    return len(manifest['files'])


def average(rows, keys, metrics):
    buckets = defaultdict(list)
    for row in rows:
        buckets[tuple(row[k] for k in keys)].append(row)
    return [{**dict(zip(keys, key)), **{m: fmean(r[m] for r in values) for m in metrics}}
            for key, values in sorted(buckets.items())]


def load_period(period):
    prefix = 'losses/' + period + '/'
    folds, groups, failures, run = (read(prefix + n) for n in
                                   ('folds.json', 'group-results.json', 'failures.json', 'run.json'))
    require(run['finished'] and run['source_unchanged'] and tuple(run['models']) == MODELS,
            period + ': incomplete or unexpected execution')
    seal = 'freeze-v1.json' if period == 'development' else 'freeze-v2.json'
    require(run['freeze_sha256'] == sha(ROOT / 'protocol' / seal), period + ': freeze identity mismatch')
    planned = {(r['grid'], r['origin']): r for r in folds}
    require(len(planned) == len(folds) == run['planned_per_model'], period + ': plan count mismatch')
    coverage = {}
    for model in MODELS:
        successes = [(r['grid'], r['origin']) for r in groups if r['model'] == model]
        failed = [(r['grid'], r['origin']) for r in failures if r['model'] == model]
        coverage[model] = {'planned': len(folds), 'success': len(successes), 'failure': len(failed)}
        require(len(set(successes + failed)) == len(successes + failed)
                and set(successes + failed) == set(planned), period + ': incomplete/duplicate denominator')
    require(not failures, period + ': failed predictions retained; no successful-subset table produced')
    require(len(groups) == len(folds) * len(MODELS), period + ': unexpected model rows')
    group_index = {}
    for row in groups:
        key = (row['grid'], row['origin'])
        require(all(row[k] == v for k, v in planned[key].items()), period + ': fold metadata mismatch')
        require(all(math.isfinite(row[k]) for k in ('marginal', 'tail', 'joint')),
                period + ': nonfinite group loss')
        group_index[(*key, row['model'])] = row
    with (ROOT / prefix / 'cell-results.csv').open(newline='', encoding='utf-8') as handle:
        cells = list(csv.DictReader(handle))
    seen, counts = set(), Counter()
    for row in cells:
        for key in ('horizon', 'year'):
            row[key] = int(row[key])
        for key in ('marginal', 'tail'):
            row[key] = float(row[key])
            require(math.isfinite(row[key]), period + ': nonfinite cell loss')
        key = (row['grid'], row['origin'], row['model'])
        group = group_index[key]
        cell = (*key, row['asset'], row['horizon'])
        require(cell not in seen, period + ': duplicate raw cell')
        seen.add(cell)
        counts[key] += 1
        require(row['source'] == group['sources'][row['asset']]
                and row['horizon'] in group['horizons'] and row['year'] == group['year'],
                period + ': cell metadata mismatch')
    require(all(counts[k] == len(g['assets']) * len(g['horizons']) for k, g in group_index.items()),
            period + ': missing cells')
    unique = average(cells, ('source', 'asset', 'origin', 'horizon', 'year', 'model'), ('marginal', 'tail'))
    annual = average(unique, ('source', 'asset', 'year', 'model'), ('marginal', 'tail'))
    support = {'coverage': coverage, 'series': len({(r['source'], r['asset']) for r in annual}),
               'series_years': len({(r['source'], r['asset'], r['year']) for r in annual}),
               'grids': len({r['grid'] for r in groups}), 'raw_cell_rows': len(cells),
               'unique_cells_per_method': len(unique) // len(MODELS)}
    return annual, groups, support


def marginal(annual, candidate, baseline):
    lookup = {(r['source'], r['asset'], r['year'], r['model']): r for r in annual}
    buckets = defaultdict(list)
    for row in annual:
        if row['model'] == candidate:
            key = (row['source'], row['asset'])
            buckets[key].append((row, lookup[(*key, row['year'], baseline)]))
    values = {metric: [] for metric in ('marginal', 'tail')}
    for pairs in buckets.values():
        for metric in values:
            numerator, denominator = (fmean(p[i][metric] for p in pairs) for i in (0, 1))
            require(denominator > 0, 'Nonpositive marginal denominator; do not silently drop series')
            values[metric].append(numerator / denominator)
    return {metric: fmean(v) for metric, v in values.items()}


def joint(groups, candidate, baseline):
    means = average(groups, ('grid', 'model'), ('joint',))
    lookup = {(r['grid'], r['model']): r['joint'] for r in means}
    details = []
    for grid in sorted({r['grid'] for r in groups}):
        num, den = lookup[(grid, candidate)], lookup[(grid, baseline)]
        require(den >= 0, 'Negative variogram denominator')
        details.append({'grid': grid, 'candidate_mean': num, 'baseline_mean': den,
                        'ratio': num / den if den > 0 else None})
    ratios = [d['ratio'] for d in details if d['ratio'] is not None]
    return fmean(ratios), details


def factor_yearly(annual, groups):
    factors = [r for r in annual if r['source'] == 'factors_daily']
    joint_rows = average([r for r in groups if set(r['sources'].values()) == {'factors_daily'}],
                         ('grid', 'year', 'model'), ('joint',))
    result = []
    for year in range(2019, 2025):
        for metric in ('marginal', 'tail', 'joint'):
            rows, identity = (joint_rows, ('grid',)) if metric == 'joint' else (factors, ('source', 'asset'))
            indexed = {(tuple(r[k] for k in identity), r['model']): r[metric]
                       for r in rows if r['year'] == year}
            ratios, paired = [], 0
            for key, model in indexed:
                if model != 'semantics-only':
                    continue
                paired += 1
                denominator = indexed[(key, 'official-floor')]
                require(denominator >= 0, 'Negative factor diagnostic denominator')
                if denominator > 0:
                    ratios.append(indexed[(key, model)] / denominator)
            result.append({'year': year, 'metric': metric, 'paired_units': paired,
                           'defined_units': len(ratios), 'undefined_zero_baseline_units': paired - len(ratios),
                           'equal_unit_ratio': fmean(ratios) if ratios else None,
                           'improved_units': sum(r < 1 - 1e-12 for r in ratios),
                           'worsened_units': sum(r > 1 + 1e-12 for r in ratios),
                           'tied_units': sum(abs(r - 1) <= 1e-12 for r in ratios),
                           'status': 'no_factor_observations' if not paired else
                           'no_positive_baseline' if not ratios else 'available'})
    return result


def reproduce():
    result = {'table2': [], 'table3': [], 'support': {}, 'joint_grid_details': {},
              'factor_joint_whole_period': {}}
    for period in ('development', 'later-124'):
        annual, groups, support = load_period(period)
        result['support'][period] = support
        factor_joint, factor_details = joint(
            [r for r in groups if set(r['sources'].values()) == {'factors_daily'}],
            'semantics-only', 'official-floor')
        result['factor_joint_whole_period'][period] = {
            'joint_ratio': factor_joint,
            'positive_baseline_grids': sum(r['ratio'] is not None for r in factor_details),
            'undefined_zero_baseline_grids': sum(r['ratio'] is None for r in factor_details)}
        for baseline in MODELS[:-1]:
            row = {'period': period, 'comparator': baseline,
                   **marginal(annual, 'block-bootstrap', baseline)}
            row['joint'], details = joint(groups, 'block-bootstrap', baseline)
            result['table2'].append(row)
            result['joint_grid_details'][period + '/' + baseline] = details
        if period == 'development':
            for family in sorted(set(FAMILY.values())):
                part = [r for r in annual if FAMILY[r['source']] == family]
                row = {'family': family, 'series': len({(r['source'], r['asset']) for r in part}),
                       'series_years': len({(r['source'], r['asset'], r['year']) for r in part})}
                for label, candidate, baseline in (
                        ('resampling/starter', 'block-bootstrap', 'official-floor'),
                        ('resampling/gaussian', 'block-bootstrap', 'semantic-gaussian'),
                        ('corrected/starter', 'semantics-only', 'official-floor')):
                    row[label] = marginal(part, candidate, baseline)
                result['table3'].append(row)
        else:
            result['table4'] = factor_yearly(annual, groups)
            result['table4_year_direction_counts'] = {}
            for metric in ('marginal', 'tail', 'joint'):
                rows = [r for r in result['table4'] if r['metric'] == metric]
                ratios = [r['equal_unit_ratio'] for r in rows if r['equal_unit_ratio'] is not None]
                counts = {'calendar_years': len(rows), 'supported_years': len(ratios),
                          'no_factor_observation_years': sum(r['status'] == 'no_factor_observations' for r in rows),
                          'only_zero_baseline_years': sum(r['status'] == 'no_positive_baseline' for r in rows)}
                for direction, n in (('improved', sum(r < 1 - 1e-12 for r in ratios)),
                                     ('worsened', sum(r > 1 + 1e-12 for r in ratios)),
                                     ('tied', sum(abs(r - 1) <= 1e-12 for r in ratios))):
                    counts[direction + '_years'], counts[direction + '_share'] = n, n / len(ratios)
                result['table4_year_direction_counts'][metric] = counts
    return result


def compare(actual, expected, path=''):
    if isinstance(expected, dict):
        require(set(actual) == set(expected), 'Output fields differ: ' + path)
        return max([compare(actual[k], v, path + '/' + k) for k, v in expected.items()] or [0.0])
    if isinstance(expected, list):
        require(len(actual) == len(expected), 'Output row count differs: ' + path)
        return max([compare(a, b, path + '/' + str(i)) for i, (a, b) in enumerate(zip(actual, expected))] or [0.0])
    if isinstance(expected, float):
        require(math.isfinite(actual) and abs(actual - expected) <= 2e-14, 'Numeric mismatch: ' + path)
        return abs(actual - expected)
    require(actual == expected, 'Value mismatch: ' + path)
    return 0.0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('verify', 'reproduce'))
    args = parser.parse_args()
    count = verify()
    if args.command == 'verify':
        print(json.dumps({'passed': True, 'verified_files': count}))
        return
    result = reproduce()
    expected = read('expected-tables.json')
    error = compare({k: result[k] for k in expected}, expected)
    result['verification'] = {'passed': True, 'verified_files': count,
                              'maximum_expected_table_error': error,
                              'scope': 'Point-estimate aggregation only; no interval or forecast regeneration'}
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError) as exc:
        sys.exit('Verification failed: ' + str(exc))
