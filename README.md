# ai_photography
Using AI/ML techniques to curate and edit photo albums for weddings.

## Value Proposition

Photography is an essential part to any wedding, hoping [other] to capture the most intimate, wonderful times throughout the week. When choosing a photographer, there are multiple considerations, including; professionalism, length of wedding, and number of photos expected.

For weddings with semi-professional camera crews, and with a length of roughly a week it can be expected there is anywhere from 3,000 to 10,000+ photos taken. These then need to be curated, and edited before returned to the bride and groom.

This process of curation and editing can take anywhere from 3-6 months. We will try to shorten this post image capture process, to reduce the time to return images to the married couple.

We will target photographers who charge in the region of £10,000 - £30,000 range for this service.

### First Stage

#### <ins>Problem Set</ins>

The inital step in processing the photos is the curation. This includes:
- removing **blurry**, **over/under exposed** images
- grouping duplicated images & identifying best from the set
- face segmentation, grouping by person
- grouping images by event
- selection of images to edit: X%/Y number, varied across the events/days

#### <ins>Expected Output</ins>

Given a set of X,000 images as an input, the algorithm will separate the images into folders as described below:

- Poor Quality: contains blurry, under/over exposed photos
- Events
  - Event (N): all images from event (N)
- Duplicates
  - Set (N): duplicated images. Best image indicated in file name
- Face Identification
  - Face (N): all images pertaining to person (N)
- Final Set: set of images to edit and present back to client. Contains metadata file of number of people, events covered, flaws (e.g. eyes closed).

#### <ins>Assumptions</ins>

#### <ins>(Potential) Solutions</ins>
To achieve the expected output, the following tools/capabilities are required:
- Blurry:
  - Lapacian number
- Over/Unexposed:
- Face Identification:
  - CNN neural network using **face_recognition** python package
- Duplicate Identification:
  - CNN, **imagededup** python package
- Event Identification:
  - Cross-image matching methods - see CVPR coursework 4th year
  - Check image metadata (when the photos were taken)
  - Build semantic layer of expectation (lighting, scenery)
- Facial Feature Extraction:
- Semantic Extraction:

Combining the above strategies with basic scripting should achieve the expected output.

### Future Stages

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
