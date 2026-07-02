import dace
import copy


def test_memlet_replace() -> None:
    M = dace.symbol('M')
    N = dace.symbol("N")

    memlet = dace.Memlet(data="A", subset='0:M')
    original = copy.deepcopy(memlet)

    memlet.replace({"M": N})
    memlet.replace({N: M})

    assert memlet == original


if __name__ == "__main__":
    test_memlet_replace()
