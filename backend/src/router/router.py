from router import index, academy, biography, comment, masterclass, partition, tag, user, video, work_analysis

def routing(app):
    app.include_router(index.router)
    app.include_router(academy.router)
    app.include_router(biography.router)
    app.include_router(comment.router)
    app.include_router(masterclass.router)
    app.include_router(partition.router)
    app.include_router(tag.router)
    app.include_router(user.router)
    app.include_router(video.router)
    app.include_router(work_analysis.router)