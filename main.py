import sys
import re


class Filter:
    """对聊天记录进行格式化"""

    __FULL2HALF = dict((i + 0xFEE0, i) for i in range(0x21, 0x7F))
    __FULL2HALF[0x3000] = 0x20

    @staticmethod
    def __halfen(chat_history: list[str]) -> list[str]:
        """将全角字符转换为半角字符"""
        return list(
            map(
                lambda history: "".join(
                    list(map(lambda ch: ch.translate(Filter.__FULL2HALF), list(history)))
                ),
                chat_history,
            )
        )

    @staticmethod
    def __remove_empty(chat_history: list[str]) -> list[str]:
        """删除聊天记录中的空白记录"""
        return list(filter(lambda history: history, chat_history))

    @staticmethod
    def __normalize_speaker_info(chat_history: list[str]) -> list[str]:
        def replace(history: str) -> str:
            history = history.strip()
            matched = re.search(r"\d{2}:\d{2}", history)
            if matched:
                return f"\n|\no- {history[(matched.start()):]} {history[:(matched.start())]}"
            else:
                return f"\n| {history}"

        return list(map(replace, chat_history))

    @staticmethod
    def filter(strings: list[str]) -> list[str]:
        return Filter.__remove_empty(
            Filter.__normalize_speaker_info(
                Filter.__halfen(Filter.__remove_empty(strings))
            )
        )


if __name__ == "__main__":
    with open(sys.argv[1], "r") as input:
        with open(sys.argv[2], "w") as output:
            output.writelines(Filter.filter(input.readlines()))
