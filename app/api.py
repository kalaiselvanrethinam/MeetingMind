from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request

from app.config import APP_TODAY
from app.llm.client import ask_llm

from app.models import AskRequest
from app.retrieval.retriever import retrieve_turns
from app.services.citation_service import build_citations
from app.services.filter_service import filter_meetings
from app.services.meeting_service import load_meetings
from app.services.validation_service import validate_filters
from app.services.scope_service import is_out_of_scope
from app.llm.token_limiter import limit_turns_by_tokens




router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/ask")
def ask_question(
    request: AskRequest,
    http_request: Request,
):
    # 1. Validate question
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    # 2. Check whether the question is in scope
    if is_out_of_scope(request.question):
        return {
            "request_id": f"r-{uuid4().hex[:8]}",
            "answer": (
                "This request is outside the scope of MeetingMind. "
                "Please ask a question about the available meetings."
            ),
            "route": "out_of_scope",
            "citations": [],
            "filters": {
                "date_from": request.date_from,
                "date_to": request.date_to,
                "project": request.project,
                "speaker": request.speaker,
            },
            "reference_date": request.as_of or APP_TODAY,
        }


    # 3. Determine reference date
    reference_date = request.as_of or APP_TODAY

   
    # 4. Reuse database loaded at startup
    database = http_request.app.state.database

    # 5. Validate filters
    try:
        validate_filters(
            project=request.project,
            speaker=request.speaker,
            date_from=request.date_from,
            date_to=request.date_to,
            as_of=reference_date,
            projects=database["projects"],
            people=database["people"],
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    # 6. Load all meetings
    meetings = http_request.app.state.meetings

    # 7. Apply filters BEFORE retrieval
    filtered_meetings = filter_meetings(
        meetings,
        project=request.project,
        speaker=request.speaker,
        date_from=request.date_from,
        date_to=request.date_to,
        as_of=reference_date,
    )

    
    # 8. Retrieve relevant transcript turns
    retrieved_turns = retrieve_turns(
        filtered_meetings,
        question=request.question,
        top_k=10,
    )

    # 9. Limit transcript evidence to stay within the token budget
    limited_turns = limit_turns_by_tokens(retrieved_turns)
    print("QUESTION:", request.question)
    print("TURNS SENT TO LLM:", [turn["text"] for turn in limited_turns])   

    # 10. Ask the LLM/mock LLM to answer from limited evidence
    try:
        llm_result = ask_llm(
        question=request.question,
        turns=limited_turns,
    )
    except Exception as error:
        print("LLM ERROR:", repr(error))
        raise


    # 11. Convert LLM turn numbers into trusted citations
    citations = build_citations(
    limited_turns,
    llm_result.get("turn_numbers", []),
    )

    # 12. Build final API response
    return {
        "request_id": f"r-{uuid4().hex[:8]}",
        "answer": llm_result["answer"],
        "route": llm_result["route"],
        "citations": citations,
        "filters": {
            "date_from": request.date_from,
            "date_to": request.date_to,
            "project": request.project,
            "speaker": request.speaker,
        },
        "reference_date": reference_date,
    }