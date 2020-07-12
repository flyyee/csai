#include "MemoryManager.h"
#include <iostream>
#include <vector>
#include <thread>
#include <fstream>
#include <string>

MemoryManager* Mem;
// offsets
#define dwLocalPlayer 0xD3DBEC
#define m_iTeamNum 0xF4
#define dwEntityList 0x4D523EC

#define m_angEyeAnglesX 0xB37C
#define m_angEyeAnglesY 0xB380
#define m_vecOrigin 0x138

#define m_bSpotted 0x93D
#define m_iTeamNum 0xF4
#define m_bBombPlanted 0x99D

#define m_szLastPlaceName 0x35B4
#define dwGameRulesProxy 0x526F38C
#define m_bFreezePeriod 0x20

#define dwClientState 0x58ADD4
#define dwClientState_ViewAngles 0x4D88

const std::string inputFN = "com.txt"; // file to communicate between ai and csgo helper

// player information structure, for obtaining specific information from a region in memory
struct player_info_t
{
	int64_t __pad0;
	union {
		int64_t xuid;
		struct {
			int xuidlow;
			int xuidhigh;
		};
	};
	char name[128];
	int userid;
	char guid[33];
	unsigned int friendsid;
	char friendsname[128];
	bool fakeplayer;
	bool ishltv;
	unsigned int customfiles[4];
	unsigned char filesdownloaded;
};

struct Spot { // structure representing an occurrence of spotting a player
	long int tick;
	float posX, posY, posZ;
	wchar_t* uid;
};

struct Vec3 {
	float x, y, z;
};

void MoveXhair(float endPitch, float endYaw) { // moves player crosshair
	Sleep(1000);
	std::cout << "Moving Xhair..." << std::endl;
	bool stop = false;
	const float pitchSpeed = 0.2, yawSpeed = 0.2; // in degrees/ms
	// obtains time for measuring speeds and performing stop conditions
	DWORD startTime = GetTickCount();
	DWORD currentTimePitch, startTimePitch = GetTickCount();
	DWORD previousTimePitch = startTimePitch;
	DWORD currentTimeYaw, startTimeYaw = GetTickCount();
	DWORD previousTimeYaw = startTimeYaw;
	DWORD LocalPlayer_Base = Mem->Read<DWORD>(Mem->ClientDLL_Base + dwLocalPlayer); // information about the current player
	DWORD clientState = Mem->Read<DWORD>(Mem->EngineDLL_Base + dwClientState); // modifiable variables for the current player

	float myEyePitch = Mem->Read<float>(LocalPlayer_Base + m_angEyeAnglesX);
	float myEyeYaw = Mem->Read<float>(LocalPlayer_Base + m_angEyeAnglesY);
	int pitchDirection = 0, yawDirection = 0; // determines the direction in which to move the crosshair
	bool pitchComplete = false, yawComplete = false; // whether the movement is complete
	Vec3 eyeVec;
	eyeVec.x = myEyePitch, eyeVec.y = myEyeYaw, eyeVec.z = 0;

	if (myEyePitch == endPitch) {
		pitchComplete = true;
	}
	if (myEyeYaw == endYaw) {
		yawComplete = true;
	}
	if (myEyePitch > 90) {
		// converts pitch to range -90 to 90
		myEyePitch -= 360;
	}
	if (endPitch > 90) {
		endPitch -= 360;
	}
	if (myEyePitch > endPitch) {
		pitchDirection = -1;
	}
	else {
		pitchDirection = 1;
	}

	// yaw in range 0 to 360
	if (myEyeYaw > endYaw) {
		if ((myEyeYaw - endYaw) > 180) {
			yawDirection = -1;
		}
		else {
			yawDirection = 1;
		}
	}
	else {
		if ((endYaw - myEyeYaw) > 180) {
			yawDirection = 1;
		}
		else {
			yawDirection = -1;
		}
	}

	while (!pitchComplete || !yawComplete) {
		if ((GetTickCount() - startTime) > 3000) {
			// more than 3s elapsed since crosshair started moving
			break;
		}
		LocalPlayer_Base = Mem->Read<DWORD>(Mem->ClientDLL_Base + dwLocalPlayer);
		currentTimePitch = GetTickCount();
		
		if (!pitchComplete) {
			if (pitchDirection == -1) {
				if (myEyePitch <= endPitch) {
					pitchComplete = true;
				}
			}
			else {
				if (myEyePitch >= endPitch) {
					pitchComplete = true;
				}
			}
			myEyePitch += (currentTimePitch - previousTimePitch) * pitchSpeed * pitchDirection;
			if (myEyePitch > 89) {
				myEyePitch = 89;
				pitchComplete = true;
			}
			else if (myEyePitch < -89) {
				myEyePitch = -89;
				pitchComplete = true;
			}
			clientState = Mem->Read<DWORD>(Mem->EngineDLL_Base + dwClientState);
			eyeVec.x = myEyePitch;
		}
		previousTimePitch = currentTimePitch;

		currentTimeYaw = GetTickCount();
		if (!yawComplete) {
			if (yawDirection == 1) {
				// clockwise
				if (myEyeYaw < 0) {
					if ((myEyeYaw + 360) < endYaw) {
						if ((endYaw - myEyeYaw - 360) < 90) {
							yawComplete = true;
						}
					}
				}
				else {
					if (myEyeYaw < endYaw) {
						if ((endYaw - myEyeYaw) < 90) {
							yawComplete = true;
						}
					}
				}
			}
			else {
				// anticlockwise
				if (myEyeYaw < 0) {
					if ((myEyeYaw + 360) > endYaw) {
						if ((myEyeYaw + 360 - endYaw) < 90) {
							yawComplete = true;
						}
					}
				}
				else {
					if (myEyeYaw > endYaw) {
						if ((myEyeYaw  - endYaw) < 90) {
							yawComplete = true;
						}
					}
				}
			}
			myEyeYaw += (currentTimeYaw - previousTimeYaw) * yawSpeed * (-yawDirection);
			if (myEyeYaw < 0) {
				// modulo check
				myEyeYaw += 360;
			}
			if (myEyeYaw >= 360) {
				myEyeYaw -= 360;
			}
			if (myEyeYaw > 180) {
				myEyeYaw -= 360;
			}
			eyeVec.y = myEyeYaw;
		}
		previousTimeYaw = currentTimeYaw;
		Mem->Write<Vec3>(clientState + dwClientState_ViewAngles, eyeVec); // writes to game memory
	}
	
}

