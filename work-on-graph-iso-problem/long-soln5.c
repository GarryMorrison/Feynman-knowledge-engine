#include <stdio.h>
#include <math.h>

void main(void) {
signed long long n = 200;
//signed long long r = -1;
signed long long r = 1;
signed long long result;

printf("p = 5, r = %lld, n = %lld, start from 2\n",r,n);

for(signed long long a = 2; a <= n; a++) {
for(signed long long b = 2; b <= n; b++) {
for(signed long long c = 2; c <= n; c++) {
for(signed long long d = 2; d <= n; d++) {
for(signed long long e = 2; e <= n; e++) {
for(signed long long f = 2; f <= n; f++) {
//  result = (a*a*a + r*b*b*b + r*r*c*c*c - 3*r*a*b*c);
//  result = (pow(a,3) + pow(b,3)*r - 3*a*b*c*r + pow(c,3)*pow(r,2));
//  result = pow(a,4) - pow(b,4)*r + 4*a*pow(b,2)*c*r - 2*pow(a,2)*pow(c,2)*r - 4*pow(a,2)*b*d*r + pow(c,4)*pow(r,2) -
//   4*b*pow(c,2)*d*pow(r,2) + 2*pow(b,2)*pow(d,2)*pow(r,2) + 4*a*c*pow(d,2)*pow(r,2) - pow(d,4)*pow(r,3);
//  result = pow(a,5) + pow(b,5)*r - 5*a*pow(b,3)*c*r + 5*pow(a,2)*b*pow(c,2)*r + 5*pow(a,2)*pow(b,2)*d*r - 5*pow(a,3)*c*d*r -
//   5*pow(a,3)*b*e*r + pow(e,5)*r + pow(c,5)*pow(r,2) - 5*b*pow(c,3)*d*pow(r,2) + 5*pow(b,2)*c*pow(d,2)*pow(r,2) +
//   5*a*pow(c,2)*pow(d,2)*pow(r,2) - 5*a*b*pow(d,3)*pow(r,2) + 5*pow(b,2)*pow(c,2)*e*pow(r,2) - 5*a*pow(c,3)*e*pow(r,2) -
//   5*pow(b,3)*d*e*pow(r,2) - 5*a*b*c*d*e*pow(r,2) + 5*pow(a,2)*pow(d,2)*e*pow(r,2) + 5*a*pow(b,2)*pow(e,2)*pow(r,2) +
//   5*pow(a,2)*c*pow(e,2)*pow(r,2) + pow(d,5)*pow(r,3) - 5*c*pow(d,3)*e*pow(r,3) + 5*pow(c,2)*d*pow(e,2)*pow(r,3) +
//   5*b*pow(d,2)*pow(e,2)*pow(r,3) - 5*b*c*pow(e,3)*pow(r,3) - 5*a*d*pow(e,3)*pow(r,3);
  result = a*a*a*a*a + b*b*b*b*b*r - 5*a*b*b*b*c*r + 5*a*a*b*c*c*r + 5*a*a*b*b*d*r - 5*a*a*a*c*d*r -
   5*a*a*a*b*e*r + c*c*c*c*c*r*r - 5*b*c*c*c*d*r*r + 5*b*b*c*d*d*r*r +
   5*a*c*c*d*d*r*r - 5*a*b*d*d*d*r*r + 5*b*b*c*c*e*r*r - 5*a*c*c*c*e*r*r -
   5*b*b*b*d*e*r*r - 5*a*b*c*d*e*r*r + 5*a*a*d*d*e*r*r + 5*a*b*b*e*e*r*r +
   5*a*a*c*e*e*r*r + d*d*d*d*d*r*r*r - 5*c*d*d*d*e*r*r*r + 5*c*c*d*e*e*r*r*r +
   5*b*d*d*e*e*r*r*r - 5*b*c*e*e*e*r*r*r - 5*a*d*e*e*e*r*r*r + e*e*e*e*e*r*r*r*r;
  if (result == f*f*f*f*f) {
    printf("%lld %lld %lld %lld %lld : %lld\n",a,b,c,d,e,f);
//    return;
  }
}
}
}
}
}
}
return;
}
