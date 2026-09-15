# Week 10 diagnostic extension, declared after v1

The original 80-case v1 returned zero enclosure failures, zero precision
instabilities, 40 disconnected sets, 10 empty sets, but ZERO disconnected
[1,2] final intersections. Its completion marker records execution, not a
passed topology gate. The original records and source snapshot are retained.

A subsequent exploratory production-only probe at counts [N/2,N/2], depths
[1,2], N=8,16,32 returned 7,5,3 components. These three deliberately selected
cases are now declared for independent reference checking as an extension;
they are not fresh confirmation. Run all 83 cases in a new output directory.
Same precision and enclosure criteria; fail explicitly if required topology
is absent. No original observation or numerical padding is changed.
