# -*- coding: utf-8 -*-
# Time      :2025/4/01 11:00
# Author    :Dylanoy
from typing import Optional, AsyncIterator
import asyncio
import uuid

from .base_llm import BaseLLM

__all__ = ["MlxLmGenerator"]


class MlxLmGenerator(BaseLLM):
    def __init__(
            self,
            model_path: str,
            max_length: int = 32768,
            stop_tokens: Optional[list[str]] = None,
            stop_token_ids: Optional[list[int]] = None,
            **kwargs):
        from mlx_lm import load, generate, stream_generate

        # Load the model and tokenizer
        self.model, tokenizer = load(model_path)

        # Store the generate function for later use
        self.generate_fn = generate
        self.stream_generate_fn = stream_generate

        super(MlxLmGenerator, self).__init__(
            tokenizer=model_path,
            max_length=max_length,
            stop_tokens=stop_tokens,
            stop_token_ids=stop_token_ids,
        )

    async def random_uid(self):
        """Generate a random UUID for request tracking"""
        return str(uuid.uuid4())

    async def async_generate(
            self,
            prompt: str,
            max_tokens: int = 1024,
            temperature: float = 0.9,
            top_p: float = 0.9,
            top_k: int = 50,
            **kwargs
    ) -> str:

        result = self.generate_fn(
            self.model,
            self.tokenizer,
            prompt=prompt,
            verbose=False,
            max_tokens=max_tokens,
            **kwargs)

        return result

    async def async_stream_generate(
            self,
            prompt: str,
            max_tokens: int = 1024,
            temperature: float = 0.9,
            top_p: float = 0.9,
            top_k: int = 50,
            **kwargs) -> AsyncIterator[str]:

        for response in self.stream_generate_fn(self.model, self.tokenizer, prompt, max_tokens=max_tokens):
            yield response.text
