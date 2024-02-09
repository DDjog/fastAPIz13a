#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from ipaddress import ip_address
from typing import Callable

import redis.asyncio as redis
import uvicorn

from fastapi import Depends, FastAPI, Request, status

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.routes import contacts, auth, users
from src.conf.config import settings

app = FastAPI()
   
origins = [
    "http://localhost:8000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


banned_ips = [ip_address("192.168.1.1"), ip_address("192.168.1.2")]

allowed_ips = [ip_address('192.168.1.0'), ip_address('172.16.0.0'), ip_address("127.0.0.1")]

user_agent_ban_list = [
                            #r"Gecko", # e.g. for Firefox
                            r"Python-urllib"]

@app.middleware("http")
async def limit_access_by_ip(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    
    if ip in banned_ips:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
    
    if ip not in allowed_ips:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Not allowed IP address"})
    
    user_agent = request.headers.get("user-agent")
    print("User agent:", user_agent)
    for ban_pattern in user_agent_ban_list:
        if re.search(ban_pattern, user_agent):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "UsrAgn: You are banned"})    
    
    response = await call_next(request)
    
    return response

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

#
# API methods
#

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def root():
    return {"message": "--> mega super duper FastAPI sample contacts  <--"}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

    