from research.journal_sprint.reversible_fixed_point import basis,read
from .bin_oracle import bin_program,bin_for_bound


def test_all_signed_bin_flags_and_clean_scratch():
    for lo,hi in ((0,2),(2,4),(4,8)):
        for sign in (-1,1):
            p,(x,s),(flag,)=bin_program(4,3,lo,hi,sign)
            for val in range(-8,8):
                for sel in range(8):
                    expected=(val>=0 if sign>0 else val<0) and lo<=abs(val)<hi and sel<abs(val)
                    initial=basis(x,val)|basis(s,sel);final=p.run(initial)
                    assert read(final,(flag,))==expected
                    assert final==initial|(int(expected)<<flag)


def test_bin_probability_uses_its_own_upper_bound():
    for lower,upper in ((0,1),(1,2),(2,4)):
        for sign in (-1,1):
            p,(x,s),(flag,)=bin_for_bound(5,2,lower,upper,sign)
            for value in range(-15,16):
                count=0
                for selector in range(2**len(s)):
                    initial=basis(x,value)|basis(s,selector)
                    count+=read(p.run(initial),(flag,))
                eligible=(value>=0 if sign>0 else value<0) and lower<=abs(value)/4<upper
                assert count/(2**len(s))==(abs(value)/(4*upper) if eligible else 0.)
