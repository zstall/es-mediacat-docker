# Running MediaCat in Docker

To run MediaCat in Docker, follow these steps:

1. **Create a working directory** and pull down the repository.

2. **Build the docker image** by running:

   ```bash
   docker build -t zstall/mediacat-flask-app:latest .
   ```

3. **Start the Docker containers** by running:

   ```bash
   docker compose up -d
   ```

4. Once the containers are running, **open a browser and go to localhost:5000** and click on the login link:

   ![alt text](https://github.com/zstall/mediacat-sqlalchemy/blob/main/test/localhostclicklogin.png?raw=true)

   Fill in the username with **admin** and create a password, then click **REGISTER**:

   ![alt text](https://github.com/zstall/mediacat-sqlalchemy/blob/main/test/adminuser.png?raw=true)



5. You have now created a user, and need to populate mediacat with some data. To do this, scroll down where it says **"Welcome Admin" and in the walk dir field add:**:

   ```bash
   /mediacatapp/test/
   ```

   ![alt text](https://github.com/zstall/mediacat-sqlalchemy/blob/main/test/walkdir.png?raw=true)

6. That will walk a test directory with some image and files, **refresh the browser by click HOME in the nav bar**:

   ![alt text](https://github.com/zstall/mediacat-sqlalchemy/blob/main/test/navbar.png?raw=true)

7. Congrats, Mediacat is now up and running!
