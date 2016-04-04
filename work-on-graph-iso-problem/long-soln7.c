#include <stdio.h>
#include <math.h>

void main(void) {
signed long long n = 200;
//signed long long r = -1;
//signed long long r = 1;
signed long long result;

printf("d = 7, n = %lld, start from 2\n",n);

for(signed long long a = 2; a <= n; a++) {
for(signed long long b = a; b <= n; b++) {
for(signed long long c = b; c <= n; c++) {
for(signed long long d = c; d <= n; d++) {
for(signed long long e = d; e <= n; e++) {
for(signed long long f = e; f <= n; f++) {
for(signed long long g = f; g <= n; e++) {
for(signed long long h = 2; h <= n; f++) {

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
/*  result = a*a*a*a*a + b*b*b*b*b*r - 5*a*b*b*b*c*r + 5*a*a*b*c*c*r + 5*a*a*b*b*d*r - 5*a*a*a*c*d*r -
   5*a*a*a*b*e*r + c*c*c*c*c*r*r - 5*b*c*c*c*d*r*r + 5*b*b*c*d*d*r*r +
   5*a*c*c*d*d*r*r - 5*a*b*d*d*d*r*r + 5*b*b*c*c*e*r*r - 5*a*c*c*c*e*r*r -
   5*b*b*b*d*e*r*r - 5*a*b*c*d*e*r*r + 5*a*a*d*d*e*r*r + 5*a*b*b*e*e*r*r +
   5*a*a*c*e*e*r*r + d*d*d*d*d*r*r*r - 5*c*d*d*d*e*r*r*r + 5*c*c*d*e*e*r*r*r +
   5*b*d*d*e*e*r*r*r - 5*b*c*e*e*e*r*r*r - 5*a*d*e*e*e*r*r*r + e*e*e*e*e*r*r*r*r;
*/
  result = pow(a,7) + pow(b,7) + pow(c,7) + pow(d,7) - 7*c*pow(d,5)*e +
   14*pow(c,2)*pow(d,3)*pow(e,2) - 7*pow(c,3)*d*pow(e,3) +
   pow(e,7) + 7*pow(c,2)*pow(d,4)*f - 21*pow(c,3)*pow(d,2)*e*f +
   7*pow(c,4)*pow(e,2)*f - 7*d*pow(e,5)*f + 7*pow(c,4)*d*pow(f,2) +
   14*pow(d,2)*pow(e,3)*pow(f,2) + 7*c*pow(e,4)*pow(f,2) -
   7*pow(d,3)*e*pow(f,3) - 21*c*d*pow(e,2)*pow(f,3) +
   7*c*pow(d,2)*pow(f,4) + 7*pow(c,2)*e*pow(f,4) + pow(f,7) -
   7*pow(c,3)*pow(d,3)*g + 14*pow(c,4)*d*e*g + 7*pow(d,2)*pow(e,4)*g -
   7*c*pow(e,5)*g - 7*pow(c,5)*f*g - 21*pow(d,3)*pow(e,2)*f*g +
   7*c*d*pow(e,3)*f*g + 7*pow(d,4)*pow(f,2)*g +
   35*c*pow(d,2)*e*pow(f,2)*g - 7*pow(c,2)*pow(e,2)*pow(f,2)*g -
   21*pow(c,2)*d*pow(f,3)*g - 7*e*pow(f,5)*g + 7*pow(d,4)*e*pow(g,2) -
   7*c*pow(d,2)*pow(e,2)*pow(g,2) + 14*pow(c,2)*pow(e,3)*pow(g,2) -
   21*c*pow(d,3)*f*pow(g,2) - 14*pow(c,2)*d*e*f*pow(g,2) +
   14*pow(c,3)*pow(f,2)*pow(g,2) + 14*pow(e,2)*pow(f,3)*pow(g,2) +
   7*d*pow(f,4)*pow(g,2) + 14*pow(c,2)*pow(d,2)*pow(g,3) -
   7*pow(c,3)*e*pow(g,3) - 7*pow(e,3)*f*pow(g,3) -
   21*d*e*pow(f,2)*pow(g,3) - 7*c*pow(f,3)*pow(g,3) +
   7*d*pow(e,2)*pow(g,4) + 7*pow(d,2)*f*pow(g,4) + 14*c*e*f*pow(g,4) -
   7*c*d*pow(g,5) + pow(g,7) - 7*pow(a,5)*(d*e + c*f + b*g) -
   7*pow(b,5)*(e*f + d*g) + 7*pow(b,4)*
    (pow(d,2)*e + c*pow(e,2) + 2*c*d*f + pow(c,2)*g + f*pow(g,2)) +
   7*pow(a,4)*(pow(c,2)*d + b*pow(d,2) + pow(b,2)*f + e*pow(f,2) +
      pow(e,2)*g + 2*d*f*g + c*(2*b*e + pow(g,2))) -
   7*pow(a,3)*(pow(b,3)*e + c*pow(e,3) + pow(d,3)*f -
      2*pow(c,2)*pow(f,2) + 3*pow(c,2)*e*g + pow(f,3)*g +
      3*e*f*pow(g,2) + pow(d,2)*(-2*pow(e,2) + 3*c*g) +
      b*(pow(c,3) + 3*pow(e,2)*f + 3*d*pow(f,2) - d*e*g - c*f*g) +
      pow(b,2)*(3*c*d - 2*pow(g,2)) + d*(-(c*e*f) + pow(g,3))) +
   7*pow(b,2)*(2*pow(c,3)*pow(d,2) + pow(c,4)*e -
      pow(d,2)*pow(e,2)*f + pow(d,3)*(2*pow(f,2) - 3*e*g) +
      pow(c,2)*(2*pow(f,3) + 5*e*f*g - d*pow(g,2)) +
      g*(pow(f,4) - e*pow(f,2)*g + 2*pow(e,2)*pow(g,2)) +
      d*(pow(e,4) - 3*f*pow(g,3)) +
      c*(-3*pow(e,3)*f - 2*d*e*pow(f,2) + 5*d*pow(e,2)*g -
         2*pow(d,2)*f*g + pow(g,4))) -
   7*pow(b,3)*(3*pow(c,2)*d*e + pow(c,3)*f - 2*pow(e,2)*pow(f,2) +
      pow(e,3)*g - d*e*f*g + d*(pow(f,3) - 2*d*pow(g,2)) +
      c*(pow(d,3) + 3*g*(pow(f,2) + e*g))) +
   7*pow(a,2)*(pow(b,4)*d + pow(e,4)*f - d*pow(e,2)*pow(f,2) +
      2*pow(d,2)*pow(f,3) + pow(c,3)*(2*pow(e,2) - 3*d*f) +
      pow(c,4)*g - 3*d*pow(e,3)*g - 2*pow(d,2)*e*f*g +
      2*pow(d,3)*pow(g,2) + 2*pow(f,2)*pow(g,3) + e*pow(g,4) +
      pow(b,2)*(2*pow(e,3) + 5*d*e*f - c*pow(f,2) - pow(d,2)*g -
         2*c*e*g) + pow(b,3)*(2*pow(c,2) - 3*f*g) -
      pow(c,2)*(pow(d,2)*e + f*pow(g,2)) +
      c*(pow(d,4) + e*f*(-3*pow(f,2) + 5*e*g) +
         d*g*(-2*pow(f,2) + 5*e*g)) +
      b*(-3*pow(d,3)*e + 5*c*pow(d,2)*f - 2*pow(c,2)*e*f + pow(f,4) +
         5*e*pow(f,2)*g - pow(e,2)*pow(g,2) - 3*c*pow(g,3) +
         d*(-2*c*pow(e,2) + 5*pow(c,2)*g - 2*f*pow(g,2)))) -
   7*b*(pow(c,5)*d - pow(d,4)*pow(e,2) + pow(d,5)*f +
      pow(e,3)*pow(f,3) - 2*pow(e,4)*f*g - pow(c,4)*pow(g,2) +
      pow(d,3)*pow(g,3) - pow(f,2)*pow(g,4) + e*pow(g,5) +
      pow(d,2)*f*g*(3*pow(f,2) - 5*e*g) +
      pow(c,3)*(3*e*pow(f,2) + 3*pow(e,2)*g - d*f*g) +
      d*e*(-2*pow(f,4) + 2*e*pow(f,2)*g + 3*pow(e,2)*pow(g,2)) -
      c*(-3*pow(d,2)*pow(e,3) + pow(d,3)*e*f - pow(f,5) +
         2*pow(d,4)*g + e*pow(f,3)*g - 2*pow(e,2)*f*pow(g,2) +
         d*pow(g,2)*(5*pow(f,2) + e*g)) +
      pow(c,2)*(-pow(e,4) - 5*d*pow(e,2)*f + 2*pow(d,2)*e*g +
         f*(pow(d,2)*f + 3*pow(g,3)))) -
   7*a*(pow(b,5)*c - pow(c,4)*pow(d,2) + pow(c,5)*e +
      pow(d,3)*pow(e,3) - 2*pow(d,4)*e*f - pow(e,2)*pow(f,4) +
      d*pow(f,5) + pow(d,5)*g + 3*pow(e,3)*pow(f,2)*g -
      d*e*pow(f,3)*g - pow(e,4)*pow(g,2) - 5*d*pow(e,2)*f*pow(g,2) +
      pow(d,2)*pow(f,2)*pow(g,2) + 3*pow(d,2)*e*pow(g,3) +
      f*pow(g,5) - pow(b,4)*(pow(f,2) + 2*e*g) +
      pow(c,3)*(pow(f,3) - e*f*g + 3*d*pow(g,2)) +
      pow(b,3)*(3*d*pow(e,2) + 3*pow(d,2)*f - c*e*f - c*d*g +
         pow(g,3)) + pow(c,2)*
       (3*pow(e,3)*f - 5*d*e*pow(f,2) + 2*d*pow(e,2)*g -
         g*(5*pow(d,2)*f + pow(g,3))) -
      c*(-2*pow(d,2)*pow(e,2)*f + pow(d,3)*(-3*pow(f,2) + e*g) +
         g*(2*pow(f,4) - 2*e*pow(f,2)*g - 3*pow(e,2)*pow(g,2)) +
         d*(2*pow(e,4) + f*pow(g,3))) +
      pow(b,2)*(-pow(d,4) - 5*c*pow(d,2)*e + pow(c,2)*pow(e,2) +
         3*pow(c,3)*g - 5*c*f*pow(g,2) + e*f*(3*pow(f,2) + 2*e*g) +
         d*(2*pow(c,2)*f + g*(-5*pow(f,2) + 2*e*g))) -
      b*(pow(c,3)*d*e - pow(e,5) + 2*pow(c,4)*f + d*pow(e,3)*f +
         5*pow(d,2)*pow(e,2)*g + e*f*(-2*pow(d,2)*f + pow(g,3)) +
         g*(pow(d,3)*f - 3*pow(f,3)*g + 2*d*pow(g,3)) +
         pow(c,2)*(-3*pow(d,3) + g*(-2*pow(f,2) + 5*e*g)) +
         c*(5*pow(e,2)*pow(f,2) + pow(e,3)*g - 15*d*e*f*g +
            d*(pow(f,3) - 2*d*pow(g,2)))));

  if (result == h*h*h*h*h*h*h) {
    printf("%lld %lld %lld %lld %lld %lld %lld : %lld\n",a,b,c,d,e,f,g,h);
//    return;
  }
}
}
}
}
}
}
}
}
return;
}
