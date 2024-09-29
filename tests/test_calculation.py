from myapp.calculations import add,multiply
import pytest


def test_multiply():
    assert multiply(10,9)==90


@pytest.mark.parametrize("nums1, nums2, sum", 
 (
     [1,2,3],[10,90,100],[0,0,0]
 )
 )
def test_add(nums1,nums2,sum):
    assert add(nums1,nums2)== sum




