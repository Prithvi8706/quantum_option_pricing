import math
import numpy as np
from .hierarchy import haar


def test_hierarchy_level_law_and_swap_symmetry():
    rng=np.random.default_rng(344)
    for f in (None,12):
        z=rng.integers(-30,31,size=(9,16,3))/16.
        for level in (1,2,3):
            fine,parent=haar(z,2,level,f)
            previous,_=haar(z,2,level-1,f)
            np.testing.assert_array_equal(parent,previous)
            changed=z.copy();changed[:,2*2**(level-1):2*2**level,:]*=-1
            swapped,_=haar(changed,2,level,f)
            np.testing.assert_array_equal(swapped[:,::2],fine[:,1::2])
            np.testing.assert_array_equal(swapped[:,1::2],fine[:,::2])
            if f is None:np.testing.assert_allclose((fine[:,::2]+fine[:,1::2])/math.sqrt(2),parent,atol=1e-14)


def test_haar_is_orthogonal_without_rounding():
    z=np.eye(16).reshape(16,16,1)
    x,_=haar(z,2,3)
    np.testing.assert_allclose(x[:,:,0]@x[:,:,0].T,np.eye(16),atol=1e-14)
