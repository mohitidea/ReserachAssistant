from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config= SettingsConfigDict(env_file='.env', extra='ignore')
    app_name: str= "Research Assistant"
    ollama_base_url: str= "http://localhost:11434"
    llm_model: str= "llama3.2"
    embed_model: str= "nomic-embed-text"
    chroma_dir:str= "./chroma_db"
    database_url: str= "sqlite:///./app.db"
    jwt_secret: str= ""
    jwt_algorithm: str= "HS256"
    jwt_expire_minutes: int= 60

settings= Settings()