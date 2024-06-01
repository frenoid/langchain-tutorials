#!/bin/python

# Serves LangChain Server on http://localhost:5001/chain
# UI is available at http://192.168.3.201:5001/chain/playground/
# API docs at: http://192.168.3.201:5001/docs

#!/usr/bin/env python
import os
from typing import List

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. Create model
os.environ["OPENAI_API_BASE"] = "http://localhost:9999/"
os.environ["OPENAI_API_KEY"] = "123456789" # dummy
model = ChatOpenAI(model="mistral-7b-instruct-v0.3")

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser


# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route

add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5001)