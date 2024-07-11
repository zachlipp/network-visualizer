<h1 align="center">Voter Network Visualizer Demo</h1>
<h3 align="center">Provided to the Sanders 2020 primary campaign</h3>

![](https://github.com/zachlipp/network-visualizer/blob/figs/figs/overview.gif)

## 📝 Overview
The goal of this project was to provide a way to display and work with relational data for political campaigns' field organizers. This is a slightly refreshed and **entirely** anonymized version of the code provided to the Sanders primary campaign in 2020. It's a fun example of building a data-intensive, interactive application without having to write bespoke JavaScript.

## 💥 Features
### 🔍 **Searching and filtering**
<details>
<summary>See it yourself!</summary>
<img src="https://github.com/zachlipp/network-visualizer/blob/figs/figs/search.gif" />
</details>
Users can filter records with searches, eventually visualzing all connections for one person by clicking on thier record. This lets an organizer see the individual's network before contacting them.

### 🗒️ **Your data, front-and-center**
<details>
<summary>See it yourself!</summary>
<img src="https://github.com/zachlipp/network-visualizer/blob/figs/figs/tables.png" />
</details>
This is a very table-heavy application. The idea is that this replaces some querying and maybe even coding for a technically-minded user.

### 🤯 **3 entire dimensions (oooOoOo!)**
<details>
<summary>See it yourself!</summary>
<img src="https://github.com/zachlipp/network-visualizer/blob/figs/figs/rotate.gif" />
</details>
Is it necessary? No. Is it cool? Yes. 📊 😎

## ⚡ Quick Start
- Clone this repository: `git clone https://github.com/zachlipp/network-visualizer.git`
- Build and run the Docker image: `docker compose up --build`
- Try out the app at `http://localhost:8050`

## 🥁 Personal rating + reflection 🥁
<details open="">
<summary>Personal rating</summary>
<h3>❤️❤️❤️🖤🖤 (3/5)</h3>
<h3>Reflection</h3>

<p>This is the coolest project I have ever gotten to work on. We built the car as we drove. The app is fun and performed specifications.</p>

<p>That said, I've learned a lot since I built this. Even though this project rocks, this isn't exactly the quality of code I'd submit for a job interview. Consider this a useful prototype provided on a tight timeline - after all, that's what it is.</p>

<h3>Areas for improvement</h3>
<ul>
    <li><strong>Carefully consider the flow of data through the application</strong>. When are we using base Python? pandas? networkx? plotly? I think answering these questions would be a useful guide in a refactor.</li>
    <li><strong>Design patterns for testing everything</strong>. The goal isn't 100% coverage; it's to establish patterns that could be extended to get to very high coverage. This will lead to a lot of refactoring, especially of the complicated Dash decorators. These scare me a little in retrospect.</li>
    <li><strong>Be exceedingly careful about the words "graph" and "network"</strong>. They are very overloaded in this project - even just trying to update it has my eyes swimming.</li>
</ul>
</details>

## 🤝 Contributing
I am not interested in adding features to this application. That said, I welcome contributions to clean up and test the codebase. I would gladly pair program on some of it, too!

## 🤗 Kudos
- Gus Sánchez ([@lgsc](https://github.com/lgsc)): 🫡 Tons of code, suggesting and guiding the project
- Benjamin Arnav ([@benarnav](https://github.com/benarnav)): 🥵🌶️ [README inspiration](https://github.com/benarnav/bytephase)
- Mohammad Shamshiri ([@ma-shamshiri](https://github.com/ma-shamshiri)): 🔥🎮 [README inspiration](https://github.com/ma-shamshiri/Pacman-Game)
