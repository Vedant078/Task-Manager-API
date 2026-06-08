from sqlmodel import create_engine, SQLModel, Session

# 1. Connects directly to the local PostgreSQL database drawer you created
DATABASE_URL = "postgresql://localhost/task_db"

# 2. The core engine that manages communication traffic lines
engine = create_engine(DATABASE_URL, echo=True)

# 3. Tells PostgreSQL to automatically build tables based on our blueprints
def init_db():
    SQLModel.metadata.create_all(engine)

# 4. Generates a safe, temporary database session for your endpoints, then closes it
def get_session():
    with Session(engine) as session:
        yield session