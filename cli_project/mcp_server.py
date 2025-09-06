from pydantic import Field
from fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from dotenv import load_dotenv
import os
import requests


load_dotenv()


mcp = FastMCP("DocumentMCP", log_level="INFO")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string.",
)
def read_doc_contents(
    doc_id: str = Field(description="The ID of the document to read."),
) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID {doc_id} not found.")
    return docs[doc_id]


@mcp.tool(
    name="edit_doc_contents",
    description="Edit the contents of a document and return the updated content.",
)
def edit_doc_contents(
    doc_id: str = Field(description="The ID of the document to edit."),
    old_str: str = Field(
        description="The old content to replace. Must match exactly, including whitespace."
    ),
    new_str: str = Field(description="The new content to replace the old content."),
) -> None:
    if doc_id not in docs:
        raise ValueError(f"Document with ID {doc_id} not found.")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)


@mcp.tool(
    name="send_me_notification",
    description="Send me a notification about something.",
)
def send_me_notification(
    title: str = Field(description="The title of the notification."),
    message: str = Field(description="The message of the notification."),
) -> None:
    PUSHBULLET_TOKEN = os.getenv("PUSHBULLET_TOKEN", "")
    PUSHBULLET_URL = "https://api.pushbullet.com/v2/pushes"

    if not PUSHBULLET_TOKEN:
        raise RuntimeError("PUSHBULLET_TOKEN is not set in environment variables.")

    headers = {
        "Access-Token": PUSHBULLET_TOKEN,
        "Content-Type": "application/json",
    }
    data = {"type": "note", "title": title, "body": message}
    response = requests.post(PUSHBULLET_URL, json=data, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to send notification: {response.status_code} {response.text}"
        )


@mcp.resource("docs://documents", mime_type="application/json")
def list_doc_ids() -> list[str]:
    return list(docs.keys())


@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def get_doc_contents(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID {doc_id} not found.")
    return docs[doc_id]


@mcp.prompt(
    name="format",
    description="Rewrite a document in markdown format.",
)
def format_document(
    doc_id: str = Field(description="The ID of the document to format."),
) -> list[base.Message]:
    prompt = f"""
    You are a helpful assistant that rewrites documents in markdown format.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra text, but don't change the meaning of the report.
    Use the 'edit_doc_contents' tool to edit the document.
    After you edit the document, please give be back the new text.
    """
    return [base.UserMessage(prompt)]


# TODO: Write a prompt to summarize a doc
@mcp.prompt(
    name="summarize",
    description="Summarize a document in a few sentences.",
)
def summarize_document(
    doc_id: str = Field(description="The ID of the document to summarize."),
) -> list[base.Message]:
    prompt = f"""
    You are a helpful assistant that summarizes documents in a few sentences.

    The id of the document you need to summarize is:
    <document_id>
    {doc_id}
    </document_id>

    Use the 'read_doc_contents' tool to read the document.
    After you read the document, please give me back a summary of the document in a few sentences.
    """
    return [base.UserMessage(prompt)]


if __name__ == "__main__":
    # mcp.run(transport="stdio")
    mcp.run(transport="http", host="127.0.0.1", port=6277, path="/mcp")
