from sqlalchemy import Column, Unicode, Float, LargeBinary
from config.database import FastModel


class APSchedulerJob(FastModel):
  __tablename__ = "apscheduler_jobs"
  __table_args__ = {"info": {"skip_autogenerate": True}}

  id = Column(Unicode(191), primary_key=True)
  next_run_time = Column(Float(25), index=True)
  job_state = Column(LargeBinary, nullable=False)
