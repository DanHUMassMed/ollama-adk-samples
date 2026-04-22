from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from pypdf import PdfReader
from typing import Optional
import io

def intercept_and_parse_pdf(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Intercepts requests with PDFs and converts them to raw text."""
    
    # # ✅ Write full LlmRequest to file for DEBUGGING
    # try:
    #     serialized = repr(llm_request)
    #     with open("LlmRequest.txt", "w") as f:
    #         if isinstance(serialized, dict):
    #             json.dump(serialized, f, indent=2)
    #         else:
    #             f.write(str(serialized))
    # except Exception as e:
    #     print(f"Failed to write LlmRequest to file: {e}")


    if not llm_request.contents:
        return None
        
    for content in llm_request.contents:
        if not content.parts:
            continue
            
        new_parts = []
        for part in content.parts:
            # Handle inline PDF data
            if part.inline_data and getattr(part.inline_data, 'mime_type', '') == 'application/pdf':
                try:
                    reader = PdfReader(io.BytesIO(part.inline_data.data))
                    extracted_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                    # Save to text file as requested in plan options
                    with open("parsed_paper.txt", "w") as f:
                        f.write(extracted_text)
                    new_parts.append(types.Part(text=f"The following is the extracted text from the PDF document:\n\n{extracted_text}"))
                except Exception as e:
                    print(f"Failed to parse inline PDF: {e}")
                    new_parts.append(part)
            # Handle referenced PDF file paths
            elif part.file_data and hasattr(part.file_data, 'file_uri') and str(part.file_data.file_uri).endswith('.pdf'):
                try:
                    # Strip gs:// or other schemas if needed, assuming local path for now
                    uri = part.file_data.file_uri
                    if uri.startswith('file://'):
                        uri = uri[7:]
                        
                    reader = PdfReader(uri)
                    extracted_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                    with open("parsed_paper.txt", "w") as f:
                        f.write(extracted_text)
                    new_parts.append(types.Part(text=f"The following is the extracted text from the PDF document '{uri}':\n\n{extracted_text}"))
                except Exception as e:
                    print(f"Failed to parse file URI PDF: {e}")
                    new_parts.append(part)
            else:
                new_parts.append(part)
                
        content.parts = new_parts
        
    return None
