/*

Crée par Ewen BRUN
ewen.brun@ecam.fr

Pour compiler et packer:
g++ main.cpp -o tricky1 && zip tricky1.zip tricky1

*/


#include <signal.h>
#include <sys/ptrace.h>
#include <iostream>
#include <string>

using namespace std;


string base = "\x0e\n\x11\x06?\x01\x1f\x1c\x1dv7\x1d/p0#w0\x18\"r5\x1b" "13p6v\'\x1ds*v+u1>7\x1d" "0,q)\x1b&t&7 #q5\x1b$su.49";

string stack_check() {
	string key = "GDB";
	for (int i = 0; i < base.size(); i++) {
		base[i] ^= key[i%key.size()];
	}
	return base;
}


int main() {
	if (ptrace(PTRACE_TRACEME, 0, 1, 0) < 0) {
		cout << "Oh no, don't debug me plz\n";
		return 42;
	} else {
		string pass;
		cout << "Enter your flag : ";
		cin >> pass;
		if (pass == stack_check()) { // INSA{CXX_1s_h4rd3r_f0r_st4t1c_4n4l1sys_wh3n_d3bugg3r_f41ls}
			cout << "Correct but this is just the first one\nValidate with the flag" << endl;
		}
		else {
			cout << "Sooo bad. Are you trying to trick me ?" << endl;
		}
		return 0;
	}
}
