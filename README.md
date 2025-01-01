<a id="readme-top"></a>
<!-- HEADER -->
[![Python][Python]][Python-url] [![Jupyter][Jupyter]][Jupyter-url] [![Docker][Docker]][Docker-url]

# SPARCED, An Aspiring MCF-10A Whole-Cell Model 

<!-- SHIELDS -->
[![Maintenance][maintenance-shield]][maintenance-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]

<!-- LOGO -->
<div align="center">
  </br>
  <a href="https://www.nature.com/articles/s41467-022-31138-1">
    <img src="https://storage.googleapis.com/plos-corpus-prod/10.1371/journal.pcbi.1005985/2/pcbi.1005985.g001.PNG_L?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=wombat-sa%40plos-prod.iam.gserviceaccount.com%2F20241216%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20241216T094255Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=b83746cf2fc11d2ed64dbdfdc217a4023978d1c8893ce846265c073032301df2ba44b1ae1613b227b0db50398d1ef9c4ba93355b4987ce89286a08a6f2d950247e315bbda56f21094806b48f734ad69b6e4dcdad51d6744babd767f53eb0be691a639418d60109283598f9c10bde7010c61f2c79435bff5cf181473e57fbf7a901ab89aadb57b208c5bed1347e37bb52ebbf8856d6d1df456dc56901227afb652aa7dacd30e62253e7e969ee0fa6057dc3eb14506f549988000e4fb0c25616c465cb9009756c34fc3c2f45c4c3d558ce01650bb3f2272deaed94fd3a07b6b8432b75ab296844412dc83f42ac9910111534489b999b6e8cf383b16cdcfeaf5c48" alt="SPARCED Model Overview" width="256">
  </a>
</br>
</br>

**[Explore the docs](http://sparced-documentation.rtfd.io/)
· [Report Bug](https://github.com/SPARCED/SPARCED/issues/new?labels=bug)
· [Request Feature](https://github.com/SPARCED/SPARCED/issues/new?labels=enhancement)**
</div>

<!-- TABLE OF CONTENTS -->
## Table of Contents
<details>
  <summary>Contents</summary>
  <ol>
    <li>
      <a href="#about-sparced">About SPARCED</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#systems-biology-modelers">For Systems Biology Modelers</a></li>
        <li><a href="#developpers">For Developpers</a></li>
      </ul>
    </li>
    <li><a href="#replicate-our-results">Replicate our results</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT -->
## About SPARCED

SPARCED is a **simple** and **efficient pipeline** for constructing, merging, expanding and simulating **large-scale**, single-cell mechanistic models.

* With **minimal set-up**, users can configure small-scale experiments on their local machines, is it through pure Python scripts or Jupyter Notebooks.
* Both **Docker** and **Singularity** containers are provided.
* SPARCED is also compatible with **High Performance Computing** and parallelization.

The acronym SPARCED stands for _**S**BML, **P**roliferation, **A**poptosis, **R**eceptor signaling, **C**ell cycle, **E**xpression & **D**NA damage_, which are sub-models of the large-scale mechanistic model.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Systems Biology Modelers

The SPARCED pipeline can be run with few to no previous coding experience.
To do so, we strongly encourage you to use the Docker / Singularity containers we provide.

_A complete installation guide is available [here](https://sparced-documentation.readthedocs.io/en/latest/tutorials/container.html)._

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Developpers

We recommend to use [Anaconda](https://www.anaconda.com/) and create a conda environment based on the [environment.yml](https://github.com/SPARCED/SPARCED/blob/master/environment.yml) file we provide.
Otherwise, you may base yourself on the [requirements.txt](https://github.com/SPARCED/SPARCED/blob/master/requirements.txt) file we provide for the minimal required versions.

_A detailed installation guide is available [here](https://sparced-documentation.readthedocs.io/en/latest/installation-guide.html)._

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Replicate our results

You will find specific instructions on how to run the model (including previousversions) as described in each of our published papers [here](https://sparced-documentation.readthedocs.io/en/latest/papers/summary.html).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

The SPARCED model can be used to create and run small to large-scale mechanistic models.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request.
You can also simply open an issue with the tag "enhancement".
Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the GNU General Public License v2.0. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

SPARCED is a product of the [Birtwistle Lab](http://www.birtwistlelab.com/) and the [Erdem Lab](https://erdemlab.github.io/).

We greatly appreciate the help from multiple colloborators, including the [Hasenauer Lab](https://www.mathematics-and-life-sciences.uni-bonn.de/en/research/hasenauer-group).

_This material is based on work supported by the National Science Foundation
under Grant Nos. MRI# 2024205, MRI# 1725573, and CRI# 2010270._

_Any opinions, findings and conclusions or recommendations expressed in this
material are those of the author(s) and do not necessarily reflect the views of
the National Science Foundation._

_Clemson University is acknowledged for their generous allotment of compute time
on the Palmetto Cluster._

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

<div align="center">

[Contact the Birtwisle Lab](https://www.birtwistlelab.com/contact) · [Contact the Erdem Lab](https://www.umu.se/en/research/groups/cemal-erdem-lab/)

![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)

</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[Python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Jupyter]: https://img.shields.io/badge/Jupyter-000000?style=for-the-badge&logo=Jupyter
[Jupyter-url]: https://jupyter.org/try
[Docker]: https://img.shields.io/badge/docker-000000?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[maintenance-shield]: https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge
[maintenance-url]: https://github.com/SPARCED/SPARCED/graphs/commit-activity
[contributors-shield]: https://img.shields.io/github/contributors/SPARCED/SPARCED.svg?style=for-the-badge
[contributors-url]: https://github.com/SPARCED/SPARCED/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/SPARCED/SPARCED.svg?style=for-the-badge
[forks-url]: https://github.com/SPARCED/SPARCED/network/members
[stars-shield]: https://img.shields.io/github/stars/SPARCED/SPARCED.svg?style=for-the-badge
[stars-url]: https://github.com/SPARCED/SPARCED/stargazers
[issues-shield]: https://img.shields.io/github/issues/SPARCED/SPARCED.svg?style=for-the-badge
[issues-url]: https://github.com/SPARCED/SPARCED/issues
[license-shield]: https://img.shields.io/github/license/SPARCED/SPARCED.svg?style=for-the-badge
[license-url]: https://github.com/SPARCED/SPARCED/blob/master/LICENSE.txt