// writes the game state to the shared file with the ai
void SendInfo(const unsigned long long startTime, std::vector<Spot> &spottedList, bool &stopFlag) {
	DWORD LocalPlayer_Base, Grp_Base;
	int myTeamId;
	float myEyePitch, myEyeYaw;
	float myPosX, myPosY, myPosZ;
	DWORD currentTime;
	int currentTick;
	bool bombPlanted, hold;
	long long lastOutputTime = 0;

	while(!stopFlag) {
		if (GetAsyncKeyState(VK_F5)) {
			//Retrieve player information
			LocalPlayer_Base = Mem->Read<DWORD>(Mem->ClientDLL_Base + dwLocalPlayer);
			myTeamId = Mem->Read<int>(LocalPlayer_Base + m_iTeamNum);
			myEyePitch = Mem->Read<float>(LocalPlayer_Base + m_angEyeAnglesX);
			myEyeYaw = Mem->Read<float>(LocalPlayer_Base + m_angEyeAnglesY);
			myPosX = Mem->Read<float>(LocalPlayer_Base + m_vecOrigin);
			myPosY = Mem->Read<float>(LocalPlayer_Base + m_vecOrigin + 0x4);
			myPosZ = Mem->Read<float>(LocalPlayer_Base + m_vecOrigin + 0x8);
			std::cout << "Eye angles: " << myEyePitch << " " << myEyeYaw << std::endl;
			std::cout << "Position: " << myPosX << " " << myPosY << " " << myPosZ << std::endl;

			currentTime = GetTickCount() - startTime;
			currentTick = currentTime / 1000 * 64;

			std::cout << "Current tick: " << currentTick << std::endl;

			Grp_Base = Mem->Read<DWORD>(Mem->ClientDLL_Base + dwGameRulesProxy);
			bombPlanted = Mem->Read<bool>(Grp_Base + m_bBombPlanted);
			hold = false;
			if (myTeamId == 2) {
				// terrorist
				hold = (bombPlanted ? true : false);
			}
			else if (myTeamId == 3) {
				// CT
				std::cout << bombPlanted;
				hold = (bombPlanted ? false : true);
			}

			std::cout << "Hold: " << (hold ? "yes" : "no");

			std::cout << "Spotted list: " << std::endl;
			for (auto& spot : spottedList) {
				std::cout << "Tick " << spot.tick << ": " << spot.posX << "," << spot.posY << "," << spot.posZ << " ->" << spot.uid << std::endl;
			}

			std::string fileInput = "\n";
			fileInput += "input," + std::to_string(currentTick) + ",";
			fileInput += std::to_string(currentTick) + "," + std::to_string(myPosX) + "," + std::to_string(myPosY) + "," + std::to_string(myPosZ) + ",";
			fileInput += std::to_string(myEyePitch) + "," + std::to_string(myEyeYaw) + ",spotted" + std::to_string(spottedList.size()) + ",hold" + (hold ? "1" : "0");
			
			for (auto& spot : spottedList) {
				fileInput += "," + std::to_string(spot.posX) + "," + std::to_string(spot.posY) + "," + std::to_string(spot.posZ) + "," + std::to_string(spot.tick);
			}
			fileInput += "\n";
			std::cout << fileInput << std::endl;

			std::fstream myfile;
			myfile.open(inputFN, std::ios_base::app);
			myfile << fileInput;
			myfile.close();
			// write to file the input to the ai
			
			for (int pollFileCount = 0; pollFileCount < 15; pollFileCount++) {
				// continuously polls the file for 3 seconds to receive the output from the ai
				std::fstream myfile2;
				myfile2.open(inputFN);

				// reads the last line of the file
				myfile2.seekg(-1, std::ios_base::end);
				bool keepLooping = true;
				while (keepLooping) {
					char ch;
					myfile2.get(ch);
					if ((int)myfile2.tellg() <= 1) {
						myfile2.seekg(0);
						keepLooping = false;
					}
					else if (ch == '\n') {
						keepLooping = false;
					}
					else {
						myfile2.seekg(-2, std::ios_base::cur);
					}
				}

				std::string lastLine;
				std::getline(myfile2, lastLine);
				myfile2.close();
				
				int linePos1 = 0, linePos2 = 0;
				float outputPitch, outputYaw;
				linePos2 = lastLine.find(",");
				std::cout << lastLine << std::endl;
				if (lastLine.substr(linePos1, linePos2) == "output") { // checks if line type is output
					linePos1 = linePos2+1;
					linePos2 = lastLine.find(",");
					int newOutputTime = std::stoll(lastLine.substr(linePos1, linePos2 - linePos1));
					if (newOutputTime > lastOutputTime) { // checks if line was written after the last previous read
						lastOutputTime = newOutputTime;
						linePos1 = linePos2+1;
						linePos2 = lastLine.find(",");
						outputPitch = std::stof(lastLine.substr(linePos1, linePos2 - linePos1));
						linePos1 = linePos2+1;
						outputYaw = std::stof(lastLine.substr(linePos1, lastLine.length() - linePos1));
						MoveXhair(outputPitch, outputYaw);
						break;
					}
				}

				Sleep(200);
			}
			Sleep(200);
		}
		Sleep(10);
	}
}

