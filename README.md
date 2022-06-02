<p align='center'><img src="https://user-images.githubusercontent.com/86114549/162587112-5000b82c-bc33-4522-b8f5-ee6afdcb4fc7.png" alt="StarBoard" width="600"><br>
<b>Shoot for the stars, aim for the moon.</b>
</p>
<br>
<br>
<p align='center'>
  
  [![Badge](https://kdad0hcl2owx.runkit.sh)]() <!-- https://git.io/gradientbadge -->
  [![Badge](https://badgen.net/github/release/Criomby/StarBoard)](https://github.com/Criomby/StarBoard/releases/tag/v2.5) <!-- [https://git.io/gradientbadge](https://badgen.net/) -->
  [![Badge](https://badgen.net/badge/contact/Telegram/blue?icon=telegram)](https://t.me/criomby)
</p>
<br>

<h1>What is StarBoard?</h1>
StarBoard is a dashboard for your daily notes.<br>
Imagine it like a digital whiteboard for to organize your dialy tasks in an efficient, practical and visually pleasing manner.<br>
<br>
<br>
<br>

<h1>Features</h1>
<h2><a href="https://www.philippebraum.com/blog">See my blog</a></h2>
<br>
<br>
<br>

<h1>Setup</h1>
<h2>1. Notion pages & table setup</h2>
First, open (or create) your Notion account and create three new pages:<br>
<br>
<img width="300" alt="Pages" src="https://user-images.githubusercontent.com/86114549/171139865-305cf21a-f92e-4fb3-9778-b9beee53b445.png">
<br>
Both pages, Daily Tasks and General Tasks contain one table each (a so called <i>block</i> in Notion terminology).<br>
The table has to contain the following 4 columns:<br>
<br>
<img width="700" alt="Table block "Daily"" src="https://user-images.githubusercontent.com/86114549/171140951-f218527c-5b28-4f00-9afd-b41b1e1c2f6c.png"><br>
The Notes page has to contain a table with just one column:<br>
<br>
<img width="700" alt="table "Notes"" src="https://user-images.githubusercontent.com/86114549/171145828-46a84eff-8776-4f74-87d9-617e0e5b04be.png">

<h2>2. Notion API token & block id's</h2>
<ol>
  <li>Configure your account to be accessible via the API: <a href="https://developers.notion.com/reference/intro">official documentation</a></li>
  <li><a href="https://developers.notion.com/docs/authorization">G the API access token.</a></li>
  <li><a href="https://stackoverflow.com/questions/67618449/how-to-get-the-block-id-in-notion-api">Get the block id of each of the 3 tables (Daily, General, Notes).</a></li>
  <li><b>Enter API key and the 3 block id's into the <a href=""><b>user.py</b></a> script.</b></li>
</ol>
:heavy_check_mark: <b>SETUP DONE!</b><br>
<br>
<br>
<br>

<h1>User manual</h1>
The app refreshes itself every 10 minutes automatically (customize to your liking).<br>
It still offers a manual refresh option.<br>

<h2>Status codes</h2>
The following status codes are accepted by the app:<br>
<ul>
  <li>open</li>
  <li>in progress</li>
  <li>closed</li>
</ul>
<br>
The app supports <b>shortcuts for the status codes</b>, so the following short-codes are also accepted:
<ul>
  <li>open: '<b>o</b>', 'O' or everything in between 'o' and 'Open'</li>
  <li>in progress: '<b>ip</b>', 'i p' or everything in between 'ip' and 'In Progress'</li>
  <li>closed '<b>c</b>', 'C' or everything in between 'c' and 'Closed'</li>
</ul>
The output in the app will still show the full status code matched with the corresponding short-code.<br>

<h2>Manual refresh</h2>
The app supports the keyboard shortcut "Ctrl + c" to get into a cli prompt which allows the user to manually refresh the app data or exit.<br>
The default option is to refresh, so using the shortcut and pressing enter without entering anything will refresh the app manually.<br>
Entering "e" and enter will exit the app.<br>
