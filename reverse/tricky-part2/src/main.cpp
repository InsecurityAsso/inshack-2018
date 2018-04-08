/*

Crée par Ewen BRUN
ewen.brun@ecam.fr

Pour compiler et packer :
g++ main.cpp -lcrypto -o tricky2 && zip tricky2.zip tricky2

*/


#include <signal.h>
#include <iomanip>
#include <sstream>
#include <cstdlib>
#include "openssl/sha.h"
#include <iostream>
#include <string>

using namespace std;


string sha256(const string str) {
	unsigned char hash[SHA256_DIGEST_LENGTH];
	SHA256_CTX sha256;
	SHA256_Init(&sha256);
	SHA256_Update(&sha256, str.c_str(), str.size());
	SHA256_Final(hash, &sha256);
	stringstream ss;
	for(int i = 0; i < SHA256_DIGEST_LENGTH; i++)
	{
		ss << hex << setw(2) << setfill('0') << (int)hash[i];
	}
	return ss.str();
}

bool check(string str) {
	int ref[52];
	ref[0] = 73;
	ref[1] = 78;
	ref[2] = 83;
	ref[3] = 65;
	ref[4] = 123;
	ref[5] = 89;
	ref[6] = 48;
	ref[7] = 117;
	ref[8] = 95;
	ref[9] = 115;
	ref[10] = 104;
	ref[11] = 48;
	ref[12] = 117;
	ref[13] = 108;
	ref[14] = 100;
	ref[15] = 95;
	ref[16] = 107;
	ref[17] = 110;
	ref[18] = 48;
	ref[19] = 119;
	ref[20] = 95;
	ref[21] = 116;
	ref[22] = 104;
	ref[23] = 52;
	ref[24] = 116;
	ref[25] = 95;
	ref[26] = 49;
	ref[27] = 95;
	ref[28] = 99;
	ref[29] = 52;
	ref[30] = 110;
	ref[31] = 95;
	ref[32] = 116;
	ref[33] = 114;
	ref[34] = 49;
	ref[35] = 99;
	ref[36] = 107;
	ref[37] = 95;
	ref[38] = 121;
	ref[39] = 48;
	ref[40] = 117;
	ref[41] = 114;
	ref[42] = 95;
	ref[43] = 100;
	ref[44] = 51;
	ref[45] = 98;
	ref[46] = 117;
	ref[47] = 103;
	ref[48] = 103;
	ref[49] = 51;
	ref[50] = 114;
	ref[51] = 125;

	for (int i = 0; i < 52; i++) {
		if (str[i] != ref[i]) {
			return false;
		}
	}
	return true;
}

void abort_trap(int s) {
	string pass;
	cout << "Enter password : ";
	cin >> pass;
	if (check(pass)) { // INSA{Y0u_sh0uld_kn0w_th4t_1_c4n_tr1ck_y0ur_d3bugg3r}
		cout << "Congratzs, use the flag to validate" << endl;
	}
	else {
		cout << "Booo\nAre you trying to trick me ?" << endl;
	}
	exit(0);
}


int main() {
	signal(SIGTRAP, abort_trap);
	__asm__ ("int3");
	string pass;
	cout << "Enter password : ";
	cin >> pass;
	if (sha256(pass) == "6b72bdc574f7733a475200c5bbe0323ed6df28d3ff5fa71746aa1d996fac1fcb") { // INSA{Th1s_1s_n0t_th3_fl4g__M1ght_b3_4_wr0ng_w4y!}
		cout << "Well Done... yet !\n";
		return 0;
	} else {
		cout << "Even worse than I thought...\n";
		return 42;
	}
}
