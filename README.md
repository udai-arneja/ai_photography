# ai_photography
Using AI/ML techniques to curate and edit photo albums for weddings.

## Elements of the model
- connecting ML models: https://github.com/langchain-ai/langchain
### Visual Perception
Takes in images from an albums and results in the following:
- Curation
  - Separating images with poor "low-level" quality. Focusing on blurriness, clarity, exposure levels, duplicates.
  - Segementation of images based on context. Focussing on people in the images.
- Selection - of the high-enough quality images.
  - Final photos suggestion, those that capture the entire event and form a good representation of the wedding
  - Photos for minor editing (contrast, brightness, etc) => GENERATES INSTRUCTION SET
  - Photos for major editing (creating a story, sihlowetting etc) => GENERATES INSTRUCTION SET
### Image Generation/Editing
- Instruction Execution
  - execute the instruction sets with the selected image directories
- TBD:
  - Rubricks to allow the execution/image generation to fall within 
