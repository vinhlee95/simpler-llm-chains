from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
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

# 1️⃣ First chain to generate a function to do a specific task
func_generator_prompt = PromptTemplate(
  template="Write a very short {language} function that will {task}",
  input_variables=["language", "task"],
)
func_generator_chain = LLMChain(
  llm=llm,
  prompt=func_generator_prompt,
  # 💡💡💡 The output key of this first chain MUST match with the input variable of the second chain
  output_key="function",
)

# 2️⃣ Second chain to generate a unit test to check if the function is correct
code_checking_prompt = PromptTemplate(
  template="Write a simple unit test that will check if this function {function} is correct in Python",
  # 💡💡💡 The input variable of this second chain MUST match with the output key of the first chain
  input_variables=["function"],
)
code_checking_chain = LLMChain(
  llm=llm,
  prompt=code_checking_prompt,
  output_key="test",
)

# ➕ Form a main chain that will run the two chains sequentially
main_chain = SequentialChain(
  chains=[func_generator_chain, code_checking_chain],
  input_variables=["language", "task"],
  # 💡💡💡 Output variables are name of the keys of the final result dict
  output_variables=["function", "test"],
)

result = main_chain({
  "language": args.language,
  "task": args.task,
})

print("function", result.get("function"))
print("test", result.get("test"))