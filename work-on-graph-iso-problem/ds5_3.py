def ds5_3(values):
  r11,r12,r13,r14,r15,r21,r22,r23,r24,r25,r31,r32,r33,r34,r35,r41,r42,r43,r44,r45,r51,r52,r53,r54,r55 = values
  return (-r11*r21*r31*r42*r53 + -r11*r21*r31*r43*r52 + -r11*r21*r32*r41*r53 + -r11*r21*r32*r43*r51 + -r11*r21*r33*r41*r52
  + -r11*r21*r33*r42*r51 + -r11*r22*r31*r41*r53 + -r11*r22*r31*r43*r51 + -r11*r22*r32*r42*r53 + -r11*r22*r32*r43*r52
  + -r11*r22*r33*r41*r51 + -r11*r22*r33*r42*r52 + -r11*r22*r33*r43*r53 + -r11*r23*r31*r41*r52 + -r11*r23*r31*r42*r51
  + -r11*r23*r32*r41*r51 + -r11*r23*r32*r42*r52 + -r11*r23*r32*r43*r53 + -r11*r23*r33*r42*r53 + -r11*r23*r33*r43*r52
  + -r12*r21*r31*r41*r53 + -r12*r21*r31*r43*r51 + -r12*r21*r32*r42*r53 + -r12*r21*r32*r43*r52 + -r12*r21*r33*r41*r51
  + -r12*r21*r33*r42*r52 + -r12*r21*r33*r43*r53 + -r12*r22*r31*r42*r53 + -r12*r22*r31*r43*r52 + -r12*r22*r32*r41*r53
  + -r12*r22*r32*r43*r51 + -r12*r22*r33*r41*r52 + -r12*r22*r33*r42*r51 + -r12*r23*r31*r41*r51 + -r12*r23*r31*r42*r52
  + -r12*r23*r31*r43*r53 + -r12*r23*r32*r41*r52 + -r12*r23*r32*r42*r51 + -r12*r23*r33*r41*r53 + -r12*r23*r33*r43*r51
  + -r13*r21*r31*r41*r52 + -r13*r21*r31*r42*r51 + -r13*r21*r32*r41*r51 + -r13*r21*r32*r42*r52 + -r13*r21*r32*r43*r53
  + -r13*r21*r33*r42*r53 + -r13*r21*r33*r43*r52 + -r13*r22*r31*r41*r51 + -r13*r22*r31*r42*r52 + -r13*r22*r31*r43*r53
  + -r13*r22*r32*r41*r52 + -r13*r22*r32*r42*r51 + -r13*r22*r33*r41*r53 + -r13*r22*r33*r43*r51 + -r13*r23*r31*r42*r53
  + -r13*r23*r31*r43*r52 + -r13*r23*r32*r41*r53 + -r13*r23*r32*r43*r51 + -r13*r23*r33*r41*r52 + -r13*r23*r33*r42*r51
  + -4*r11*r21*r32*r42*r53 + -4*r11*r21*r32*r43*r52 + -4*r11*r21*r32*r43*r53 + -4*r11*r21*r33*r42*r52 + -4*r11*r21*r33*r42*r53
  + -4*r11*r21*r33*r43*r52 + -4*r11*r22*r31*r42*r53 + -4*r11*r22*r31*r43*r52 + -4*r11*r22*r31*r43*r53 + -4*r11*r22*r32*r41*r53
  + -4*r11*r22*r32*r43*r51 + -4*r11*r22*r32*r43*r53 + -4*r11*r22*r33*r41*r52 + -4*r11*r22*r33*r41*r53 + -4*r11*r22*r33*r42*r51
  + -4*r11*r22*r33*r42*r53 + -4*r11*r22*r33*r43*r51 + -4*r11*r22*r33*r43*r52 + -4*r11*r23*r31*r42*r52 + -4*r11*r23*r31*r42*r53
  + -4*r11*r23*r31*r43*r52 + -4*r11*r23*r32*r41*r52 + -4*r11*r23*r32*r41*r53 + -4*r11*r23*r32*r42*r51 + -4*r11*r23*r32*r42*r53
  + -4*r11*r23*r32*r43*r51 + -4*r11*r23*r32*r43*r52 + -4*r11*r23*r33*r41*r52 + -4*r11*r23*r33*r42*r51 + -4*r11*r23*r33*r42*r52
  + -4*r12*r21*r31*r42*r53 + -4*r12*r21*r31*r43*r52 + -4*r12*r21*r31*r43*r53 + -4*r12*r21*r32*r41*r53 + -4*r12*r21*r32*r43*r51
  + -4*r12*r21*r32*r43*r53 + -4*r12*r21*r33*r41*r52 + -4*r12*r21*r33*r41*r53 + -4*r12*r21*r33*r42*r51 + -4*r12*r21*r33*r42*r53
  + -4*r12*r21*r33*r43*r51 + -4*r12*r21*r33*r43*r52 + -4*r12*r22*r31*r41*r53 + -4*r12*r22*r31*r43*r51 + -4*r12*r22*r31*r43*r53
  + -4*r12*r22*r33*r41*r51 + -4*r12*r22*r33*r41*r53 + -4*r12*r22*r33*r43*r51 + -4*r12*r23*r31*r41*r52 + -4*r12*r23*r31*r41*r53
  + -4*r12*r23*r31*r42*r51 + -4*r12*r23*r31*r42*r53 + -4*r12*r23*r31*r43*r51 + -4*r12*r23*r31*r43*r52 + -4*r12*r23*r32*r41*r51
  + -4*r12*r23*r32*r41*r53 + -4*r12*r23*r32*r43*r51 + -4*r12*r23*r33*r41*r51 + -4*r12*r23*r33*r41*r52 + -4*r12*r23*r33*r42*r51
  + -4*r13*r21*r31*r42*r52 + -4*r13*r21*r31*r42*r53 + -4*r13*r21*r31*r43*r52 + -4*r13*r21*r32*r41*r52 + -4*r13*r21*r32*r41*r53
  + -4*r13*r21*r32*r42*r51 + -4*r13*r21*r32*r42*r53 + -4*r13*r21*r32*r43*r51 + -4*r13*r21*r32*r43*r52 + -4*r13*r21*r33*r41*r52
  + -4*r13*r21*r33*r42*r51 + -4*r13*r21*r33*r42*r52 + -4*r13*r22*r31*r41*r52 + -4*r13*r22*r31*r41*r53 + -4*r13*r22*r31*r42*r51
  + -4*r13*r22*r31*r42*r53 + -4*r13*r22*r31*r43*r51 + -4*r13*r22*r31*r43*r52 + -4*r13*r22*r32*r41*r51 + -4*r13*r22*r32*r41*r53
  + -4*r13*r22*r32*r43*r51 + -4*r13*r22*r33*r41*r51 + -4*r13*r22*r33*r41*r52 + -4*r13*r22*r33*r42*r51 + -4*r13*r23*r31*r41*r52
  + -4*r13*r23*r31*r42*r51 + -4*r13*r23*r31*r42*r52 + -4*r13*r23*r32*r41*r51 + -4*r13*r23*r32*r41*r52 + -4*r13*r23*r32*r42*r51
  + 2*r11*r21*r31*r42*r52 + 2*r11*r21*r31*r43*r53 + 2*r11*r21*r32*r41*r52 + 2*r11*r21*r32*r42*r51 + 2*r11*r21*r32*r42*r52
  + 2*r11*r21*r33*r41*r53 + 2*r11*r21*r33*r43*r51 + 2*r11*r21*r33*r43*r53 + 2*r11*r22*r31*r41*r52 + 2*r11*r22*r31*r42*r51
  + 2*r11*r22*r31*r42*r52 + 2*r11*r22*r32*r41*r51 + 2*r11*r22*r32*r41*r52 + 2*r11*r22*r32*r42*r51 + 2*r11*r23*r31*r41*r53
  + 2*r11*r23*r31*r43*r51 + 2*r11*r23*r31*r43*r53 + 2*r11*r23*r33*r41*r51 + 2*r11*r23*r33*r41*r53 + 2*r11*r23*r33*r43*r51
  + 2*r12*r21*r31*r41*r52 + 2*r12*r21*r31*r42*r51 + 2*r12*r21*r31*r42*r52 + 2*r12*r21*r32*r41*r51 + 2*r12*r21*r32*r41*r52
  + 2*r12*r21*r32*r42*r51 + 2*r12*r22*r31*r41*r51 + 2*r12*r22*r31*r41*r52 + 2*r12*r22*r31*r42*r51 + 2*r12*r22*r32*r41*r51
  + 2*r12*r22*r32*r43*r53 + 2*r12*r22*r33*r42*r53 + 2*r12*r22*r33*r43*r52 + 2*r12*r22*r33*r43*r53 + 2*r12*r23*r32*r42*r53
  + 2*r12*r23*r32*r43*r52 + 2*r12*r23*r32*r43*r53 + 2*r12*r23*r33*r42*r52 + 2*r12*r23*r33*r42*r53 + 2*r12*r23*r33*r43*r52
  + 2*r13*r21*r31*r41*r53 + 2*r13*r21*r31*r43*r51 + 2*r13*r21*r31*r43*r53 + 2*r13*r21*r33*r41*r51 + 2*r13*r21*r33*r41*r53
  + 2*r13*r21*r33*r43*r51 + 2*r13*r22*r32*r42*r53 + 2*r13*r22*r32*r43*r52 + 2*r13*r22*r32*r43*r53 + 2*r13*r22*r33*r42*r52
  + 2*r13*r22*r33*r42*r53 + 2*r13*r22*r33*r43*r52 + 2*r13*r23*r31*r41*r51 + 2*r13*r23*r31*r41*r53 + 2*r13*r23*r31*r43*r51
  + 2*r13*r23*r32*r42*r52 + 2*r13*r23*r32*r42*r53 + 2*r13*r23*r32*r43*r52 + 2*r13*r23*r33*r41*r51 + 2*r13*r23*r33*r42*r52
  + 8*r11*r21*r31*r41*r52 + 8*r11*r21*r31*r41*r53 + 8*r11*r21*r31*r42*r51 + 8*r11*r21*r31*r43*r51 + 8*r11*r21*r32*r41*r51
  + 8*r11*r21*r33*r41*r51 + 8*r11*r22*r31*r41*r51 + 8*r11*r22*r32*r42*r52 + 8*r11*r23*r31*r41*r51 + 8*r11*r23*r33*r43*r53
  + 8*r12*r21*r31*r41*r51 + 8*r12*r21*r32*r42*r52 + 8*r12*r22*r31*r42*r52 + 8*r12*r22*r32*r41*r52 + 8*r12*r22*r32*r42*r51
  + 8*r12*r22*r32*r42*r53 + 8*r12*r22*r32*r43*r52 + 8*r12*r22*r33*r42*r52 + 8*r12*r23*r32*r42*r52 + 8*r12*r23*r33*r43*r53
  + 8*r13*r21*r31*r41*r51 + 8*r13*r21*r33*r43*r53 + 8*r13*r22*r32*r42*r52 + 8*r13*r22*r33*r43*r53 + 8*r13*r23*r31*r43*r53
  + 8*r13*r23*r32*r43*r53 + 8*r13*r23*r33*r41*r53 + 8*r13*r23*r33*r42*r53 + 8*r13*r23*r33*r43*r51 + 8*r13*r23*r33*r43*r52
  + 20*r11*r21*r31*r41*r51 + 20*r12*r22*r32*r42*r52 + 20*r13*r23*r33*r43*r53 + 20*r14*r24*r34*r44*r54 + 20*r15*r25*r35*r45*r55
  + 0 )