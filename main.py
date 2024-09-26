from fastapi import FastAPI, status, Query, Path, HTTPException
import uvicorn

users = [
    {"id": 1, "admin": "Admin"},
    {"id": 2, "user1": "User1"},
    {"id": 3, "user2": "User2"}
]

app = FastAPI()


@app.get('/users')
async def all_users():
    return {"users": users}


@app.get('/users/{user_id}')
async def get_user_id(user_id: int):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        return {"user": user}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with {user_id} not found")


@app.post("/users/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_user(user_id: int = Path(gt=max([i["id"] for i in users])),
                      title: str = Query(description="enter user")):
    user = {"id": user_id, "title": title}
    users.append(user)
    return {"new user": user}



@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        users.remove(user)
        return {"user is deleted": user}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f" {user_id} not found")


if __name__ == '__main__':
    uvicorn.run("__main__:app", reload=True)
