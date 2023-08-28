#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

using namespace std;

#define u8 uint8_t
#define u16 uint16_t
#define u32 uint32_t
#define u64 uint64_t

#define ROTL16(x,r) (((x)<<(r)) | (x>>(16-(r))))
#define ROTR16(x,r) (((x)>>(r)) | ((x)<<(16-(r))))


#define f16(x) ((ROTL16(x,1) & ROTL16(x,8)) ^ ROTL16(x,2)) 
#define R16x2(x,y,k1,k2) (y^=f16(x), y^=k1, x^=f16(y), x^=k2)


void Simon3264KeySchedule(u16 K[], u16 rk[], u16 T);

void Simon3264Encrypt(u16 Pt[],u16 Ct[],u16 rk[], u16 T);