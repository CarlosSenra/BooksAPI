if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:http_server", host="0.0.0.0", port=8000)
