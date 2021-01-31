module IceGauntlet{

    exception Unauthorized {};
    exception RoomAlreadyExists {};
    exception RoomNotExists {};
 
    interface Authentication{
        void changePassword(string user, string currentPassHash, string newPassHash) throws Unauthorized;
        string getNewToken(string user, string passwordHash) throws Unauthorized;
        string getOwner(string token) throws Unauthorized;
    };
 
    interface ObtenerMapa{
        string getRoom() throws RoomNotExists;
    };

    interface GestorMapas{
        void publish(string token, string roomData) throws 	RoomAlreadyExists;
        void remove (string token, string roomName)throws Unauthorized;
    };

};
