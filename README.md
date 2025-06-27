# Social Network Services is fullstack application which allows to connect telegram account and view your tg chats

### How to launch it
1. Clone repository and cd:
  ```bash
  git clone https://github.com/AlexeyTarasov77/sns-test-task && cd sns-test-task
  ```
2. Create backend .env file:
  ```bash
    cd backend && cp .example.env .env
  ```

3. Start backend server (you need to additionally use something like ngrok to run your dev server over https - otherwise cookies won't work)
  ```bash
    make docker/up
  ```

4. Run database migrations
  ```bash
    make docker/run-migrations
  ```

5. Change api base url to match your backend server:
  ```bash
    cd ../frontend
  ```
  Open `src/shared/constants/base.ts` in your editor and change value of SERVER_URL constant, 
e.g `export const SERVER_URL = "https://localhost:8000/api/v1"` if server is running on localhost (remember cookies won't work on localhost, and therefore auth won't work too because token is saved in cookies)

6. Start frontend next.js server
  ```bash
    npm install && npm run dev
  ```

7. Enjoy the app!
