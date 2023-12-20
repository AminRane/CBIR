from fastapi import FastAPI, File, UploadFile
from starlette.requests import Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import utility
import uvicorn

app = FastAPI()

# Mount the "images" directory to serve static files
app.mount("/images", StaticFiles(directory="images"), name="images")

# Templates
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/process_image/", response_class=JSONResponse)
async def process_image(query_image: UploadFile = File(...)):

    content = await query_image.read()

    top_images = utility.query_similar_images(content, 12) 
    print(top_images)
    return JSONResponse(content={"top_images": top_images})


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

