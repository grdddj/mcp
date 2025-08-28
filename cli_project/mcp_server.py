from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


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


if __name__ == "__main__":
    mcp.run(transport="stdio")
