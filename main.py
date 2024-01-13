from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import argparse
import os

from dotenv import load_dotenv
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--language", type=str, help="The name of the language")
parser.add_argument("--task", type=str, help="The name of the task")

args = parser.parse_args()

api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(openai_api_key=api_key)

prompt = PromptTemplate(
  template="Write a very short {language} function that will {task}",
  input_variables=["language", "task"],
)

chain = LLMChain(
  llm=llm,
  prompt=prompt,
)

result = chain({
  "language": args.language,
  "task": args.task,
})

print(result["text"])
