
#include "SIMON3264.h"

void Simon3264KeySchedule(u16 K[], u16 rk[], u16 T){
    u16 i;
    u16 c = 0xfffc;
    u64 z = 0b11111010001001010110000111001101111101000100101011000011100110;

    rk[0]=K[0]; rk[1]=K[1]; rk[2]=K[2]; rk[3]=K[3];
    for (i = 4; i < T; i++){
        rk[i]=c^((z >> ((61 - (i-4) % 62))) &1)^rk[i-4]^ROTR16(rk[i-1],3)^rk[i-3] ^ROTR16(rk[i-1],4)^ROTR16(rk[i-3],1); 
        
    }
}

void Simon3264Encrypt(u16 Pt[],u16 Ct[],u16 rk[], u16 T) { 
    u16 i, tmp; 
    Ct[1]=Pt[1]; Ct[0]=Pt[0]; 
    for(i=0;i<(T/2)*2;i+=2 ) R16x2(Ct[1],Ct[0],rk[i],rk[i+1]); 
    if (T%2) {
        tmp = Ct[1];
        Ct[1] = Ct[0] ^ (ROTL16(Ct[1],1) & ROTL16(Ct[1],8))^ ROTL16(Ct[1], 2) ^ rk[T-1];
        Ct[0] = tmp;
    }
}

