from typing import (
    Any,
    Dict,
    List,
    Mapping,
    MutableSequence,
    NewType,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

import pytest

from yui.type import (
    Namespace,
    cast,
    is_container,
)


class User(Namespace):

    id: str
    pw: str
    addresses: Optional[List[str]]


def test_cast():

    ID = NewType('ID', str)

    assert cast(int, '3') == 3
    assert cast(List[str], ('kirito', 'asuna')) == ['kirito', 'asuna']
    assert cast(List[int], ('1', '2', '3')) == [1, 2, 3]
    assert cast(Sequence[int], ('1', '2', '3')) == [1, 2, 3]
    assert cast(MutableSequence[int], ('1', '2', '3')) == [1, 2, 3]
    assert cast(Tuple[int, float, str], ['1', '2', '3']) == (1, 2.0, '3')
    assert cast(Set[int], ['1', '1', '2']) == {1, 2}
    assert cast(Optional[int], 3) == 3
    assert cast(Optional[int], None) is None
    assert cast(Union[int, float], '3.2') == 3.2
    assert cast(List[ID], [1, 2, 3]) == [ID(1), ID(2), ID(3)]
    assert cast(Dict[str, Any], {1: 1, 2: 2.2}) == {'1': 1, '2': 2.2}
    assert cast(Mapping[str, str], {1: 1, 2: 2.2}) == {'1': '1', '2': '2.2'}
    assert cast(List, ('kirito', 'asuna', 16.5)) == ['kirito', 'asuna', 16.5]
    assert cast(Sequence, ('kirito', 'asuna', 16.5)) == [
        'kirito', 'asuna', 16.5]
    assert cast(MutableSequence, ('kirito', 'asuna', 16.5)) == [
        'kirito', 'asuna', 16.5]
    assert cast(Tuple, ['1', 2, 3.0]) == ('1', 2, 3.0)
    assert cast(Set, {'1', 2, 3.0, 2}) == {'1', 2, 3.0}
    assert cast(Dict, {'1': 'kirito', 2: 'asuna', 3: 16.5}) == {
        '1': 'kirito',
        2: 'asuna',
        3: 16.5,
    }
    assert cast(Mapping, {'1': 'kirito', 2: 'asuna', 3: 16.5}) == {
        '1': 'kirito',
        2: 'asuna',
        3: 16.5,
    }
    user = cast(User, {'id': 'item4', 'pw': 'supersecret'})
    assert user.id == 'item4'
    assert user.pw == 'supersecret'
    assert user.addresses is None
    users = cast(
        List[User],
        [
            {'id': 'item4', 'pw': 'supersecret'},
            {'id': 'item2', 'pw': 'weak', 'addresses': [1, 2]},
        ]
    )
    assert users[0].id == 'item4'
    assert users[0].pw == 'supersecret'
    assert users[0].addresses is None
    assert users[1].id == 'item2'
    assert users[1].pw == 'weak'
    assert users[1].addresses == ['1', '2']

    with pytest.raises(ValueError):
        cast(Union[int, float], 'asdf')


def test_is_container():
    assert is_container(List[int])
    assert is_container(Set[int])
    assert is_container(Tuple[int])
    assert is_container(list)
    assert is_container(set)
    assert is_container(tuple)
    assert not is_container(int)
    assert not is_container(float)
    assert not is_container(bool)
