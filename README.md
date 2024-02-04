# style-transfer
An image processing project where we implement style transfer, which is a type of content mixing of two images, via texture synthesis algorithms, we implemented Style Transfer based on Elad's et al. paper "Style-Transfer via Texture-Synthesis", which relies on classical methods. The original paper can be found at [original](https://arxiv.org/abs/1609.03057), and our documentation is available at [original doc](https://drive.google.com/file/d/19spwLj2io5snppn04L6t4C7YNug0SsMC/view).

## The Proposed Algorithm
1) Segmentation
2) Building Gaussian Pyramids
3) Initialization
4) Color Transfer
5) Patch Matching
6) Robust Aggregation
7) Content Fusion
8) Denoise

Each step will be discussed in details.

### 1) Segmentation
Our exploration encompassed the implementation of different segmentation techniques. Initially, we employed GrabCut, as advocated in Elad's paper. However, GrabCut's reliance on user-defined foreground and background annotations often resulted in suboptimal performance, particularly when these annotations were absent, leading to degraded outcomes.
Subsequently, an alternative edge-based segmentation technique was adopted. This technique involved a series of
steps, starting with the application of the Canny edge detection algorithm, followed by dilation, contour extraction, and subsequent filling. Notably, this approach exhibited superior performance in multiple scenarios, showcasing improved outcomes compared to GrabCut in diverse contexts.

