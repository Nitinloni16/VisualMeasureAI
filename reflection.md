# Design Decisions & Reflection

## Architectural Decisions
1.  **Strict Pydantic Models**: I chose to define extremely strict Pydantic models (e.g., `-5.0` to `+5.0` range constraints) to ensure the AI's output is always valid and normalized before it reaches the frontend or database. This acts as a robust anti-corruption layer.
2.  **Vision Service Abstraction**: The `IVisionService` interface allows switching between `MockVisionService`, `OpenAIVisionService`, or others (Gemini/Claude) without changing the API or Frontend code. This is essential for testability and portability.
3.  **Visual-Only Prompting**: The system prompt explicitly forbids non-visual inferences. This design choice prevents hallucinations about brand, price, or function, which are common pitfalls in multimodal AI.
4.  **Backend-Driven Logic**: All business logic (scoring ranges, validation) resides in the backend. The frontend is a dumb terminal that renders whatever the backend provides.

## Trade-offs
-   **Mock Data**: For this prototype, I used a `MockVisionService` to simulate AI responses. A real integration would introduce latency and non-determinism, handling which requires more robust error handling and retries (which I added structure for).
-   **Minimal UI**: The frontend is functional but minimal. I prioritized the data visualization (progress bars) over aesthetic polish, as requested ("clarity over polish").

## Future Improvements
-   **Image Pre-processing**: cropping or normalizing images before sending to the Vision API to improve accuracy.
-   **Batch Processing**: The API accepts a list of URLs but processes conceptually as one item. True batching for multiple products would be a logical next step.
-   **Feedback Loop**: Allowing users to correct the AI's scores in the UI and saving that data to fine-tune the prompt or model.
