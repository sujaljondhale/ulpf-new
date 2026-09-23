<<<<<<< HEAD
from app.models.raw import RawEvent
from app.parsers.base import BaseParser, ParseResult


class TextParser(BaseParser):
    @property
    def parser_name(self) -> str:
        return "plain_text"

    def parse(self, raw_event: RawEvent) -> ParseResult:
        return ParseResult(
            status="unparsed",
            parser_name=self.parser_name,
            fields={"unparsed_message": raw_event.raw_message},
            raw_event=raw_event,
            reason="Log format unrecognized or raw text fallback. Preserving raw message."
        )
=======
from app.models.raw import RawEvent
from app.parsers.base import BaseParser, ParseResult


class TextParser(BaseParser):
    @property
    def parser_name(self) -> str:
        return "plain_text"

    def parse(self, raw_event: RawEvent) -> ParseResult:
        return ParseResult(
            status="unparsed",
            parser_name=self.parser_name,
            fields={"unparsed_message": raw_event.raw_message},
            raw_event=raw_event,
            reason="Log format unrecognized or raw text fallback. Preserving raw message."
        )
>>>>>>> 3831b7383e78d54d129d8499c87cadb87be6e6c0
