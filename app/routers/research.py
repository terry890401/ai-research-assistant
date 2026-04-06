from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import ResearchCreate, ResearchResponse
from app.models import Research
from app.agent import run_research
import json

router = APIRouter(prefix="/research", tags=["研究任務"])

# 背景執行 Agent
def process_research(research_id: int, topic: str, db: Session, agent):
    try:
        research = db.query(Research).filter(Research.id == research_id).first()
        research.status = "running"
        db.commit()

        report = run_research(topic, agent)

        research.status = "completed"
        research.result = json.dumps(report, ensure_ascii=False)
        db.commit()

    except Exception as e:
        research = db.query(Research).filter(Research.id == research_id).first()
        research.status = "failed"
        db.commit()

# 建立研究任務
@router.post("/", response_model=ResearchResponse, status_code=201)
def create_research(
    request: Request,
    data: ResearchCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    research = Research(
        user_id=current_user.id,
        topic=data.topic,
        status="pending"
    )
    db.add(research)
    db.commit()
    db.refresh(research)

    agent = request.app.state.agent
    background_tasks.add_task(process_research, research.id, data.topic, db, agent)

    return research

# 查詢單一研究任務
@router.get("/{research_id}", response_model=ResearchResponse)
def get_research(
    research_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    research = db.query(Research).filter(Research.id == research_id).first()
    if research is None:
        raise HTTPException(status_code=404, detail="找不到該研究任務")
    if research.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="無權限存取此任務")
    return research

# 查詢所有研究任務
@router.get("/", response_model=list[ResearchResponse])
def get_all_research(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Research).filter(Research.user_id == current_user.id).all()