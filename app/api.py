from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.presentation.http.controllers.questionnaire_router import (
    router as questionnaire_router,
)
from app.presentation.http.controllers.question_router import router as question_router

app = FastAPI(title="My API")


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(status_code=404, content={"detail": "Not Found!"})


# add code here
app.include_router(questionnaire_router)
app.include_router(question_router)
