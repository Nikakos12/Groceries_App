from gemini_client import ask_gemini
from database import get_user_purchase_history
from tools import purchase_history_tool, TOOLS
from google.genai import types

class GroceryAgent:

    def format_purchase_history(self, history):

        if not history:
            return "Δεν υπάρχει ιστορικό αγορών."

        context = "Ιστορικό αγορών χρήστη:\n"

        for product, quantity in history:
            context += f"- {product}: {quantity}\n"

        return context


    def run(self, question, user_id):

        conversation = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=question)
                ]
            )
        ]


        MAX_ITERATIONS = 5


        for _ in range(MAX_ITERATIONS):

            ########### check conversation #########
            print('\n\n\n\n')
            print('this is conversation\n')
            print(conversation)
            print('this is question\n')
            print(question)

            ########### end check ##################


            # 1. Κλήση Gemini
            response = ask_gemini(conversation)


            # 2. Προσθήκη της απάντησης του Gemini στο history
            conversation.append(
                response.candidates[0].content
            )


            # 3. Έλεγχος αν ζήτησε tool
            function_call = None

            for part in response.candidates[0].content.parts:
                if part.function_call:
                    function_call = part.function_call
                    break


            # 4. Αν δεν υπάρχει tool call, τελειώσαμε
            if not function_call:
                return response.text


            # 5. Ποιο tool ζήτησε
            tool_name = function_call.name

            print("Tool requested:", tool_name)


            tool = TOOLS[tool_name]


            # 6. Παράμετροι από Gemini
            arguments = dict(
                function_call.args
            )


            # 7. Αυτόματο user_id injection
            if tool["inject_user_id"]:
                arguments["user_id"] = user_id


            print("Arguments:", arguments)


            # 8. Εκτέλεση tool
            result = tool["function"](**arguments)


            print("Tool result:", result)


            # 9. Επιστροφή αποτελέσματος στο Gemini
            function_response = types.Part.from_function_response(
                name=tool_name,
                response={
                    "result": result
                }
            )


            conversation.append(
                types.Content(
                    role="tool",
                    parts=[
                        function_response
                    ]
                )
            )


        return "I could not complete the request."