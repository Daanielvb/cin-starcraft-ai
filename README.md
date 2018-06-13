# CIn/UFPE - StarCraft 2 Project
This is a project for the master degree class *IN1100 (Agentes Cognitivos e Adaptativos - ACA)* at CIn/UFPE. Year 2018.1. 

## Team
* Daniel Cirne (dcvs@cin.ufpe.br)
* Eduardo Matos (ejvm@cin.ufpe.br)
* Eduardo Simões (ecs4@cin.ufpe.br)
* Marlom Oliveira (mjdo@cin.ufpe.br)

## Environment Setup

### StarCraft 2 Installation
For Windows, get the installer from [link](https://us.battle.net/account/download/) and follow the instructions for its installation.

For Linux., get the linux package version 4.1.2 from [link](http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.1.2.60604_2018_05_16.zip) and unzip it using the password **iagreetotheeula** on `$HOME` directory. Then download the [Melee](http://blzdistsc2-a.akamaihd.net/MapPacks/Melee.zip) map pack and unzip it into the game folder. It should be into the folder *Maps*. Follow the final folder structure:
```shell
StarCraftII/
├── AppData
├── Battle.net
├── Interfaces
├── Libs
├── Maps
│   ├── Melee
│   │   ├── Empty128.SC2Map
│   │   ├── Flat128.SC2Map
│   │   ├── Flat32.SC2Map
│   │   ├── Flat48.SC2Map
│   │   ├── Flat64.SC2Map
│   │   ├── Flat96.SC2Map
│   │   ├── Simple128.SC2Map
│   │   ├── Simple64.SC2Map
│   │   └── Simple96.SC2Map
│   └── mini_games
│       ├── BuildMarines.SC2Map
│       ├── CollectMineralsAndGas.SC2Map
│       ├── CollectMineralShards.SC2Map
│       ├── DefeatRoaches.SC2Map
│       ├── DefeatZerglingsAndBanelings.SC2Map
│       ├── FindAndDefeatZerglings.SC2Map
│       └── MoveToBeacon.SC2Map
├── Replays
├── SC2Data
└── Versions
```

### Python Version
The Python version required is 3.6 or newer.
[Windows installer](https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe). For Linux it might already brings it by default. Just type `python3` on terminal. In any case.

### Clone this project
```shell
$ git clone git@github.com:Daanielvb/cin-starcraft-ai.git
```

### Create VirtualEnv 
```shell
$ mkdir $HOME/.virtualenvs
$ cd $HOME/.virtualenvs
$ python3 -m venv cin-starcraft-ai
```

### Install the dependencies
```shell
$ source $HOME/.virtualenvs/cin-starcraft-ai/bin/activate
(cin-starcraft-ai) $ cd [CIN_STARCRAFT_AI_FOLDER_PATH]
(cin-starcraft-ai) $ pip install -r requirements-dev.txt
```

## How To Run
```shell
$ source $HOME/.virtualenvs/cin-starcraft-ai/bin/activate
(cin-starcraft-ai) $ cd [CIN_STARCRAFT_AI_FOLDER_PATH]
(cin-starcraft-ai) $ python -m pysc2.bin.agent --map Simple64 --agent agent.Agent --agent_race terran
```

## References
* https://github.com/deepmind/pysc2
* https://github.com/Blizzard/s2client-proto
* https://itnext.io/build-a-sparse-reward-pysc2-agent-a44e94ba5255
* https://chatbotslife.com/building-a-basic-pysc2-agent-b109cde1477c
* https://chatbotslife.com/building-a-smart-pysc2-agent-cdc269cb095d
* https://itnext.io/add-smart-attacking-to-your-pysc2-agent-17fd5caad578
* https://itnext.io/build-a-sparse-reward-pysc2-agent-a44e94ba5255
