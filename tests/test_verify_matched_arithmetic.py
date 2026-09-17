"""Adversarial archive checks; CLI separately performs expensive gate re-emission."""

import copy
import json
import shutil

import pytest

from research.journal_sprint import verify_matched_arithmetic as verifier
from research.journal_sprint.storage import ROOT, sha256


ARCHIVE = ROOT/'results/journal_sprint/matched_arithmetic_v1'


def write(path, data):
    path.write_text(json.dumps(data), encoding='utf-8')


def rehash(path):
    write(path/'complete.json', {'sha256': {n: sha256(path/n) for n in verifier.FILES}})


@pytest.fixture
def archive(tmp_path, monkeypatch):
    path = tmp_path/'archive'
    shutil.copytree(ARCHIVE, path)
    expected = {case: verifier.read(ARCHIVE/('case_'+case+'.json')) for case in ('D1', 'D2')}
    finite = verifier.read(ARCHIVE/'finite.json')
    # These tests target comparison/mutation rejection. The recorded CLI receipt
    # performs real provenance checks, fresh circuits, budgets and finite replay.
    monkeypatch.setattr(verifier, 'provenance', lambda *args: None)
    monkeypatch.setattr(verifier, 'reconstruct_case', lambda key: copy.deepcopy(expected[key]))
    monkeypatch.setattr(verifier, 'reconstruct_finite', lambda: copy.deepcopy(finite))
    return path


def test_intact_archive_structure(archive):
    assert verifier.verify(archive)['rows_checked'] == 12


@pytest.mark.parametrize('mutation', ['duplicates', 'missing_budget', 'winner', 'qubits',
                                     'missing_component', 'production_promotion'])
def test_rehashed_semantic_mutations_are_rejected(archive, mutation):
    results = verifier.read(archive/'results.json')
    case = results['comparisons'][0]
    if mutation == 'duplicates':
        case['alternatives'] = [copy.deepcopy(case['alternatives'][0]) for _ in range(6)]
    elif mutation == 'missing_budget':
        case['alternatives'][-1]['budget']['components'].pop('preparation')
    elif mutation == 'winner':
        case['lowest_projection'] = {'mode': 'nonexistent', 'degree': 1}
    elif mutation == 'qubits':
        case['alternatives'][-1]['resources']['total_qubits'] = 1
    elif mutation == 'missing_component':
        case.pop('arithmetic_components')
    else:
        case['production_choice'] = 'reflection'
    write(archive/'case_D1.json', case)
    write(archive/'results.json', results)
    rehash(archive)
    with pytest.raises(ValueError, match='recomputation'):
        verifier.verify(archive)


def test_rehashed_missing_finite_menu_is_rejected(archive):
    write(archive/'finite.json', {})
    rehash(archive)
    with pytest.raises(ValueError, match='finite'):
        verifier.verify(archive)


def test_unhashed_artifact_change_is_rejected(archive):
    write(archive/'finite.json', {})
    with pytest.raises(ValueError, match='hash mismatch'):
        verifier.verify(archive)


def test_empty_sources_are_rejected_before_recomputation():
    planned = verifier.read(ARCHIVE/'planned.json')
    planned['source_sha256'] = {}
    with pytest.raises(ValueError, match='source inventory'):
        verifier.provenance(planned, verifier.read(ARCHIVE/'inputs.json'))


def test_empty_inputs_are_rejected_before_recomputation():
    with pytest.raises(ValueError, match='input inventory'):
        verifier.provenance(verifier.read(ARCHIVE/'planned.json'), {})


def test_extra_file_is_rejected(archive):
    (archive/'unrecorded.txt').write_text('extra', encoding='utf-8')
    with pytest.raises(ValueError, match='inventory'):
        verifier.verify(archive)


def test_unsafe_manifest_paths_are_rejected(archive):
    data = verifier.read(archive/'complete.json')
    data['sha256']['../outside.json'] = '0'*64
    write(archive/'complete.json', data)
    with pytest.raises(ValueError, match='inventory'):
        verifier.verify(archive)