void GetStats() { // records the instantaneous state of the game and 
	std::vector<Spot> spottedList(0); // list of spotted players
	const unsigned long long startTime = GetTickCount();
	bool stopFlag = false;
	// creates a thread to wait for key press to activate the ai
	std::thread tSendInfo(SendInfo, startTime, std::ref(spottedList), std::ref(stopFlag)); 

	const int tickrate = 64;
	DWORD LocalPlayer_Base, Grp_Base;
	int myTeamId;
	bool freezetime;
	std::cout << "Started recording stats..." << std::endl;
	while (true) {
		LocalPlayer_Base = Mem->Read<DWORD>(Mem->ClientDLL_Base + dwLocalPlayer);

		myTeamId = Mem->Read<int>(LocalPlayer_Base + m_iTeamNum);

		Grp_Base = Mem->Read<DWORD>(Mem->ClientDLL_Base + dwGameRulesProxy);
		freezetime = Mem->Read<bool>(Grp_Base + m_bFreezePeriod);
		if (freezetime) {
			// round over
			spottedList.clear();
		}

		for (int i = 1; i < 64; i++) {
			// iterates over all entities in the list, includes players
			DWORD playerBase = Mem->Read<DWORD>(Mem->ClientDLL_Base + dwEntityList + (i * 0x10));
			if (!playerBase) continue;

			int playerTeamId = Mem->Read<int>(playerBase + m_iTeamNum);
			if (playerTeamId != 2 && playerTeamId != 3) continue; // checks if the entity is a valid player

			wchar_t* playerLastPlace = Mem->Read<wchar_t*>(playerBase + m_szLastPlaceName); // reads the player's last position's name
			
			if (playerTeamId != myTeamId) { // player not on user's team
				bool spotted = Mem->Read<bool>(playerBase + m_bSpotted);
				if (spotted) {
					Spot newSpot;
					newSpot.posX = Mem->Read<float>(playerBase + m_vecOrigin);
					newSpot.posY = Mem->Read<float>(playerBase + m_vecOrigin + 0x4);
					newSpot.posZ = Mem->Read<float>(playerBase + m_vecOrigin + 0x8);
					newSpot.posZ += 64.06;

					auto currentTime = GetTickCount();
					currentTime -= startTime;
					newSpot.tick = currentTime / 1000 * 64;;
					newSpot.uid = Mem->Read<wchar_t*>(playerBase + m_szLastPlaceName);

					// merges duplicate spots
					for (int x = spottedList.size()-1; x >= 0; x--) {
						if (newSpot.tick - spottedList[x].tick < 256) {
							// spot occurred <256ticks (4s) before current spot
							if (spottedList[x].uid == newSpot.uid) {
								spottedList.erase(spottedList.begin() + x);
								break;
							}
						}
						else {
							break;
						}
					}
					spottedList.push_back(newSpot);
				}
			}
		}
	}
	stopFlag = true;
	tSendInfo.join();
}

int main()
{
	Mem = new MemoryManager();
	std::cout << "CSAI started :^D" << std::endl;
	GetStats();
	delete Mem;
	return 0;
}