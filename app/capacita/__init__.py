def main() -> None:
    import uvicorn

    from capacita.settings import settings

    uvicorn.run("capacita.main:app", host=settings.host, port=settings.port, reload=False)

