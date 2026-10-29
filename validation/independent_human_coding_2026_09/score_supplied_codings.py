"""Audit supplied coding files; calculate agreement without asserting coder provenance.
Run from this directory: python3 score_supplied_codings.py
Uses the Python standard library; preserves all original judgments.
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LABELS = ['explicit_rest', 'illness', 'other_non_injury', 'specific', 'vague', 'unknown']

def read(name):
    with (ROOT / name).open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 300, (name, 'Expected 300 rows')
    assert len({r['spell_id'] for r in rows}) == 300, (name, 'Duplicate IDs')
    return {r['spell_id']: r for r in rows}

def score(pairs):
    n = len(pairs)
    m1, m2 = Counter(x for x,y in pairs), Counter(y for x,y in pairs)
    agree = sum(x == y for x,y in pairs)
    pe = sum(m1[k]*m2[k] for k in LABELS)/n**2
    return dict(n=n, agreements=agree, disagreements=n-agree,
                observed_agreement=agree/n, expected_agreement=pe,
                cohen_kappa=(agree/n-pe)/(1-pe))

def write_csv(name, rows, fields):
    with (ROOT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

a, b, original = [read(n) for n in ['Encoded1.csv', 'Encoded2.txt', 'development_reference.csv']]
assert a.keys() == b.keys() == original.keys(), 'Mismatched ID sets'
combined = []
for key in a:
    x, y = a[key]['human_class_coder_1'], b[key]['human_class_coder_2']
    assert x in LABELS and y in LABELS, ('Invalid or missing label', key)
    assert a[key]['initial_designation_raw'] == b[key]['initial_designation_raw'] == original[key]['initial_designation_raw'], ('Changed description', key)
    assert not a[key]['human_class_coder_2'] and not b[key]['human_class_coder_1'], ('Unexpected populated column', key)
    combined.append(dict(spell_id=key, initial_designation_raw=a[key]['initial_designation_raw'],
                         supplied_coder_1=x, supplied_coder_2=y,
                         development_reference=original[key]['reference_class'], agreement=x==y))

fields = list(combined[0])
write_csv('coding_comparison.csv', combined, fields)
write_csv('coding_disagreements.csv', [r for r in combined if not r['agreement']], fields)
pairs = [(r['supplied_coder_1'], r['supplied_coder_2']) for r in combined]
counts = Counter(pairs)
write_csv('confusion_matrix.csv', [dict(coder_1=x, **{y:counts[x,y] for y in LABELS}) for x in LABELS], ['coder_1']+LABELS)
results = dict(
    checks={'unique_rows_per_file':300, 'ids_match_development_sample':True,
            'descriptions_unchanged':True, 'missing_or_invalid_labels':0},
    supplied_coder_1_vs_2=score(pairs),
    reference_vs_supplied_coder_1=score([(r['development_reference'],r['supplied_coder_1']) for r in combined]),
    reference_vs_supplied_coder_2=score([(r['development_reference'],r['supplied_coder_2']) for r in combined]),
    provenance=json.loads((ROOT/'coding_provenance.json').read_text()),
    limitations=['Development sample, not held-out validation.',
                 'Agreement measures consistency of wording labels, not medical truth.',
                 'Reference comparisons use the assistant-coded development reference, not a gold standard.',
                 'No adjudication or changes to the frozen panel taxonomy have been made.'],
    source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['Encoded1.csv','Encoded2.txt','development_reference.csv']})
(ROOT/'agreement_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
