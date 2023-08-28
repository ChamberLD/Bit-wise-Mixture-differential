/*
 * Quadruple distinguisher verification for SIMON32/64
 * Date: Aug 09, 2023
 * Author: Kexin Qiao
 * Contact: qiao.kexin@bit.edu.cn
*/

#define __USE_MINGW_ANSI_STDIO 1  // to avoid %ll issue. special request for windows
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <string>
#include <math.h>
#include "mpi.h"
#include <iostream>
#include <assert.h>
#include <random>
#include <bitset>
#include "SIMON3264.h"


std::mt19937 gen;
std::uniform_int_distribution<int> dis(0x0,0xffff);

void init_prng_mt(int offset){
    unsigned int initial_seed = 10*time(NULL) + offset;
    gen.seed(initial_seed);
    //printf("[+] PRNG initialized to 0x%08X\n", initial_seed);
}

void genQuadruple(u16 p0[2], u16 p1[2], u16 p2[2], u16 p3[2], u16 md1[2], u16 md2[2], u16 md3[2]){
    p1[0] = p0[0] ^ md1[0]; p1[1] = p0[1] ^ md1[1];
    p2[0] = p0[0] ^ md2[0]; p2[1] = p0[1] ^ md2[1];
    p3[0] = p0[0] ^ md3[0]; p3[1] = p0[1] ^ md3[1];
    
}

bool check_pattern(u16 c0[2], u16 c1[2], u16 c2[2], u16 c3[2], u16 md1[2], u16 md2[2], u16 md3[2]){
    /*
    check if quadruple (c0,c1,c2,c3) satisfy patt.
    */
    bool flag = true;
    //check left side
    if (((c0[1] ^ c1[1]) == md1[1]) and ((c0[1] ^ c2[1]) == md2[1]) and ((c0[1] ^ c3[1]) == md3[1])) {}
    else {
        flag = false;
        return flag;
    }

    //check right side
    if (((c0[0] ^ c1[0]) == md1[0]) and ((c0[0] ^ c2[0]) == md2[0]) and ((c0[0] ^ c3[0]) == md3[0])) {}
    else {
        flag = false;
        return flag;
    }
    return flag;
}
void get_diff_from_pattern(u16 md1[2], u16 md2[2], u16 md3[2], string patt){
    u8 i;
    md1[1] = 0; md1[0] = 0;
    md2[1] = 0; md2[0] = 0;
    md3[1] = 0; md3[0] = 0;
    for (i=0; i<16; i++){ //left side difference
        switch (patt[i]){
            case 's':
                md2[1] ^= (1 << (15 - i)); 
                md3[1] ^= (1 << (15 - i)); 
                break;
            case 'c':
                md1[1] ^= (1 << (15 - i)); 
                md3[1] ^= (1 << (15 - i)); 
                break;
            case 'x':
                md1[1] ^= (1 << (15 - i)); 
                md2[1] ^= (1 << (15 - i)); 
                break;
            default:
                break;
        }
    }

    for (i=0; i<16; i++){ //right side difference
        switch (patt[i+16]){
            case 's':
                md2[0] ^= (1 << (15 - i)); 
                md3[0] ^= (1 << (15 - i)); 
                break;
            case 'c':
                md1[0] ^= (1 << (15 - i)); 
                md3[0] ^= (1 << (15 - i)); 
                break;
            case 'x':
                md1[0] ^= (1 << (15 - i)); 
                md2[0] ^= (1 << (15 - i)); 
                break;
            default:
                break;
        }
    }
}
u64 * quadruple(u8 rd, u16 k[32], string inpatt, string outpatt){
    /*
    Construct all quadruples in inpatt under fixed roundkey.
    Return the number of right quadruples satisfying outpatt.
    */
    u16 in1[2], in2[2], in3[2];
    u16 out1[2], out2[2], out3[2];

    get_diff_from_pattern(in1, in2, in3, inpatt);
    get_diff_from_pattern(out1, out2, out3, outpatt);
    /*
    cout << "in1 " << bitset<16>(in1[1]) << bitset<16>(in1[0])<<endl;
    cout << "in2 " << bitset<16>(in2[1]) << bitset<16>(in2[0])<<endl;
    cout << "in3 " << bitset<16>(in3[1]) << bitset<16>(in3[0])<<endl;
    cout << "out1 " << bitset<16>(out1[1]) << bitset<16>(out1[0])<<endl;
    cout << "out2 " << bitset<16>(out2[1]) << bitset<16>(out2[0])<<endl;
    cout << "out3 " << bitset<16>(out3[1]) << bitset<16>(out3[0])<<endl;
    */
    u16 p0[2], p1[2], p2[2], p3[2];
    u16 c0[2], c1[2], c2[2], c3[2];

    
    static u64 count[2];
    count[0] = 0;
    count[1] = 0;

    for (u32 itr1 = 0; itr1 < (1<<16); itr1++){
        p0[1] = itr1 & 0xffff;
        for (u32 itr0 = 0; itr0 < (1<<16); itr0++){ //enumerate all plaintexts
            p0[0] = itr0 & 0xffff;
            genQuadruple(p0, p1, p2, p3, in1, in2, in3);
            //cout << "p0 " << bitset<16>(p0[1]) << bitset<16>(p0[0])<<endl;
            //cout << "p1 " << bitset<16>(p1[1]) << bitset<16>(p1[0])<<endl;
            //cout << "p2 " << bitset<16>(p2[1]) << bitset<16>(p2[0])<<endl;
            //cout << "p3 " << bitset<16>(p3[1]) << bitset<16>(p3[0])<<endl;
            Simon3264Encrypt(p0, c0, k, rd);
            Simon3264Encrypt(p1, c1, k, rd);
            Simon3264Encrypt(p2, c2, k, rd);
            Simon3264Encrypt(p3, c3, k, rd);

            //cout << "c0 " << bitset<16>(c0[1]) << bitset<16>(c0[0])<<endl;
            //cout << "c1 " << bitset<16>(c1[1]) << bitset<16>(c1[0])<<endl;
            //cout << "c2 " << bitset<16>(c2[1]) << bitset<16>(c2[0])<<endl;
            //cout << "c3 " << bitset<16>(c3[1]) << bitset<16>(c3[0])<<endl;

            if (check_pattern(c0, c1, c2, c3, out1, out2, out3))
                count[0]++;

            Simon3264Encrypt(p0, c0, k, 32);
            Simon3264Encrypt(p1, c1, k, 32);
            Simon3264Encrypt(p2, c2, k, 32);
            Simon3264Encrypt(p3, c3, k, 32);

            if (check_pattern(c0, c1, c2, c3, out1, out2, out3))
                count[1]++;

        }
    }

    return count;
}

