
# Blogpost API Documentatio
This AIP performs functions like signup,login,create,update,delete, view all and specific posts.

## To run this code
- Install the project requirements with 
 ```
 pip install -r requirements.txt 
 ```  
 - Finally run with  
 ```
 flask run
 ```

 - To sign-up user must send the following request: 
 ```
mutation signup($username: String!, $email: String!, $password: String!) {
  signup(email: $email, username: $username, password: $password) {
    user 
  }
}
 ```
 - To login user must send the following request, in return the user will get a jwt token that is set to expire in a day. This token needs to be passed in authorization header to create, update, and delete user's own post
 ```
 mutation login($username: String!, $password: String!) {
  login(username: $username, password: $password) {
    token
  }
}
 ```
 - Authorized user can create a post by sending the following request along with providing the token received from the login result in the header:  
 ```
 mutation createpost($content: String!, $title: String!) {
  createpost(content: $content, title: $title) {
    msg
  }
}
 ```
 - Authorized user can update a post by sending the following request along with providing the token received from the login result in the header:  
 ```
 mutation updatepost($content: String!, $id: Int!, $title: String!) {
  updatepost(content: $content, title: $title, id: $id) {
    msg
  }
}
 ```
  - Authorized user can delete a post by sending the following request along with providing the token received from the login result in the header:  
 ```
mutation deletepost($id: Int!) {
  deletePost(id: $id) {
    msg
  }
}
 ```
   - User can view all posts by sending the below request. Users can also specify the fields as shown in the second query
 ```
query{
  posts{}
}
```
```
query{
  posts{
  title
  content
}
}
 ```
   - User can view a single post by sending the below request. Users can also specify the fields as shown in the second query
 ```
query{
  post(id=$id){}
}
```
```
query{
  post(id=$id){
  title
  content
}
}
 ```
