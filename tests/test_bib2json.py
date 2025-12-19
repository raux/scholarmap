import json, os, tempfile
from pathlib import Path

def run_bib2json(bib_content):
    # write temp ref.bib
    tmpdir = tempfile.mkdtemp()
    Path(tmpdir, 'ref.bib').write_text(bib_content)
    # run script
    import subprocess, sys
    subprocess.check_call([sys.executable,'bib2json.py'], cwd=tmpdir)
    return json.load(Path(tmpdir, 'bibtex.json').open())


def test_single_article():
    bib = '''@article{test2019,author={Doe, Jane and Smith, John},title={Test},year={2019},journal={Journal}}'''
    data = run_bib2json(bib)
    assert len(data['nodes']) == 3  # article + two authors
    types = {n['type'] for n in data['nodes']}
    assert 2 in types
    assert 1 in types
    links = data['links']
    assert len(links) == 2
    sources = {l['source'] for l in links}
    targets = {l['target'] for l in links}
    # article node index should be 2
    assert 2 in targets
