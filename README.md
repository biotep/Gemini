
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<br />
<p align="center">

  <h3 align="center">Gemini Pair Trade Analyzer</h3>

  <p align="center">
    A handy tool to show stock pair properties in regarding correlation & cointegration
    <br />
  </p>




<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

I've put this utility together to help finding pair trade candidates, and to optimize model parameters.

Features:

* Run linear regression on stock pairs with correlation and display cointegration statistical properties
* Display historical stock pair relationship 
* Quick & dirty backtesting for ratio and residual model trading strategies 
* Correlation matrix for a universe of stocks - work in progress

With the current setup, the program download hourly and daily OHLC stock data from Interactive Broker API. 
Other data provider can be used, eg.: yahoo finance.

First step is to modify config.ini to match your setup: add IB API IP address and the path for your historical data directory

The technology used here is Bokeh. Run the application as a web service, change to the project root directory
and execute the following command:

bokeh serve .

App starts and the UI is available on "http://localhost:5006/Bokeh_Gemini"


### Built With

Using the application with ineractive brokers requires ib_insync library
* [IB](https://interactivebrokers.com)
* [Bokeh](https://https://bokeh.org/)
* [ib_insync](https://ib-insync.readthedocs.io/api.html)



<img src="https://user-images.githubusercontent.com/6575510/134542544-282b295a-6d19-4734-8d95-55c43ece7dad.png" width="90%"></img> <img src="https://user-images.githubusercontent.com/6575510/134542571-1cc17c8e-8725-4771-951a-10a769bb3e0c.png" width="90%"></img> <img src="https://user-images.githubusercontent.com/6575510/134542573-f0837252-fe48-45dc-8373-1997a8854e24.png" width="90%"></img> <img src="https://user-images.githubusercontent.com/6575510/134542576-72dbc8bb-7b43-42ba-81ff-d82ab6532d1c.png" width="90%"></img> 


<!-- GETTING STARTED -->

<!-- ROADMAP -->
## Roadmap



<!-- CONTRIBUTING -->
## Contributing



<!-- LICENSE -->
## License



<!-- CONTACT -->
## Contact



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
