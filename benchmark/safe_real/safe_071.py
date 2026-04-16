# source: DjangoSafe / django/utils/text.py
# function: handle_data

class TruncateHTMLParser:
    def handle_data(self, data):
        data, output = self.process(data)
        data_len = len(data)
        if self.remaining < data_len:
            self.remaining = 0
            self.output.append(add_truncation_text(output, self.replacement))
            raise self.TruncationCompleted
        self.remaining -= data_len
        self.output.append(output)