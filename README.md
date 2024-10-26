
# Stag Hunt Game Visualization: China vs US on AI Policy

This project is an interactive application designed to model and analyze the strategic interactions between China and the United States in artificial intelligence (AI) policy-making. Utilizing the classic Stag Hunt game from game theory in the context of international relations, this tool provides a visual and dynamic platform for exploring the nuanced interplay between cooperation and competition between these two global superpowers.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Selecting Scenarios](#selecting-scenarios)
  - [Custom Scenario](#custom-scenario)
  - [Interpreting the Heatmap](#interpreting-the-heatmap)
- [Understanding the Game](#understanding-the-game)
- [Dependencies](#dependencies)
- [Acknowledgments](#acknowledgments)

## Overview

The **Stag Hunt** is a game that describes a conflict between safety and social cooperation. This application models the strategic interactions between China and the US as they decide whether to **cooperate** or **compete** on AI policy.

By adjusting scenarios and payoffs, users can observe how different strategies affect the outcomes for both countries and how Nash equilibria shift in response to these changes.

## Features

- **Interactive Scenarios**: Choose from predefined scenarios like Mutual Cooperation, One-Sided Cooperation, Mutual Competition, and Balanced.
- **Custom Payoff Adjustment**: Use sliders to adjust payoffs in the Custom scenario.
- **Visual Payoff Matrix**: View a heatmap representation of the payoff matrix with clear visual cues.
- **Nash Equilibria Highlighting**: Nash equilibrium cells are highlighted with gold-colored rectangles for easy identification.
- **Responsive Layout**: Consistent styling and clear visuals enhance user experience.
- **Hover Information**: Hover over cells to see detailed payoffs for both China and the US.

## Getting Started

### Prerequisites

- **Python 3.x**
- **Web Browser**: A modern browser like Chrome, Firefox, or Edge.

### Installation

If you're running the application locally or in an environment like Google Colab, you'll need to install the required packages.

#### Install Required Packages

```bash
pip install dash
pip install jupyter_dash
pip install numpy
pip install plotly
``` 
## Usage

### Selecting Scenarios
- **Dropdown Menu**: Use the dropdown menu labeled "Select Scenario" to choose a predefined scenario.
- **Scenario Description**: A description of the selected scenario will appear below the dropdown.

### Custom Scenario
- **Enable Sliders**: Select "Custom" from the dropdown menu to enable payoff adjustment sliders.
- **Adjust Payoffs**: Move the sliders to set custom payoff values for different strategy combinations.
- **Automatic Update**: The payoff matrix and Nash equilibria will update automatically based on the slider values.

### Interpreting the Heatmap
- **Cells**: Each cell represents a combination of strategies by China (rows) and the US (columns).
- **Colors**: The color intensity reflects the combined payoffs.
- **Hover Details**: Hover over a cell to see the specific payoffs for both countries.
- **Nash Equilibria**: Gold-colored rectangles highlight the Nash equilibrium cells where both countries are making the best response to each other's strategy.

## Understanding the Game

### Stag Hunt Game
The "Stag Hunt" is a scenario in game theory that describes a situation in which two players can either cooperate or compete, with the best outcome achieved when both cooperate.

### Strategies
- **Cooperate on AI Policy**: Both countries work together on AI regulations and policies.
- **Compete on AI Policy**: Each country pursues its own AI agenda, which can potentially lead to conflict or suboptimal outcomes.
- **Payoffs**: Numerical values representing the benefits each country receives from the combination of strategies.

### Nash Equilibrium
A set of strategies where no player can benefit by unilaterally changing their approach, given the other player's strategy.

## Dependencies
- **Dash**: For building the interactive web application.
- **JupyterDash**: Allows Dash apps to be run from Jupyter environments like Colab.
- **NumPy**: For numerical operations and defining payoff matrices.
- **Plotly**: For creating interactive visualizations.

## Acknowledgments
- **Jean-Jacques Rousseau's Stag Hunt Game**: Conceptual basis for the Stag Hunt game.
- **Game Theory Concepts**: The application is based on classical game theory principles.
- **Dash Documentation**: [Dash Docs](https://dash.plotly.com/) for providing comprehensive guides and tutorials.
- **Plotly Graphing Library**: For the interactive and visually appealing graphs.



