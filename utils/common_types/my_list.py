class MyList:
    @staticmethod
    def move_element_in(list_: list, from_index: int, to_index: int) -> None:
        start: int = from_index
        end: int = to_index
        if start == end:
            return

        list_.insert(end, list_[start])

        if start > end:
            start += 1
        list_.pop(start)
