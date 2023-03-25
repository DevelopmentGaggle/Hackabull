import openai
import API_KEY

# Set up the OpenAI API client
openai.api_key = API_KEY.api_key

# Set up the model and prompt
model_engine = "text-davinci-003"


class PromptResponder:
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.average_call = 0
        self.number_of_calls = 0

    def get_response(self, user_input: str):
        input_prompt = "Context: \"" + self.prompt + "\"\n\nUser input: \"" + user_input + "\"\n"
        print(input_prompt)
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=input_prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        self.average_call = (completion.response_ms + self.average_call * self.number_of_calls) / (self.number_of_calls + 1)
        self.number_of_calls += 1

        return completion.choices[0].text


prompt_responder = PromptResponder("""
The user can ask two types of questions, and you will respond with an answer if enough information is given or ask additional clarifying questions until enough information has been gathered.
The first type of question will use information you know from the internet.
- Attempt to answer like this unless the user requests information that is not available on the internet.
- These will likely be a majority of the questions.
The second type of question will use of a set of given functions to answer the question.
- This second type of question will often ask for information that you do not directly know, and using a combination of the given functions would allow you to know this information.
- DO NO USE ANY OTHER FUNCTIONS OTHER THAN THE ONES DEFINED. You must only use the functions defined below.
- Especially if no answer is possible, consider answering the question using the first method defined above, using its formatting.


A list of all the available functions you can use are included below.
Function descriptions start:
1. spotify_get_liked_count() where the returned value is the number of liked songs in your spotify account.

End of function descriptions, no other functions defined.


A few examples with proper formatting are provided below for how to answer the user prompts:
An example for the first type of question is;
input: "How old Benjamin Franklin was when he died", output: "Answer: Benjamin Franklin was 84 years old when he died".
An example for the second type of question when it is possible is;
input: "How many liked songs do I have on my spotify account", output: "Function(s): spotify_get_liked_count()"
An example for the second type of question when it is not possible is;
input: "How many computers do I own?", output: "Function(s): N/A"
""")

print(prompt_responder.get_response("How tall is the tallest building?"))
# print(prompt_responder.get_response("How many playlists do I have?"))
# print(prompt_responder.get_response("How many liked songs do I have?"))


# prompt_responder = PromptResponder("""
# Answer the following user defined question
#
# """)
#
# print(prompt_responder.get_response("How tall is the tallest building?"))