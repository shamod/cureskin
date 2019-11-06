@app.route("/classify-url", methods = ["GET"])
async def classify_url(request):
      bytes = await get.bytes(request.query_params['url'])
      img = open_image(BytesIO(bytes))
      _,_,losses = learner.predict(img)
      return JSONResponse({
            "predictions": sorted(
                zip(cat_learner.data.classes, map(float, losses)),
                key=lamba p: p[1],
                reverse=True
            )
      })
