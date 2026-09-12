using System.Data.SqlClient;

namespace DemoApp
{
    public class UserRepository
    {
        public SqlDataReader FindByName(SqlConnection connection, string userName)
        {
            // Deliberately vulnerable (SQL injection) - this file exists only to give the SR SAST
            // Action demo something real to find.
            var query = "SELECT * FROM Users WHERE Name = '" + userName + "'";
            var command = new SqlCommand(query, connection);
            return command.ExecuteReader();
        }
    }
}
