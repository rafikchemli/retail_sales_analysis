#!/bin/bash

PORT=8015

# Kill any processes running on the specified port
lsof -ti tcp:$PORT | xargs kill -9

# Launch the Streamlit app on the specified port
streamlit run app.py --server.port $PORT
