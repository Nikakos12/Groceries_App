from database import get_user_purchase_history
from email_service import email_tool


def purchase_history_tool(user_id):

    print('\n\n\n\n\n\n\n\n\n\n')
    print('tool called')
    print('\n\n\n\n\n\n\n')
    
    return get_user_purchase_history(
        user_id
    )

def send_email_tool(recipient, message):

    email_tool(
        recipient,
        message
    )

    return "Email sent successfully"


TOOLS = {

    "purchase_history": {

        "function": purchase_history_tool,

        "description": (
            "Returns the grocery purchase history of the current user."
        ),

        "parameters": {},
        
        "inject_user_id": True

    },

    
    "send_email": {

    "function": send_email_tool,

    "description":
        "Sends an email to the user with the requested content.",

    "parameters": {

        "recipient": {
            "type": "string",
            "description":
                "Email address of the recipient."
        },

        "message": {
            "type": "string",
            "description":
                "The content that should be sent in the email."
        }

    },

    "inject_user_id": False

}

    }