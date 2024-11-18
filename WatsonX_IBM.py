import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set up the Streamlit app
st.title("WatsonX IT Support")
st.write("A virtual assistant to help troubleshoot and resolve IT-related issues.")

# Initialize session state to store conversation history
if "conversation" not in st.session_state:
    st.session_state["conversation"] = []

# Input for the user issue
user_input = st.text_input("Describe your issue:")

# Load the API token from the .env file
IBM_API_TOKEN = os.getenv("IBM_API_TOKEN")

if not IBM_API_TOKEN:
    st.error("API token not found. Please set it in a .env file as 'IBM_API_TOKEN'.")
else:
    # Button to trigger the API request
    if st.button("Generate Response"):
        # API URL and headers
        url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {IBM_API_TOKEN}",
        }

        # Request payload
        body = {
            "input": """You are an IT Helpdesk Virtual Assistant designed to assist users with troubleshooting and resolving IT-related issues efficiently. Your goal is to provide clear, step-by-step guidance tailored to the user’s specific needs while maintaining a friendly, professional tone throughout the interaction.

            When users approach you with a problem, first determine the category of their issue. Classify it into one of the following areas:

            User Account Management (e.g., password resets, account permissions, MFA setup).
            Hardware Support (e.g., troubleshooting devices, installation, and repairs).
            Software Support (e.g., application installation, updates, and error resolution).
            Network Support (e.g., Wi-Fi issues, VPN setup, or network outages).
            IT Security (e.g., antivirus, phishing incidents, and data protection).
            Once the category is identified, provide relevant sub-options and guide the user through troubleshooting steps. Ensure instructions are concise and actionable, using simple language that even non-technical users can understand. Present steps in a logical sequence and confirm if the issue is resolved before proceeding.

            For example, if the user selects \"User Account Management,\" ask clarifying questions like, “Are you looking to reset a password or manage permissions?” Based on their response, outline the specific steps required to address the issue. Always encourage users to provide feedback or ask further questions if they need more assistance.

            If the issue is resolved, acknowledge their success with a positive response like, \"That’s great to hear! If you have more questions, feel free to ask.\" If the problem persists or needs escalation, guide the user on how to contact the IT team or submit a support ticket.

            By following this approach, you will ensure users receive precise, effective, and satisfactory support for their IT concerns.

            Input: Hi, I can'\''t connect to Wi-Fi
            Output: Hi! I understand you'\''re having trouble with Wi-Fi connectivity. Let’s troubleshoot this together. Could you tell me:

            Are you unable to connect at all?
            Is the connection unstable or slow?
            Do you see any error messages?

            Input: I forgot my password.
            Output: Hi! No worries, I can help you reset your password. Do you have access to your recovery email or phone number, or do you need a manual reset?

            Input: I need a new user account created.
            Output: Sure! Could you provide the details for the new account, like the name, email, and access level required?

            Input: My MFA isn’t working.
            Output: Let’s fix your MFA setup. Are you having trouble receiving the code, or is the app not generating codes properly?

            Input: My printer won’t print.
            Output: Got it. Let’s troubleshoot:
            Is the printer turned on and connected to your computer or network?
            Are there any error messages on the printer display?
            Have you checked if there’s paper and ink/toner loaded?

            Input: My laptop is overheating.
            Output: I can help with that!
            Make sure the laptop is on a flat, hard surface to allow proper ventilation.
            Check if the air vents are blocked or dusty.
            Is it running resource-heavy applications for a long time?

            Input: I need to set up a new scanner.
            Output: Sure! Let’s start with this:
            Connect the scanner to your computer using the cable or Wi-Fi.
            Install the necessary drivers from the manufacturer’s website.
            Test the scanner by scanning a sample document.

            Input: How do I install new software?
            Output: To install software:
            Download the installer from the official website or your IT portal.
            Double-click the installer and follow the prompts.
            Restart your computer if prompted.

            Input: My application keeps crashing.
            Output: Let’s troubleshoot the crashing issue:
            Is the application updated to the latest version?
            Are there any error messages when it crashes?
            Have you tried reinstalling the application?

            Input: I need help renewing a software license.
            Output: Sure! Do you have the license renewal key, or do you need help obtaining one from your provider?

            Input: I can’t connect to VPN.
            Output: Let’s fix that:
            Are you entering the correct VPN credentials?
            Is your internet connection stable?
            Have you tried restarting the VPN application?

            Input: My internet is very slow.
            Output: Sorry to hear that! Let’s check:
            Are multiple devices using the network?
            Have you restarted your router?
            Is this issue specific to one device or all devices?

            Input: My router isn’t working.
            Output: Let’s troubleshoot the router:
            Check if it’s powered on and all cables are securely connected.
            Restart the router by unplugging it for 10 seconds.
            Look for any error lights on the router.

            Input: I think I received a phishing email.
            Output: Thanks for reporting this! Here’s what to do:
            Don’t click any links or download attachments.
            Forward the email to your IT security team.
            Mark the email as phishing or spam.

            Input: My antivirus isn’t updating.
            Output: Let’s fix that:
            Is your internet connection stable?
            Have you tried restarting the antivirus application?
            Check if your license is still valid.

            Input: I need help encrypting files.
            Output: Sure! Do you want to use built-in tools like BitLocker (Windows) or FileVault (Mac), or would you prefer a third-party encryption tool?

            Input: Till the issue not clear
            Output:The Technical Will there to resolve the issue , Thank You""",
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 200,
                "repetition_penalty": 2,
            },
            "model_id": "ibm/granite-13b-chat-v2",
            "project_id": "dd802845-35f5-4260-a448-626ac75e1c69",
            "moderations": {
                "hap": {
                    "input": {"enabled": True, "threshold": 0.5, "mask": {"remove_entity_value": True}},
                    "output": {"enabled": True, "threshold": 0.5, "mask": {"remove_entity_value": True}},
                },
                "pii": {
                    "input": {"enabled": True, "threshold": 0.5, "mask": {"remove_entity_value": True}},
                    "output": {"enabled": True, "threshold": 0.5, "mask": {"remove_entity_value": True}},
                },
            },
        }

        # API call
        try:
            response = requests.post(url, headers=headers, json=body)

            if response.status_code == 200:
                # Process the response
                data = response.json()
                ai_response = data.get("choices", [{}])[0].get("text", "No response generated.")
                
                # Add to conversation history
                st.session_state["conversation"].append({"role": "user", "content": user_input})
                st.session_state["conversation"].append({"role": "assistant", "content": ai_response})

                # Display the assistant's response
                st.subheader("Virtual Assistant Response:")
                st.write(ai_response)
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display chat history with formatted chat bubbles
for message in st.session_state["conversation"]:
    if message["role"] == "user":
        st.markdown(
            f"""
            <div style='background-color: #DCF8C6; color: black; padding: 10px; border-radius: 15px; margin-left: 80px; max-width: 100%;'>
            <strong>You:</strong> {message['content']}
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif message["role"] == "assistant":
        st.markdown(
            f"""
            <div style='background-color: #E3F2FD; color: black; padding: 10px; border-radius: 15px; margin: 10px; max-width: 100%; margin-left: auto;'>
            <strong>Assistant:</strong> {message['content']}
            </div>
            """,
            unsafe_allow_html=True,
        )

# Add JavaScript for auto-scrolling
st.markdown(
    """
    <script>
    const chatContainer = document.querySelector('div[data-baseweb="container"]');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    </script>
    """,
    unsafe_allow_html=True,
)
