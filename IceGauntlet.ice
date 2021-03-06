module IceGauntlet{

 exception Unauthorized {};
 exception RoomAlreadyExists {};
 exception RoomNotExists {};
 
 interface Authentication {
	string getNewToken(string user, string passwordHash) throws Unauthorized;
	void changePassword(string user,string currentPassHash, string newPassHash) throws Unauthorized;
	bool isValid(string token);
 };
 
 interface GetMap{
	string getRoom() throws RoomNotExists;
 }

 interface GestorMaps{
 	void publish(string token, roomData) throws RoomAlreadyExists;
 	void remove (string token, string roomName)throws Unauthorized;
 };

};
