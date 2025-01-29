# Fetch Technical Takehome - Receipt Processor - Kenyon Allan
Submission for the technical takehome described at https://github.com/fetch-rewards/receipt-processor-challenge by Kenyon Allan.

Developed in Python using Pydantic, Flask, and Marshmallow.

## How to run
1. Clone the repository
2. Run `docker compose up` in the root directory
3. The API will be available at `http://localhost:5001`
4. The app can be stopped by using `ctrl + c` in the terminal running the docker compose command

### API Endpoints
- POST `http://localhost:5001/receipts/process`
- GET `http://localhost:5001/receipts/<id>/points`

## Notes and Assumptions
- I noticed that all of the regex patterns included in the spec use double escaped backslashes. I'm assuming that the intention is for them to not actually be escaped this way to make sense (i.e. \\\w is supposed to be \w).
- I interpreted "after 2:00pm and before 4:00pm" to be non-inclusive, so 2:00 and 4:00 are invalid, but 2:01 and 3:59 are valid.
- I used a singleton for handling the id : receipt data relationship. It's not thread safe, and is definitely more over-engineered than just having a global dictionary or storing things in flask.g but I felt it was cleaner for me to work with since it made the whole thing object based and I'm assuming this will be running in a single thread with the current constraints. If it wasn't to be stored in memory, a database would be used in place here.
- I went ahead and cached (using the singleton) the id : points lookup in case an id is checked multiple times per session so it doesn't need to recalculate each time.
- There's a couple debug logger statements in the code for checking things like the point by point calculation. If it's desired for these to be seen in the console for any reason, the logger level can be changed from `INFO` -> `DEBUG` in the `app.py` file.

#### Note on Testing
While not directly part of the API. I've included some tests for the models and the API in the tests/ directory. These are written using pytest and all pass on my local machine at time of submission.