# ITSG-2024-2025


## Cursuri

Sapt 1: Deschiderea anului universitar :)

Sapt 2: [Introducere](Lectures/01_ML_review.ppt)

Sapt 3: ML [review1](Examples/MLalgorithms.ipynb) [review2](Examples/MLopenCourse.ipynb)
<!-- 
Sapt 4: [AI for problem solving](Lectures/02_optim.ppt) and [ML for Computer Vision - part 1](Lectures/03_CV_ML_part1.ppt)

Sapt 5: [ML for Computer Vision - part 2](Lectures/03_CV_ML.ppt)

Sapt 6: Discutie cu Zoltan Balint despre imagistica medicala

Sapt 7: [ML for NLP](Lectures/04_TextMining.ppt)

Sapt 8: Testing ML-based systems 
- step1: watch the video-lecture - see MsTeam platform (folder ClassMaterials - week08_part1) and this [material](Lectures/05_modelQuality.ppt) 
- step2: reading aux materials - possible starting points: 
    * Continuous Delivery for Machine Learning [link](https://martinfowler.com/articles/cd4ml.html#TestingAndQualityInMachineLearning)
    * Zhang, J. M., Harman, M., Ma, L., & Liu, Y. (2020). Machine learning testing: Survey, landscapes and horizons. IEEE Transactions on Software Engineering [pdf](papers/Zhang2020.pdf)
- step3: live lecture & in-class group session

Sapt 9: Quality of an ML-based system

Sapt 11: AI in mobile apps 

Sapt 12: Data importance in AI

Sapt 13: Fairness in AI

Sapt 14: Complex networks -->

## Despre proiecte

Proiectul pe care trebuie să-l realizaţi este o oportunitate de a explora o problemă din domeniul Inteligentei Artificiale (AI) în contextul unor date reale. Proiectul va fi evaluat atat la finalul semestrului, cat si pe parcursul semestrului cand fiecare echipă va trebui să prezinte cadrului didactic îndrumător aplicaţia realizată şi raportul tehnic aferent ei.

**Metode de AI**

1. Clasificarea de imagini/texte/alte date folosind tehnici de Federated learning
    - [link](https://federated.withgoogle.com/), 
    - [link](https://github.com/tensorflow/federated)

2. Tehnici de invatare semi-supervizata pentru probleme de detectie in imagini.
    - [link](https://arxiv.org/pdf/2105.13502.pdf)

3. Tehnici de invatare bazate pe grafe
    - [link](https://github.com/pyg-team/pytorch_geometric)
    - [link](http://snap.stanford.edu/graphlearning-workshop/)

**Analiza modelelor inteligente**
1. Performanta
    - calitativa (eroare, acuratete, precizie, IoU, Dice, etc.)
    - din punct de vedere al complexitatii (temporale si spatiale)
2. Modele de explicabilitate 
    - [link](https://christophm.github.io/interpretable-ml-book/index.html)
    - [link](https://ema.drwhy.ai/preface.html)



Proiectul implică:
- alegerea unei teme
- formarea unei echipe de 2-4 membri
- rezolvarea unei probleme cu ajutorul unei tehnici de AI din cele enumerate mai sus şi analiza rezultatelor obţinute (analiza numerica si cu ajutorul unui model de Explainable AI).
- dezvoltarea aplicatiei (care integreaza algoritmii inteligenti)
- redactarea documentatiei (raportului)
- realizarea unei postari pe [blog](Medium)
- prezentarea proiectului


**Dezvoltarea aplicatiei**
In realizarea aplicatiei se pot folosi diferite limbaje de programare, tehnologii si instrumente specifice AI. Codebase-urile aferente aplicatiilor trebuie incarcate, inainte de expirarea termenelor, [aici](https://classroom.github.com/a/qRLDYEtS).
[Good tips](https://www.deeplearningbook.org/)

**Raportul tehnic**
Trebuie redactat in latex conform modelului de [aici](Report/texModel/model.tex) si trebuie sa fie structurat conform recomandarilor de [aici](Report/readme.md). 

**Postarea pe blog**
Scrierea unei postari pe blog este usoara si intuitiva (a se vedea recomandarile de mai jos):
1. inscrierea/autentificarea pe [Medium](https://medium.com/)
2. creare draft
    - draft nou [link](https://medium.com/new-story)
    - re-editare draft [link](https://medium.com/me/stories/drafts)
3. revizie postare
    - transmiteti coordonatorului link-ul spre draftul postarii ("Share draft link")
    - va rog sa nu publicati blog-ul inainte de a fi revizuit de un mentor
4. publicare
    - incorporare feedback in postare


    First, please read this article [link](https://www.google.com/url?q=https://towardsdatascience.com/questions-96667b06af5&sa=D&source=editors&ust=1727864471183094&usg=AOvVaw2gWVLXH3STS3Yv1KmA7r-7) carefully to learn about how to write machine learning blog posts. For this course project, please also follow the instructions below.


In the blog posts, you should include the following:

- At the beginning of your blog post, include “By XXX, YYY, ZZZ as part of the Stanford CS224W course project.”, where XXX, YYY, ZZZ are the names of the team members.
- Wherever applicable:
    - The domain(s) that you are applying graph ML to.
    - Dataset descriptions (source, pre-processing etc).
    - Results that you obtain using the model on the dataset
- Paper references as [1], [2], etc., see this blog post as an example [link](https://www.google.com/url?q=https://towardsdatascience.com/geometric-foundations-of-deep-learning-94cdd45b451d&sa=D&source=editors&ust=1727864471183983&usg=AOvVaw0TFbr6e5F15Kl2-Ho4wmZL).
- Step-by-step explanation of graph ML techniques you are using
    - You can assume the following for the readers.
        - Readers are familiar with machine learning (e.g., CS229) and deep learning (e.g., ​​CS230) concepts. You do not need to explain them in detail.
        - Readers are familiar with PyTorch.
        - Readers are not familiar with graph ML.
    - Some code snippets of how you used PyG/PyTorch to implement the techniques
- Visualizations that would make the blog posts intriguing to read.
    - Gifs > Images > Text to show your methods and results.
    - Try to use videos, images, flow charts as much as possible.
    - The more visualization, the better. Reading text-occupied blogs is often painful.
    - Provide image credits if you are adopting figures from other places (we encourage you to make your own figures).
- Link to your Google Colab that can be used to reproduce your results.
- Avoid criticizing research / research orgs. You are here to showcase your work, not to write opinion pieces.

A good blog post should
- be fun to read with many figures and visualizations.
- be easy to follow even for graph ML novice.
- clearly convey the potential of graph ML.
- contain a good amount of PyG code snippets, with explanations, to understand how PyG is used in the project.
- be around 10 minutes to read (although this is not a hard constraint).

Examples of good blog posts:
- http://peterbloem.nl/blog/transformers 
- https://tkipf.github.io/graph-convolutional-networks/
- https://towardsdatascience.com/graph-neural-networks-as-neural-diffusion-pdes-8571b8c0c774
- https://blog.twitter.com/engineering/en_us/topics/insights/2021/temporal-graph-networks


**Prezentarea finala**
Trebuie realizata o prezentare video (teaser) a muncii realizate de-a lungul semstrului. Structura prezentarii urmează îndeaproape structura raportului, cu un accent deosebit pus pe rezultatele obţinute. Prezentarea trebuie sa se bazeze pe aproximativ 10 slide-uri şi să dureze maxim 10 minute. Expunerea trebuie să includă şi prezentarea aplicaţiei realizate şi folosite pentru efectuarea experimentelor.

**Criterii de evaluare**
Detalii despre continutul evaluarii si termenele de predare intermediare se gasesc [aici](Eval/readme.md)

Situatie punctaje [aici](?)