u64 * testOnMultKey(u8 rd, u64 N2, string inpatt, string outpatt){
    /*
    Set N2 multi masterkeys. Under each masterkey, test on N3 quadruples.
    Return sum of right quadruple numbers under each key.
    */
    u16 mk[2];
    u16 rk[32];
    static u64 count[2];
    u64 *count_itr;
    u64 bnum = 0;
    count[0] = 0;
    count[1] = 0;
    while (bnum < N2){
        bnum++;
        //generate a random key
        mk[0] = dis(gen);
        mk[1] = dis(gen);

        Simon3264KeySchedule(mk, rk, 32);
        count_itr = quadruple(rd, rk, inpatt, outpatt);
        count[0] += *count_itr;
        count[1] += *(count_itr + 1);
    }
    return count;
}
int main(int argc, char** argv){
    u64 N2 = 1<<2; //each process try N2 keys
    
    u8 rd = 9;
    string inpatt = "---c---c-------x-s---x-------x-c";
    string outpatt = "-x---s-------s-----c---c-------s";
   /*
    u8 rd = 7;
    string inpatt = "-s---c---------xs--x---------x-s";
    string outpatt = "---x---x-------c-c---s----------";
    */
    /*
    For each processor, run 
    testOnMultKey(u8 rd, u64 N2, string inpatt, string outpatt):
    Set N2 multi masterkeys. Under each masterkey, test on all quadruples.
    Return sum of right quadruple numbers under each key.
    */
    MPI_Init(NULL, NULL);
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    printf("\n[+] Proc %d\n", world_rank);
    init_prng_mt(world_rank);
    //Compute on each process
    u64 *count;
    
    clock_t clock_timer;
    clock_timer = clock();
    
    MPI_Barrier(MPI_COMM_WORLD);
    
    
    //init_prng_mt(world_rank);
    double proc_time;
    
    proc_time = MPI_Wtime();
    count = testOnMultKey(rd,N2,inpatt,outpatt);
    proc_time = MPI_Wtime() - proc_time;

    MPI_Barrier(MPI_COMM_WORLD);
    //Gather all number of right quadruples down to the root process
    u64 *NUM = NULL;
    if (world_rank == 0){
        NUM = (u64 *)malloc(world_size * sizeof(u64) * 2);
        assert(NUM != NULL);
    }

    MPI_Gather(count, 2, MPI_UNSIGNED_LONG_LONG, NUM, 2, MPI_UNSIGNED_LONG_LONG,0,MPI_COMM_WORLD);

    //Compute sum on the root process
    if (world_rank == 0){
        u64 right,rand_right;
        right = 0;
        rand_right = 0;
        printf("\n Quaries on each process = 2^(%f)\n",log(N2)/log(2)+30); //actually 2^30 unique quadruples
        for (int i = 0; i < world_size *2; i=i+2){
            
            right += *(NUM + i);
            rand_right += *(NUM + i + 1);
            printf(" %d proc:     Right = 2^(%f)\n", i/2, log(*(NUM + i)/4)/log(2)); //divide 4 to remove repeats
            printf(" %d proc: randRight = 2^(%f)\n", i/2, log(*(NUM + i + 1)/4)/log(2));//divide 4 to remove repeats
        }
        printf("\n                              Total queries = 2^(%f) \n", log(N2 * world_size)/log(2)+30);
        printf("SIMON32:     Number of total right quadruples = 2^(%f)\n", log(right/4)/log(2));//divide 4 to remove repeats
        printf("           Probability of right quadruples  = 2^(-%0.4f)\n", log(N2 *  world_size)/log(2)+30-log(right/4)/log(2));
        printf(" RandPerm: Number of total right quadruples = 2^(%f)\n", log(rand_right/4)/log(2));
        printf("            Probability of right quadruples = 2^(-%0.4f)\n", log(N2  * world_size)/log(2)+30-log(rand_right/4)/log(2));
        cout << " time on clock(): " << ((double)clock() - clock_timer) / CLOCKS_PER_SEC<<endl<<endl;
    }

    
    printf("[+] Time : %lf\n",proc_time);
    printf("[+] SIMON32:         Number of right quadruples = 2^(%f)\n", log(*count)/log(2));
    printf("[+]           Probability of right quadruples = 2^(-%0.4f)\n\n", log(N2 )/log(2)+32-log(*count)/log(2));
    printf("[+] RandPerm:      Number of right quadruples = 2^(%f)\n", log(*(count+1))/log(2));
    printf("[+]           Probability of right quadruples = 2^(-%0.4f)\n\n", log(N2)/log(2)+32-log(*(count+1))/log(2));

    //Clean up
    if (world_rank == 0){
        free(NUM);
    }
    
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Finalize();
    return 0;
}
