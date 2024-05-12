def silence(fn):
    try:
        fn()
    except Exception as e:
        from app.utils.others import Logger
        Logger.error(e)
        pass
