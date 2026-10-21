OPENQASM 3.0;
include "stdgates.inc";
bit[3] c;
qubit[10] q;
ccx q[0], q[1], q[7];
ccx q[7], q[2], q[8];
ccx q[8], q[3], q[9];
ccx q[9], q[4], q[5];
h q[9];
c[0] = measure q[9];
if (c[0]) {
  cz q[8], q[3];
  x q[9];
}
h q[8];
c[1] = measure q[8];
if (c[1]) {
  cz q[7], q[2];
  x q[8];
}
h q[7];
c[2] = measure q[7];
if (c[2]) {
  cz q[0], q[1];
  x q[7];
}
