import random
from kivy.clock import Clock


class TokenSimulation:
    def stream(self, text, min_chunk=1, max_chunk=4,
               min_delay=0.02, max_delay=0.08):
        i = 0
        while i < len(text):
            chunk_size = random.randint(min_chunk, max_chunk)
            chunk = text[i:i + chunk_size]
            i += chunk_size
            yield chunk, random.uniform(min_delay, max_delay)

    def ui_text(self, label, text,
                min_chunk=1, max_chunk=4,
                min_delay=0.02, max_delay=0.08):

        stream = self.stream(
            text,
            min_chunk=min_chunk,
            max_chunk=max_chunk,
            min_delay=min_delay,
            max_delay=max_delay
        )

        def step(dt):
            try:
                chunk, delay = next(stream)
                label.text += chunk
                Clock.schedule_once(step, delay)
            except StopIteration:
                pass

        Clock.schedule_once(step, 0)
