// CamSimDummyApp.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
using namespace std;

int main(int argc, char* argv[])
{
	cout << "CamSim app called successfully with " << argc << " args" << endl;

	//argv[0] will contain the name and path of the app used to call the app
	for(int i = 0;  i < argc; i++) {
		cout << "Recieved argument " << i << ": " << argv[i] << endl;
	}
	return 0;
}

