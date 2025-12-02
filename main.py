from fastapi import FastAPI 
from pydantic import BaseModel 
from typing import Dict 

app = FastAPI() 

def escape_string(string: str) -> str:
    return string.replace('"', '\\"')

def serialize_string(data: Dict[str, str]) -> str:
    compress_dict = []

    # go over each tuple and append to new dict
    for key, value in data.items():
        key_str = f"\"{escape_string(key)}\""
        val_str = f"\"{escape_string(value)}\""
        compress_dict.append(f"{key_str}:{val_str}")
    
    # return in dict form (as string) 
    return "{" + ",".join(compress_dict) + "}"

class SerializeRequest(BaseModel):
    data: Dict[str, str] # use Dict to enforce string input and return 

@app.post("/serialize")
def serialize(req: SerializeRequest):
    serialize = serialize_string(req.data)
    return {"serialized": serialize}  # don't let FastAPI JSON encode it 

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run("main:app", host="127.0.0.1", port=7000, reload=True)