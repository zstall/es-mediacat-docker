# Running MediaCat in Docker

To run MediaCat in Docker, follow these steps:

1. **Create a working directory** and pull down the repository.

2. **Update Mounted Storage** in the docker-compose.yaml file update:

   ```bash
   volumes:
      - /Users/zach.stall/Downloads:/app
   ```
   NOTE: I'm using my downloads folder on my mac, this simply has a lot of random files to scan. Use whatever works for you!

3. **Start the Docker containers** by running:

   ```bash
   docker-compose up --build -d
   ```

4. Once the containers are running, **open a browser and go to localhost:5000** and click on the login link:

   ![alt text](https://github.com/zstall/es-mediacat-docker/blob/main/test/localhostclicklogin.png?raw=true)

   Fill in the username with **admin** and create a password, then click **REGISTER**:

   ![alt text](https://github.com/zstall/es-mediacat-docker/blob/main/test/adminuser.png?raw=true)



5. You have now created a user, and need to populate mediacat with some data. To do this, scroll down where it says **"Welcome Admin" and in the walk dir field add:**:

   ```bash
   /app/
   ```

   ![alt text](https://github.com/zstall/es-mediacat-docker/blob/main/media/walkdir.png?raw=true)

6. That will walk a test directory with some image and files, **refresh the browser by click HOME in the nav bar**:

   ![alt text](https://github.com/zstall/es-mediacat-docker/blob/main/media/navbar.png?raw=true)

7. Finally, index the DB by clicking the 
