# ai_photography
Using AI/ML techniques to curate and edit photo albums for weddings.

## Elements of the model
Reading:
- connecting ML models: https://github.com/langchain-ai/langchain
- https://arxiv.org/abs/2103.00020
- visual prompt tunning: https://arxiv.org/abs/2203.12119

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
Reading:
- instruction led image generation: https://www.timothybrooks.com/instruct-pix2pix , https://arxiv.org/pdf/2303.04671.pdf

- Instruction Execution
  - execute the instruction sets with the selected image directories
- TBD:
  - Rubricks to allow the execution/image generation to fall within 
