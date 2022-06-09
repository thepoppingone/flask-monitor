### Assumptions

If we want to make it more reliable to prevent memory leaks, we can use Flask + Celery workers to run constant tasks

rq-scheduler requires redis as well and to design a worker pattern for jobs to be taken

## Design considerations
- To keep logic separate
- Make the python object easily debuggable
- For Loops calls are not dependable, the response time can have some delay, best to use threads, and check on parallel 


### File Reading
- Using docker volumes for flexibility to mount files directly to src folder

## For local Testing
```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 main.py
```

## Building for docker
docker build . -t wangpp1/scheduler:latest

## Run container 
sudo docker run -v $PWD:/src -p 5001:5001 wangpp1/scheduler:latest
