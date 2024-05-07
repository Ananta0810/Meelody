def silence(fn):
    try:
        fn()
    except Exception as e:
        from app.helpers.others import Logger
        Logger.error(e)
        pass
