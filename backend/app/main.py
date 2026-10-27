from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_dashboard import router as dashboard_router
from app.api.routes_prediction import router as prediction_router
from app.api.routes_analytics import router as analytics_router
from app.api.routes_infrastructure import router as infrastructure_router
from app.api.routes_cv import router as cv_router
from app.api.routes_optimization import router as optimization_router
from app.api.routes_chat import router as chat_router
from app.api.routes_audit import router as audit_router

from app.api.routes_damage import router as damage_router

app = FastAPI(title='AI Urban Infrastructure Failure Predictor', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(dashboard_router, prefix='/api')
app.include_router(prediction_router, prefix='/api')
app.include_router(analytics_router, prefix='/api')
app.include_router(infrastructure_router, prefix='/api')
app.include_router(damage_router, prefix='/api')
app.include_router(cv_router, prefix='/api')
app.include_router(optimization_router, prefix='/api')
app.include_router(chat_router, prefix='/api')
app.include_router(audit_router, prefix='/api')


@app.get('/api/health')
async def health():
    return {
        'status': 'ok',
        'message': 'AI Urban Infrastructure Failure Predictor backend is running.',
    }