Segmentation mask using GrabCut algorithm             |  Segmentation mask using edge-Based Segmentation
:-------------------------:|:-------------------------:
![image](https://github.com/Amreux/style-transfer/assets/96792115/5ac95505-a61e-4b73-bf93-898f64ac8051) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/5e5b23ff-c9e0-4bff-806d-2541d5563e08)

### 2) Building Gaussian Pyramids
The process of constructing Gaussian pyramids involves downscaling the resolution of the content, style and segmentation mask images, creating multiple layers. Operating the style transfer algorithm on each of these layers is instrumental in enhancing the content image's capacity to assimilate broader stylistic features from the style image.

### 3) Initialization
Following the completion of pre-processing functions and pyramid construction, the algorithm initiates X, the primary image subjected to algorithmic operations. Initially set as the content image, X undergoes an additional procedural step wherein a significant amount of Gaussian noise is applied.
The deliberate injection of Gaussian noise into the content image, serving as the basis for subsequent operations, fostersa more pronounced and authentic style transfer experience, minimizing repetitive patterns and enhancing the overall stylistic coherence within the transformed image.

Patch matching on uniform white image with no noise             |  Patch matching on uniform image with added noise
:-------------------------:|:-------------------------:
![image](https://github.com/Amreux/style-transfer/assets/96792115/75414132-0a15-42c2-8776-133aba79502d) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/be4d6e92-55a3-4765-b9c8-617e1993cf5b)

### 4) Color Transfer
The process of color transfer involves transposing the color palette from the style image onto the content image. Several methodologies were explored to accomplish this task, commencing with histogram matching, as advocated in Elad’s paper While histogram matching showcased efficacy in many instances, it occasionally exhibited limitations, leading to instances of extreme color transfer. To mitigate these challenges and ensure a more nuanced and controlled color transformation, an alternative approach was adopted. Subsequently, color transfer in LAB channels was implemented as an alternative methodology.

Original image             |  Style
:-------------------------:|:-------------------------:
![image](https://github.com/Amreux/style-transfer/assets/96792115/deda0153-f2b1-4346-a654-3d1d0f013794) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/e7d9ae47-6c46-43ab-a5c3-4a0607ed8482)

Color transfer using histogram matching             |  Color transfer using LAB channels.
:-------------------------:|:-------------------------:
![image](https://github.com/Amreux/style-transfer/assets/96792115/41bbf85a-c0f4-4864-b8e5-ba8570fe153a) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/82b0e2be-4b08-40f0-939b-a93a30dfbf07)

### 5) Patch Matching
The crux of patch matching revolves around identifying the nearest patch in the style image that corresponds to the current patch in the content image. This fundamental process ensures that the changes introduced post-style transfer remain coherent with the original content.
The minimization task aims to determine the most fitting patch in the style image, corresponding to each patch in the content image, using a Nearest Neighbor approach. However, the exhaustive nature of Nearest Neighbor for each patch incurs substantial computational overheads. To address the computational complexity while retaining fidelity in patch matching, Principal Component Analysis (PCA) was employed as an alternative.

Patch matching with patch sizes = [40, 30]             |  Patch matching with patch sizes = [20, 10]
:-------------------------:|:-------------------------:
![image](https://github.com/Amreux/style-transfer/assets/96792115/83bba289-c345-4a0f-9b90-faea8435a6f1) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/0ece5e86-fe12-47ba-a95b-946f96036804)

### 6) Robust Aggregation
Robust Aggregation, a crucial procedure within the style transfer algorithm, involves the systematic adjustment of each patch in the content image. This adjustment aims to iteratively align each content patch closer to its matched counterpart in the style image.
The methodology employed for this purpose, as elucidated in Kwatra's paper, relies on Iteratively Reweighted Least Squares (IRLS). This technique systematically refines the content patches by iteratively adjusting their attributes to converge towards the corresponding style patches.

### 7) Content Fusion
Content Fusion serves as the pivotal stage in the style transfer process, focusing on reapplying the content image in alignment with the segmentation outcome. This crucial step aims to ensure the preservation of significant content elements within the final stylized output.

### 8) Denoise
Denoising stands as a crucial step within the style transfer process, pivotal in guaranteeing seamless transitions within the resultant image. It plays a pivotal role in refining the overall visual quality by minimizing unwanted artifacts or noise.
Throughout our experimentation, various denoising methodologies were rigorously assessed for their efficacy in achieving smooth transitions within the output image. Among the methodologies scrutinized, the Bilateral Filter emerged as the most proficient performer.

## Experiment Results
Content             |  Style  | Result
:-------------------------:|:-------------------------:|:-------------------------:
![image](https://github.com/Amreux/style-transfer/assets/96792115/7a36216b-4d3e-4cdf-9ad6-564eaddb66da)   | ![image](https://github.com/Amreux/style-transfer/assets/96792115/666a3a48-595c-45a4-b8f6-5187b108e125)   | ![image](https://github.com/Amreux/style-transfer/assets/96792115/8e56a10f-8748-442d-87dc-972daa29f35a)
![image](https://github.com/Amreux/style-transfer/assets/96792115/65376237-17dd-45c2-9cfb-25797ef89acc) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/6d0d9942-e239-47b9-bfa6-4c6709ad306e) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/bbe127db-14d3-4ee5-beae-953fab5e83fe)
![image](https://github.com/Amreux/style-transfer/assets/96792115/f095dea9-1ead-4890-afa4-e2465d8cd0f3) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/482503e2-028e-4cdd-9a63-d3be8dcb0221) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/4a42f1f1-276f-47d8-8136-d9447c7c3ce3)
![image](https://github.com/Amreux/style-transfer/assets/96792115/1823795c-96ff-4252-ad7d-e4e2970b6838) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/34b69ca4-a9ef-414f-9a78-15a3bd3b18ef) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/4ea619e2-d885-4998-b0d6-dcba79aeac5e)
![image](https://github.com/Amreux/style-transfer/assets/96792115/94207654-2876-41dc-98e2-61385a5b6d55) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/e4cccfd5-ad27-408a-a6a9-01455cd8fac5) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/7e00be23-37d8-47ff-a9bb-6488b38278e5)
![image](https://github.com/Amreux/style-transfer/assets/96792115/702eee98-73b9-4543-b140-d34a3d8524e8) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/b82cdb59-3148-4c7e-9879-2e03badb171c) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/9ec21518-00a7-4a6a-9020-dba01a8e3789)

We also modified the algorithm to preserve the geometric shapes in the style images.

Content             |  Style  | Result
:-------------------------:|:-------------------------:|:-------------------------:
![image](https://github.com/Amreux/style-transfer/assets/96792115/5899a217-d4f6-4187-a3a0-dda2f37f9574) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/bb8a07a4-037c-4193-ae62-7810a8af24a7) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/f42b4e91-e3d4-4c07-a34a-3d8cb4f78fc2)
![image](https://github.com/Amreux/style-transfer/assets/96792115/f694d9f8-a170-4349-ad8a-f6d24876b430) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/70038e61-0029-4a04-af75-b8625c4de255) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/83d710dd-c928-46b0-bb3e-055aad6f97bd)
![image](https://github.com/Amreux/style-transfer/assets/96792115/d86b0e82-a14f-4e50-ae70-04b9a2eca5f3) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/e1c2af3e-1105-4e22-be8d-7d2b83fb7722) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/10a8e452-3a79-4241-8321-49bb493820dc)
![image](https://github.com/Amreux/style-transfer/assets/96792115/5a8d87bf-3099-4329-9e90-e515743f260b) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/6a585dc2-62e0-471f-b969-d673325bd825) | ![image](https://github.com/Amreux/style-transfer/assets/96792115/7672791f-cb1d-448d-b442-16debf1aa129)


## ©️Developers

| Name                 |         Email          |
|----------------------|:----------------------:|
| Fares Atef           | faresatef553@gmail.com |
| Ghaith Mohamed       |  gaoia123@gmail.com    |
| Amr ElSheshtawy      | Sheshtawy321@gmail.com |
| Amr Magdy            |  amr4121999@gmail.com  |
