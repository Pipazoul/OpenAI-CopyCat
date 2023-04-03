# Start the uvicorn server
#uvicorn main:app --host 0.0.0.0 --port 8000 --reload

while true; do
    uvicorn main:app --host 0.0.0.0 --port 8000 
    sleep 1
done