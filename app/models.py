from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, nullable=True, index=True)

    # dados principais
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    team_home = Column(String, nullable=False)
    team_away = Column(String, nullable=False)

    # contexto do jogo
    stage = Column(String, nullable=True)
    group = Column(String, nullable=True)
    stadium = Column(String, nullable=True)

    # atualização futura
    score_home = Column(Integer, nullable=True)
    score_away = Column(Integer, nullable=True)
    status = Column(String, default="scheduled")  # scheduled, live, finished